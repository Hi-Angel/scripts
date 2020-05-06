#!/usr/bin/python
# requires python-gobject
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Formats:
    def __init__(self, target, clipboard):
        self.name    = target.name()
        self.content = clipboard.wait_for_contents(target)
        self.text    = self.content.get_data() if self.content else None

clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
targets   = clipboard.wait_for_targets()
formats   = [Formats(target, clipboard) for target in targets.targets]
print('\n'.join([f'{format.name}:\t{format.text}' for format in formats]))
