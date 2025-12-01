#!/usr/bin/env python

# https://adventofcode.com/2025/day/1#part2

import fileinput

from constants import INITIAL_DIAL_POSITION, DIAL_SIZE


lines = [line.strip() for line in fileinput.input()]

dial_position = INITIAL_DIAL_POSITION
n_zero_positions = 0

for line in lines:
    amount = int(line[1:])

    if amount > DIAL_SIZE:
        n_zero_positions += amount // DIAL_SIZE
        amount = amount % DIAL_SIZE

    if line.startswith("L"):
        if amount - dial_position >= 0 and dial_position != 0:
            n_zero_positions += 1

        dial_position = (dial_position - amount) % DIAL_SIZE
    else:
        if dial_position + amount >= DIAL_SIZE:
            n_zero_positions += 1
        
        dial_position = (dial_position + amount) % DIAL_SIZE

print(n_zero_positions)