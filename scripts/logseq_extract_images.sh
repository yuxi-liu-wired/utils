#!/usr/bin/perl

use strict;
use warnings;

# Open the input file (input.md).
open(my $in_fh, '<', 'input.md') or die "Could not open file 'input.md' $!\n";

# Open the output file (output.md).
open(my $out_fh, '>', 'output.md') or die "Could not open file 'output.md' $!\n";

# Open the output file for filenames.
open(my $filenames_fh, '>', 'filenames.txt') or die "Could not open file 'filenames.txt' $!\n";

# Read the input file line by line.
while (my $line = <$in_fh>) {
    # Substitute the image paths using a regular expression.
    $line =~ s/!\[[^\]]*\]\(\.\.\/assets\/([^\)]*)\)/!\[$1](figure\/$1)/g;

    # Print the modified line to the output file.
    print $out_fh $line;

    # Extract and print the filenames to filenames.txt.
    if ($line =~ /!\[[^\]]*\]\(figure\/([^\)]*)\)/) {
        print $filenames_fh "$1\n";
    }
}

# Close all files.
close $in_fh;
close $out_fh;
close $filenames_fh;