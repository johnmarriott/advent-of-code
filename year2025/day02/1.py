#!/usr/bin/env python
"""
Advent of Code - 2025 Day 2, Part 1
https://adventofcode.com/2025/day/2
"""


import fileinput


def is_invalid(n: int) -> bool:
    """
    Return whether the number n is invalid, i.e., whether its string of digits
    consists of the same substring repeated twice.

    >>> is_invalid(1212)
    True
    >>> is_invalid(1234)
    False
    """
    word = str(n)
    half_length = len(word) // 2
    return word[:half_length] == word[half_length:]


def main():
    lines = [line.strip() for line in fileinput.input()]

    sum_invalid = 0

    for interval in lines[0].split(','):
        start, end = map(int, interval.split('-'))

        for n in range(start, end + 1):
            if is_invalid(n):
                sum_invalid += n

    print(sum_invalid)


if __name__ == "__main__":
    main()
