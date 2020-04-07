#!/usr/bin/perl
# this shows a pop up message if SWAP file has less than 25% left. For those
# wondering, whether system is usable at that moment: well, with ZSWAP enabled on
# 5.3 and later kernel (at least with an SSD disk) there's no lags until SWAP
# gets 100% full.
use warnings;
use strict;

my $user_alerted=0;
while (1) {
    my $free_output=`free`;
    foreach (split /^/, $free_output) {
        if (/^Swap/) {
            my $total = (split /\s+/)[1];
            if ($total == 0) {
                print "Swap is missing, nothing to do\n"
            } else {
                my $used = (split /\s+/)[2];
                my $threshold = $total*0.75;
                if ($threshold <= $used) {
                    if (not $user_alerted) {
                        if (system('notify-send "Warning" "Your memory is low!"')) {
                            die 'Failed to call notify-send!'
                        }
                        $user_alerted = 1;
                    }
                } else {
                    $user_alerted = 0;
                }
            }
        }
    }
    sleep(5);
}
