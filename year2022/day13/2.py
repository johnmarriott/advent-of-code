#!/usr/bin/env python

# https://adventofcode.com/2022/day/13#part2

"""
use part one as-is to sort the packets
"""

import fileinput
from functools import cmp_to_key
from json import loads
import math

from part1 import compare

lines = [line.strip() for line in fileinput.input() if len(line.strip()) > 0]
lines.append('[[2]]')
lines.append('[[6]]')

packets = [loads(line) for line in lines]

packets_sorted = sorted(packets, key=cmp_to_key(compare))

divider_indices = [
    (i + 1) 
    for i in range(len(packets_sorted)) 
    if packets_sorted[i] == [[2]] or packets_sorted[i] == [[6]]
]

print(math.prod(divider_indices))