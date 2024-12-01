#!/usr/bin/perl

use List::Util qw( sum max );

$input = join("", <STDIN>);
@parts = split(/\n\n/, $input);

@sums; 
foreach $part (@parts) {
	$sum = 0;
	map { $sum += $_ } split(/\n/, $part);
	push(@sums, $sum);
}

$max_sum = max(@sums);
$sum_top_three = sum((sort {$b <=> $a} @sums)[0 .. 2]);

print("part one: $max_sum\n");

print("part two: $sum_top_three\n");
