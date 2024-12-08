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

n_rows = len(lines)
n_cols = len(lines[0])
antinodes = set()

## find antinodes 

for frequency in antennas:
    if len(antennas[frequency]) < 2:
        continue

    # all pairs of antennas of this frequency
    for a, b in combinations(antennas[frequency], 2):
        x_step = a[0] - b[0]
        y_step = a[1] - b[1]

        # antinodes behind a, starting at a
        steps = 0
        while True:
            antinode_behind_a = (a[0] + steps * x_step, a[1] + steps * y_step)
            if 0 <= antinode_behind_a[0] < n_rows and 0 <= antinode_behind_a[1] < n_cols:
                antinodes.add(antinode_behind_a)
            else:
                break
            steps += 1

        # antinodes ahead of b, starting at b
        steps = 0
        while True:
            antinode_ahead_of_b = (b[0] - steps * x_step, b[1] - steps * y_step)
            if 0 <= antinode_ahead_of_b[0] < n_rows and 0 <= antinode_ahead_of_b[1] < n_cols:
                antinodes.add(antinode_ahead_of_b)
            else:
                break
            steps += 1

print(len(antinodes))
