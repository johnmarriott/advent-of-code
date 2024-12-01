#!/usr/bin/env python

import fileinput

lines = [line.strip() for line in fileinput.input()]

left_numbers = []
right_numbers = []

for line in lines:
    left, right = line.split()
    left_numbers.append(int(left))
    right_numbers.append(int(right))

left_numbers.sort()
right_numbers.sort()

total_distance = sum([
    abs(left_numbers[i] - right_numbers[i]) 
    for i 
    in range(len(left_numbers))
])

similarity = sum([
    left_number * right_numbers.count(left_number)
    for left_number
    in left_numbers
])

print(f"part one: {total_distance}")
print(f"part two: {similarity}")