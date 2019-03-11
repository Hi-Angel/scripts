use strict;
use warnings;

# this is the analog to -i option on command line; it enables in-place editing
our $^I = '';

my $start_match = "Format for the datetime that a message being replied to was received";
my @clock_formats = ("%-l:%M %p", "%l:%M %p", "%H:%M %p", "%H:%M", "%H.%M", "%-l:%M", "%-k:%M");

# in-place editiing works *only* with variable named @ARGV. So we save its old
# content, and later overwrite variable
my @file_list = @ARGV;
my $line_processed = 1;

foreach my $file(@file_list) {
    # open my $file, $filename or die "couldn't open $file: $!";
    my @ARGV = ($file);
    while (<ARGV>) {
        if ($line_processed == 1 and m/$start_match/) {
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
                if (m/\Q$clock/) {
                    s/\Q$clock/%s/;
                    last;
                }
            }
            print;
            # on 5-th: double %
            $line_processed = 1;
        } else {
            print;
        }
    }
}
