#!/usr/bin/env python
""" 
Advent of Code 2025 - Day 9, Part 1
https://adventofcode.com/2025/day/9
"""


import fileinput
from itertools import combinations


lines = [line.strip() for line in fileinput.input()]
coordinates = [tuple(map(int, line.split(','))) for line in lines]

all_coordinate_pairs = combinations(coordinates, 2)

max_area = 0
for (x1, y1), (x2, y2) in all_coordinate_pairs:
    # pad each "center" out to the full box
    area = (1 + abs(x1 - x2)) * (1 + abs(y1 - y2))
    if area > max_area:
        max_area = area

print(max_area)
