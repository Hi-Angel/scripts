use strict;
use warnings;

# this is the analog to -i option on command line; it enables in-place editing
our $^I = '';

my $start_match = "Format for the datetime that a message being replied to was received";
my @clock_formats = ("%-Hu%M", "%-k.%M-kor", "%-l∶%M %p", "%-l:%M %p", "%l:%M %p", "%H:%M %p", "%-H:%M", "%H∶%M", "%H:%M", "%H.%M", "%-l:%M", "%-k:%M");

my $line_processed = 1;

while (readline) {
    # \Q means "exact substring match"
    if ($line_processed == 1 and m/\Q$start_match/) {
        # ignore 1st line
        $line_processed = 2;
    } elsif ($line_processed == 2) {
        # ignore 2nd line
        $line_processed++;
    } elsif ($line_processed == 3) {
        # replace 3-rd to exact text
        print "#: src/client/util/util-date.vala:217\n";
        $line_processed++;
    } elsif ($line_processed == 4) {
        # replace 4-th to exact text
        print "msgid \"%%a, %%b %%-e, %%Y at %s\"\n";
        $line_processed++;
    } elsif ($line_processed == 5) {
        # replace clock_format with %s
        foreach my $clock(@clock_formats) {
            last if s/\Q$clock/%s/;
        }
        # double "%"s except in "%s"
        s/%([^s])/%%$1/g;
        print;
        $line_processed = 1;
    } else {
        print;
    }
}
