#!/usr/bin/env python

# https://adventofcode.com/2022/day/14

from dataclasses import dataclass
import fileinput

"""
simulate sand falling

when a piece of sand falls past the lowest point of the input,
it is into the abyss, so end simulation here
"""

SAND_AT_REST = 'o'
AIR = '.'
ROCK = '#'

INCOMING_SAND_POSITION = (500, 0)

@dataclass
class Cave:
    rocks: set[tuple[int, int]]
    fallen_sand: set[tuple[int, int]]

def make_cave(lines: list[str]) -> tuple[Cave, int]:
    """
    Return a Cave and the depth of the given rocks.  The cave is artificially deeper:

    After adding rocks from the input, add one more row of rocks that are two
    rows below the last rock of the input, and that is is at least "depth" wider
    on each side than the bounds of the input.  This is to give somewhere for
    sand to land on when it falls "into the abyss" which will stop the
    simulation.
    """

    # cave uses sets because start/end of pairs of lines can have duplicate rocks
    cave = Cave(set(), set())

    for line in lines:
        coordinate_pairs = line.split(' -> ')

        for i, coordinate_pair in enumerate(coordinate_pairs):
            # so that we can look at pairs
            if i == 0:
                continue

            previous_coordinate_pair = coordinate_pairs[i - 1]
            previous_x = int(previous_coordinate_pair.split(',')[0])
            previous_y = int(previous_coordinate_pair.split(',')[1])
            x = int(coordinate_pair.split(',')[0])
            y = int(coordinate_pair.split(',')[1])

            if previous_x == x:
                # vertical line
                min_y = min(previous_y, y)
                max_y = max(previous_y, y)
                for y in range(min_y, max_y + 1):
                    cave.rocks.add((x, y))
            elif previous_y == y:
                # horizontal line
                min_x = min(previous_x, x)
                max_x = max(previous_x, x)
                for x in range(min_x, max_x + 1):
                    cave.rocks.add((x, y))
            else:
                raise Exception(f"line from {previous_coordinate_pair} to {coordinate_pair} looks wrong")

    # find depth of the given rocks
    actual_depth = max(y for _, y in cave.rocks)

    min_x = min(x for x, _ in cave.rocks)
    max_x = max(x for x, _ in cave.rocks)

    for x in range(min_x - actual_depth - 2, max_x + actual_depth + 3):
        cave.rocks.add((x, actual_depth + 2))

    return cave, actual_depth

def insert_sand(cave: Cave, stop_at_depth: int) -> None:
    """
    Insert a piece of sand and simulate it falling.  

    If stop_at_depth is not None, return True if the sand "falls into the abyss"
    lower than the stop_at_depth

    If stop_at_depth is None, return True once sand reaches the input height
    """

    falling_sand = INCOMING_SAND_POSITION

    while True:
        # update position of falling sand and learn if it
        new_position = cave_simulation_step(cave, falling_sand)

        if new_position == falling_sand:
            # sand has become stationary
            cave.fallen_sand.add(falling_sand)
            break
        else:
            falling_sand = new_position

    if (stop_at_depth is not None 
        and falling_sand[1] > stop_at_depth):
            # first one fell below the given rocks
            print(f"part one: {len(cave.fallen_sand)}")
            return True

    if falling_sand[1] == 0:
        # it reached the input height
        print(f"part two: {len(cave.fallen_sand)}")
        return True

    return False

def cave_simulation_step(cave: Cave, falling_sand: tuple[int, int]) -> tuple[int, int]:
    """
    Simulate one step of sand falling.  Return the updated position of the falling sand,
    which is equal to the input if it has become stationary.
    """
    possible_new_positions = [
        (falling_sand[0], falling_sand[1] + 1),
        (falling_sand[0] - 1, falling_sand[1] + 1),
        (falling_sand[0] + 1, falling_sand[1] + 1)
    ]

    for possible_new_position in possible_new_positions:
        if (possible_new_position not in cave.rocks 
            and possible_new_position not in cave.fallen_sand):
            return possible_new_position
        
    return falling_sand


def print_cave(cave: Cave) -> None:
    min_x = min(x for x, _ in cave.rocks)
    max_x = max(x for x, _ in cave.rocks)
    min_y = 0
    max_y = max(y for _, y in cave.rocks)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in cave.rocks:
                print(ROCK, end='')
            elif (x, y) in cave.fallen_sand:
                print(SAND_AT_REST, end='')
            else:
                print(AIR, end='')
        print()
    print()

lines = [line.strip() for line in fileinput.input()]
cave, actual_depth = make_cave(lines)

# use this twice, first to print part one then to continue for part two
while not insert_sand(cave, actual_depth):
    pass

while not insert_sand(cave, None):
    pass

