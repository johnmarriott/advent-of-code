#!/usr/bin/env python
"""
Advent of Code 2025 - Day 7, Part 1
https://adventofcode.com/2025/day/7
"""


import fileinput

from constants import SPLITTER, START


lines = [line.strip() for line in fileinput.input()]

beam_positions = [x == START for x in lines[0]]

n_splits = 0
for line in lines:
    for i, cell in enumerate(line):
        if (
            cell == SPLITTER 
            and beam_positions[i]
        ):
            n_splits += 1
            beam_positions[i - 1] = True
            beam_positions[i + 1] = True
            beam_positions[i] = False

print(n_splits)
