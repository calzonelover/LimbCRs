#!/usr/bin/perl

# Convert Dictionary file to header file
# Usage: dict2c tdict.txt > tdict.h
# By: vuthi@ctrl.titech.ac.jp

# This doesn't seem to work anymore (MAA 19/12/2003) - line 18 gives problems

print <<ENDEND;
/* This file is machine-generated by a perl script. */
/* Do not modify unless you maintain the word order. */

unsigned char *wordptr[]={
ENDEND
$c = 0;
while(<>) {
  chop;
  $i = length($_);
  print ",\n" if $c;
  printf "\"\\x%02X%s\"", $i, $_;
  $c++;
}

print <<ENDEND;
};
int numword = $c;

ENDEND

