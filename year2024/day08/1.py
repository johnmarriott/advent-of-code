#!/usr/bin/env python

import fileinput
from itertools import combinations

OPEN_CELL = "."

## read input to locate antennas

lines = [line.strip() for line in fileinput.input()]

# dict of antenna frequency to list of antenna coordinates
antennas: dict[str, list[tuple[int, int]]] = {}

for i, row in enumerate(lines):
    for j, cell in enumerate(row):
        if cell != OPEN_CELL:
            if cell in antennas:
                antennas[cell].append((i, j))
            else:
                antennas[cell] = [(i, j)]

## find antinodes 
# looking at a pair of antennas from a to b, antinodes are a step behind a or
# ahead of b.  Keep the antinodes that are within the given space

n_rows = len(lines)
n_cols = len(lines[0])
antinodes = set()

for frequency in antennas:
    if len(antennas[frequency]) < 2:
        continue

    # all pairs of antennas of this frequency
    for a, b in combinations(antennas[frequency], 2):
        x_step = a[0] - b[0]
        y_step = a[1] - b[1]

        antinode_behind_a = (a[0] + x_step, a[1] + y_step)
        antinode_ahead_of_b = (b[0] - x_step, b[1] - y_step)

        if 0 <= antinode_behind_a[0] < n_rows and 0 <= antinode_behind_a[1] < n_cols:
            antinodes.add(antinode_behind_a)

        if 0 <= antinode_ahead_of_b[0] < n_rows and 0 <= antinode_ahead_of_b[1] < n_cols:
            antinodes.add(antinode_ahead_of_b)

print(len(antinodes))
