#!/usr/bin/env python

"""
express each rock shape as a set of offsets from the bottom left corner of the rock's bounding box

coordinate system has the floor at (0, 0) to (6, 0), and rocks rest at positive y-coordinates

"""

import fileinput

MAX_ROCKS = 2022
CAVE_WIDTH = 7

rocks = ('-', '+', 'J', '|', '.')
jets = [line.strip() for line in fileinput.input()][0]

rock_shape_offsets = {
    '-': [(0, 0), (1, 0), (2, 0), (3, 0)],
    '+': [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    'J': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    '|': [(0, 0), (0, 1), (0, 2), (0, 3)],
    '.': [(0, 0), (1, 0), (0, 1), (1, 1)]
}

cave = [(x, 0) for x in range(CAVE_WIDTH)]
jet_index = 0

def cave_rocks_height(cave: list[tuple[int, int]]) -> int:
    return max(y for x, y in cave)

def print_cave(cave: list[tuple[int, int]], falling_rock: list[tuple[int, int]]):
    return
    max_height = max(cave_rocks_height(cave), max(y for x, y in falling_rock))

    for y in range(max_height, 0, -1):
        print("|", end="")
        for x in range(CAVE_WIDTH):
            if (x, y) in cave:
                print("#", end="")
            elif (x, y) in falling_rock:
                print("@", end="")
            else:
                print(".", end="")
        print("|")

    print("+", end="")
    print("-" * CAVE_WIDTH, end="")
    print("+")
    print()
        
for i in range(MAX_ROCKS):
    rock = rocks[i % len(rocks)]
    print(f"{i:03d}: adding rock {rock}")

    # Each rock appears so that its left edge is two units away from the left wall 
    # and its bottom edge is three units above the highest rock in the room (or the 
    # floor, if there isn't one).
    rocks_height = cave_rocks_height(cave)
    rock_coordinates = [
        (offset[0] + 2, offset[1] + rocks_height + 4) 
        for offset 
        in rock_shape_offsets[rock]
    ]

    rock_has_settled = False
    while not rock_has_settled:
        print_cave(cave, rock_coordinates)

        # let the jet blow the rock
        jet = jets[jet_index % len(jets)]
        jet_index += 1

        if jet == "<":
            if not (
                any(x == 0 for x, y in rock_coordinates) # rock would hit left wall
                or any((x - 1, y) in cave for x, y in rock_coordinates) # rock would hit settled rock
            ):
                rock_coordinates = [(x - 1, y) for x, y in rock_coordinates]
        else: # jet == ">"
            if not (
                any(x == (CAVE_WIDTH - 1) for x, y in rock_coordinates) # rock would hit right wall
                or any((x + 1, y) in cave for x, y in rock_coordinates) # rock would hit settled rock
            ):
                rock_coordinates = [(x + 1, y) for x, y in rock_coordinates]

        print_cave(cave, rock_coordinates)

        if any((x, y - 1) in cave for x, y in rock_coordinates):
            rock_has_settled = True
        else:
            rock_coordinates = [(x, y - 1) for x, y in rock_coordinates]

        print_cave(cave, rock_coordinates)
        #input()

    cave += rock_coordinates

    print(f"rock {i} settled, max height is now {cave_rocks_height(cave)}")