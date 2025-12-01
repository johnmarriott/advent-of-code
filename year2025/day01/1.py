#!/usr/bin/env python

# https://adventofcode.com/2025/day/1

import fileinput

from constants import INITIAL_DIAL_POSITION, DIAL_SIZE


lines = [line.strip() for line in fileinput.input()]

dial_position = INITIAL_DIAL_POSITION
n_zero_positions = 0

for line in lines:
    amount = int(line[1:])

    if line.startswith("L"):
        dial_position = (dial_position - amount) % DIAL_SIZE
    else:
        dial_position = (dial_position + amount) % DIAL_SIZE

    if dial_position == 0:
        n_zero_positions += 1

print(n_zero_positions)