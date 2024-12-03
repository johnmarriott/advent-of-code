#!/usr/bin/env python

import fileinput
import re

def mul_value(block):
    """The sum of the valid multiplications in a do/don't block of the input"""
    block_sum = 0
    mul_parts = block.split('mul')

    for part in mul_parts:
        # chop of anything after the first ')'
        part = re.sub(r"\).*", ")", part)

        if re.match(r"^\(\d+,\d+\)$", part):
            a, b = part[1:-1].split(',')
            block_sum += int(a) * int(b)

    return block_sum

# concatenate input to one line
lines = [line.strip() for line in fileinput.input()]
line = [''.join(lines)][0]

sum = 0
count_block = True # first block is implicitly a 'do()'

remaining_input = line
while len(remaining_input) > 0:
    if remaining_input.startswith('do()'):
        count_block = True
        remaining_input = remaining_input[4:]
    elif remaining_input.startswith("don't()"):
        count_block = False
        remaining_input = remaining_input[8:]
    # else this is the first block, already set to count_block = True

    block = re.match(r"^(.*?)(do\(\)|don't\(\)|$)", remaining_input).group(1)
    remaining_input = remaining_input[len(block):]

    if count_block:
        sum += mul_value(block)

print(sum)





