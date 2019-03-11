use strict;
use warnings;

# this is the analog to -i option on command line; it enables in-place editing
our $^I = '.bak';

my $start_match = "Format for the datetime that a message being replied to was received";
my @clock_formats = ("%-l:%M %p", "%l:%M %p", "%H:%M %p", "%H:%M", "%H.%M", "%-l:%M", "%-k:%M");

# in-place editiing works *only* with variable named @ARGV. So we save its old
# content, and later overwrite variable
my @file_list = @ARGV;

foreach my $file(@file_list) {
    # open my $file, $filename or die "couldn't open $file: $!";
    my @ARGV = ($file);
    while (<ARGV>) {
        if (m/$start_match/) {
            print "Yay";
        }
        print;
    }
    # delete 2 lines
    # replace 3-rd and 4-th to exact text
    # on 5-th: double %
    # on 5-th: replace clock_formats with %s
}
