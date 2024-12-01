#!/usr/bin/env python

# https://adventofcode.com/2022/day/3#part2

import fileinput

def letter_value(letter):
    return (ord(letter) - ord('a') + 1) % 58

lines = [line.strip() for line in fileinput.input()]

values = []

for offset in range(0, len(lines), 3):
    first_letters = set(lines[offset])
    second_letters = set(lines[offset + 1])
    third_letters = set(lines[offset + 2])

    common_letter = (first_letters & second_letters & third_letters).pop()

    values.append(letter_value(common_letter))

print(sum(values))
