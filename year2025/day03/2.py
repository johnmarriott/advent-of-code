#!/usr/bin/env python
"""
Advent of Code - 2025 Day 3, Part 2
https://adventofcode.com/2025/day/3#part2
"""

import fileinput


def max_joltage(values: list[int], digits: int) -> int:
    """
    Return the maximum `digits`-digit number value that can be constructed from 
    an ordered subset of the digits in the input list `values`.

    Assumes that the `values` are all between 1 and 9 inclusive, and that the
    length of `values` is at least `digits`.

    >>> max_joltage([1, 2, 3, 4, 5], 2)
    45 
    >>> max_joltage([5, 3, 1, 4, 2], 2)
    54
    >>> max_joltage([1, 9, 8, 7, 6], 2)
    98
    """

    # where to look in the list of values for the next digit—after we start 
    # assigning digits, we can only look after those for the next digit
    starting_index = 0
    
    joltage = 0

    for d in reversed(range(digits)):
        if d > 0:
            # this place value is the max of the remaining values, up to the last d values
            # (leave space for the following places)
            place_value = max(values[starting_index : -d]) 

            place_index = values.index(place_value, starting_index)
            joltage += place_value * (10 ** d)
            starting_index = place_index + 1
        else:
            # last digit is the max of the remaining values
            joltage += max(values[starting_index:])

    return joltage


def main():
    lines = [line.strip() for line in fileinput.input()]

    sum_joltage_two_digit = 0
    sum_joltage_twelve_digit = 0

    for line in lines:
        sum_joltage_two_digit += max_joltage(list(map(int, list(line))), digits=2)
        sum_joltage_twelve_digit += max_joltage(list(map(int, list(line))), digits=12)

    print("part one:", sum_joltage_two_digit)
    print("part two:", sum_joltage_twelve_digit)


if __name__ == "__main__":
    main()
