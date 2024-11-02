#!/usr/bin/perl

use strict;
use warnings;
use File::Copy;

# Open the filenames file.
open(my $filenames_fh, '<', 'filenames.txt') or die "Could not open file 'filenames.txt' $!\n";

# Source directory.
my $source_dir = '/home/assets/';

# Read filenames.txt line by line.
while (my $filename = <$filenames_fh>) {
    chomp $filename;  # Remove newline character.

    # Construct the source file path.
    my $source_file = $source_dir . $filename;

    # Copy the file if it exists in the source directory.
    if (-e $source_file) {
        copy($source_file, $filename) or die "Could not copy file '$source_file' to '$filename': $!\n";
        print "Copied '$filename'\n"; # Optional: Print a confirmation message.
    } else {
        warn "File '$source_file' not found.\n"; # Optional: Warn if the source file doesn't exist.
    }
}

# Close the filenames file.
close $filenames_fh;
