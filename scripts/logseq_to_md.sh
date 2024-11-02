#!/usr/bin/perl

use strict;
use warnings;

my $fname = "input.md";

open my $f, "<", $fname or die "Failed to open file: $!";
my $fstring = do { local $/; <$f> };
close $f;
my $temp = $fstring;

# Output images
open( my $fh, '>', 'output_images.txt' ) or die "Could not open file 'output_images.txt' $!";

while ( $temp =~ /\!\[[^(]*\]\(\.\.\/assets\/([^)]*)\)/g ) {
    print $fh "$1\n";
}

close $fh;

# general clean-up
$temp =~ s/^[ \t]*- /\n/g;
$temp =~ s/\$ ([\.,!;:?])/\$$1/g;
$temp =~ s/collapsed:: true//g;

# Change image name files
$temp =~ s/\!\[[^(]*\]\(\.\.\/assets\/([^)]*)\)/![]($1)/g;

# thm, prop, proof
$temp =~ s/PROP\./::: \{\#prp-todo\}\n\n\#\# \n\n:::/g;
$temp =~ s/THM\./::: \{\#thm-todo\}\n\n\#\# \n\n:::/g;
$temp =~ s/COR\./::: \{\#cor-todo\}\n\n\#\# \n\n:::/g;
$temp =~ s/LEMMA\./::: \{\#thm-todo\}\n\n\#\# \n\n:::/g;
$temp =~ s/PROOF\./::: \{.proof\}\n\n:::/g;

$temp =~ s/WARN\./::: \{.callout-warning\}\n\n:::/g;
$temp =~ s/COMM\./::: \{.callout-tip\}\n\n:::/g;
$temp =~ s/INTP\./::: \{.callout-note title=\"Interpretation\"\}\n\n:::/g;
$temp =~ s/NOTE\./::: \{.callout-note\}\n\n:::/g;

# my math shorthands
$temp =~ s/(?i)(wolog)/WLOG/g;
$temp =~ s/wirt/with respect to/g;
$temp =~ s/bequl/the following are equivalent/g;
$temp =~ s/cone\(/\\mathrm\{Cone\}(/g;
$temp =~ s/E(_\{[^}]*\})\[/\\mathbb\{E\}$1\[/g;
$temp =~ s/D\(([^;]+);([^\)]+)\)/D\($1 \\\| $2\)/g;

# # general clean-up
$temp =~ s/\s+\$\$\s+- /\$\$\n\n/g;
$temp =~ s/\s+\$\$\s+/\$\$\n\n/g;
$temp =~ s/^\t+ *-/\n/mg;
$temp =~ s/^ +//mg;
$temp =~ s/^-//mg;
$temp =~ s/\n\n\n+/\n\n/g;


# Output to "output.md"
open my $output, ">", "output.md" or die "Failed to open output file: $!";
print $output $temp;
close $output;

# Screw this perl shit.
my $outfname = "output.md";
system("sed -i 's/\\\n\\\n\\\n\\\{1,\\\}/\\\n\\\n/g' $outfname"); 

exit 0
