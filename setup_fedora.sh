#!/bin/bash

# script for setting up a clean newly installed (no modifications) Fedora.
# Comment out unnecessary sections/installations before use.

set -exu

cd ~/ # we assume to be working in /home/foo/

function fail() {
    echo "${@}"
    exit 1
}

if mount | grep btrfs > /dev/null; then
    if [[ ! $(mount | grep btrfs) == *zstd:3* ]]; then
        fail "enable zstd:3 (default compression version) on btrfs partition, space_cache=v2,autodefrag"
    fi
fi

if [[ ! $(mount | grep " / ") == *noatime* ]] || [[ ! $(mount | grep " /home ") == *noatime* ]]; then
    fail "enable noatime on / and home"
fi

sudo systemctl disable --now systemd-oomd{,.socket}
sudo systemctl mask systemd-oomd #there's a bug that systemd-oomd will restart even after being disabled

### ZSWAP setup
# I want SWAP + ZSWAP, no ZRAM.
if [ -e /sys/module/zram ]; then
    sudo touch /etc/systemd/zram-generator.conf # disables Fedora ZRAM service
fi

sudo sh -c 'echo add_drivers+=\" lz4hc lz4hc_compress \" > /etc/dracut.conf.d/lz4hc.conf'
sudo dracut --regenerate-all --force
sudo sed -i 's/GRUB_CMDLINE_LINUX="[^"]*/& zswap.enabled=1 zswap.max_pool_percent=25 zswap.compressor=lz4hc/' /etc/default/grub
sudo sh -c 'echo GRUB_SAVEDEFAULT=true >> /etc/default/grub' # load last chosen kernel
sudo grub2-mkconfig -o /etc/grub2.cfg
sudo cp /etc/grub2{,-efi}.cfg
#### END of ZSWAP setup

### installation
# util-linux-user provides chsh
# konsole is way better than gnome-terminal
# sqlite: required for zsh completion
# gnome-extensions-app: why do they even install Gnome without the app?
# moreutils provides ifne
# aspell-{ru,en} hunspell-{ru,en}: for good measure both lang-checking packages
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install vim git zsh google-chrome-stable util-linux-user konsole qutebrowser moreutils libva-utils libva-intel-driver aspell-{ru,en} hunspell-{ru,en} lshw ack
### END installation

### zsh section
wget https://raw.githubusercontent.com/Hi-Angel/dotfiles/master/.zshrc
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
git clone https://github.com/robbyrussell/oh-my-zsh ~/.oh-my-zsh
chsh -s $(which zsh)
### END zsh section

### konsole setup
mkdir ~/Projects
git clone https://github.com/Hi-Angel/dotfiles/ ~/Projects/dotfiles
cp -rv ~/Projects/dotfiles/.local ~/
### END konsole setup

### vim setup
wget https://raw.githubusercontent.com/Hi-Angel/dotfiles/master/.vimrc
git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
mkdir -p ~/.vim/autoload
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
### END vim setup

cp -r ~/Projects/dotfiles/.config ~/
cp ~/Projects/dotfiles/.XCompose ~/
sudo cp ~/Projects/dotfiles/etc/sysctl.d/99-sysctl.conf /etc/sysctl.d/
sudo sh -c "echo LC_TIME=ru_RU.UTF-8 >> /etc/environment"

### Gnome setup
# I don't use Gnome, but let's make it a bit more usable for other people
# Might require Gnome restart, since editing via command-line is badly integrated in Gnome.
gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true
gsettings set org.gnome.Settings last-panel power
gsettings set org.gnome.desktop.input-sources xkb-options "['compose:menu']"
gsettings set org.gnome.desktop.interface show-battery-percentage true
gsettings set org.gnome.desktop.session idle-delay uint32 600
### END Gnome setup

### install liquorix-kernel 
# it has MLRU patchset included, which is a must have till it landed upstream
sudo dnf copr enable rmnscnce/kernel-lqx -y
sudo dnf install kernel-lqx
### END install liquorix-kernel 

### podman setup
if [ ! -e /etc/subgid ]; then
    sudo sh -c 'echo $(whoami):100000:65536 > /etc/subgid'
    sudo cp /etc/sub{g,u}id
fi
### END podman setup

### sway
sudo dnf install sway python-i3ipc rofi i3blocks network-manager-applet
cp -r ~/Projects/dotfiles/.config/sway ~/.config
curl -LSso ~/.config/sway/inactive-windows-transparency.py https://raw.githubusercontent.com/swaywm/sway/master/contrib/inactive-windows-transparency.py
mkdir -p ~/Pictures
curl -LSso ~/Pictures/ANIME-PICTURES.NET_-_130164-1600x989-original-sakimichan-long+hair-wide+image-grey+hair-horn+%28horns%29.jpg https://ip1.anime-pictures.net/direct-images/dae/dae6076faa97645534586ab1d22603c3.jpg?if=ANIME-PICTURES.NET_-_130164-1600x989-original-sakimichan-long+hair-light+erotic-wide+image-horn+%28horns%29.jpg
### END sway

### Plasma + i3
systemctl mask plasma-kwin_x11.target --user
systemctl enable plasma-i3 --user
sudo dnf install -y i3 feh xinput picom xset
sudo dnf groupinstall -y "KDE Plasma Workspaces"
### END KDE

### Emacs
sudo dnf install emacs
cp -r ~/Projects/dotfiles/.emacs* ~/
# didn't care to automate packages installation. See comment at the top of `.emacs`.
### END Emacs

# some stuff is hard to install from cmd line or doesn't make much sense in general configuration
# * Tray is a must have on Gnome: https://extensions.gnome.org/extension/2890/tray-icons-reloaded/
# * skype, telegram, vaapi for Chrome
