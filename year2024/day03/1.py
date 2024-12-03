#!/usr/bin/env python

import fileinput
import re

# concatenate input to one line
lines = [line.strip() for line in fileinput.input()]
line = [''.join(lines)][0]

sum = 0

mul_parts = line.split('mul')

for part in mul_parts:
    # chop of anything after the first ')'
    part = re.sub(r"\).*", ")", part)

    if re.match(r"^\(\d+,\d+\)$", part):
        a, b = part[1:-1].split(',')
        sum += int(a) * int(b)

print(sum)