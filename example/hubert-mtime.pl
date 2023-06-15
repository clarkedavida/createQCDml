#!/usr/bin/perl -w
#
#  Print current time (if no argument) or mtime of file given as argument
#  in format suitable for QCDml Schemata

#  hs 18.3.2022
#
################################################################################
use POSIX qw(strftime);

if ( ! @ARGV ) {
    my $t = time();
    show_timestamp($t) 
}
else {
    my $f = shift;
    my @fstat = stat($f);
    show_timestamp($fstat[9]);
}

sub show_timestamp {
    # my ($ss,$mm,$hh,$dd,$mon,$yy);
    # ($ss,$mm,$hh,$dd,$mon,$yy) = localtime($t);
    # printf "%04d-%02d-%02dT%02d:%02d:%02d", $yy+1900, $mon+1, $dd, $hh, $mm, $ss; 
    my $str = strftime "%Y-%m-%dT%H:%M:%S%z", localtime(shift);
    $str =~ s/00$/:00/;
    print $str;
}
