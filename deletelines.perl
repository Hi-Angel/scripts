#!/usr/bin/perl -w
use strict;
use warnings;

our $^I = '.bak';

my $start_match = "Format for the datetime that a message being replied to was received";
my @clock_formats = ("%-l:%M %p", "%l:%M %p", "%H:%M %p", "%H:%M", "%H.%M", "%-l:%M", "%-k:%M");

foreach my $file_str(@ARGV) {
    open my $file, $file_str or die "couldn't open $file_str: $!";
    our @arr = $file;
    while (my $line = <arr>) {
    #     if ($line ~= m/$start_match/) {
    #         print "Yay";
    #     }
        print;
    }
    # delete 2 lines
    # replace 3-rd and 4-th to exact text
    # on 5-th: double %
    # on 5-th: replace clock_formats with %s
}
