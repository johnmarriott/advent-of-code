#!/usr/bin/env python
"""
Advent of Code - 2025 Day 3, Part 1
https://adventofcode.com/2025/day/3
"""

import fileinput

lines = [line.strip() for line in fileinput.input()]

sum_values = 0

for line in lines:
    values = list(map(int, list(line)))

    # tens digit is the max value of all but the last digit
    # (leave space for the ones digit at the end)
    tens_digit_value = max(values[0:-1])

    # index of the tens digit is the first occurrence of tens_digit_value
    tens_digit_index = values.index(tens_digit_value)

    # ones digit is the max value after the tens digit index
    ones_digit_value = max(values[tens_digit_index + 1:])

    sum_values += tens_digit_value * 10 + ones_digit_value

print(sum_values)