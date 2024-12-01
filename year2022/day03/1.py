#!/usr/bin/env python

# https://adventofcode.com/2022/day/3

import fileinput

def letter_value(letter):
    return (ord(letter) - ord('a') + 1) % 58

lines = [line.strip() for line in fileinput.input()]

values = []

for line in lines:
    midpoint = len(line) // 2
    left_half = set(line[:midpoint])
    right_half = set(line[midpoint:])

    # assume there's only one thing in the intersection (per problem statement)
    common_letter = (left_half & right_half).pop()

    values.append(letter_value(common_letter))

print(sum(values))
