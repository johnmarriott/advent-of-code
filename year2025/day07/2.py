#!/usr/bin/env python
"""
Advent of Code 2025 - Day 7, Part 2
https://adventofcode.com/2025/day/7#part2
"""


import fileinput
import functools

from constants import SPLITTER, START


@functools.cache
def beam_paths(beam_position: int, line_index: int, lines: list[str]) -> int:
    """
    Given a current beam position and line index, returns how many
    different paths are possible from this position onward.
    """

    # base case - reached the bottom row, which is always all empty
    if line_index == len(lines):
        return 1

    line = lines[line_index]
    cell = line[beam_position]

    if cell == SPLITTER:
        left_paths = beam_paths(beam_position - 1, line_index + 1, lines)
        right_paths = beam_paths(beam_position + 1, line_index + 1, lines)
        return left_paths + right_paths
    else:
        return beam_paths(beam_position, line_index + 1, lines)


def main():
    lines = tuple(line.strip() for line in fileinput.input())
    beam_position = lines[0].index(START)

    print(beam_paths(beam_position, 1, lines))


if __name__ == "__main__":
    main()
