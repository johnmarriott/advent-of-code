#!/usr/bin/env python

# https://adventofcode.com/2022/day/10

import fileinput

lines = [line.strip() for line in fileinput.input()]
lines.extend(["noop"])

cycle = 0
value = 1
cycle_values = []

for line in lines:
    cycle += 1
    cycle_values.append(value)

    # nothing more needed for noop

    if line.startswith("addx"):
        cycle += 1
        cycle_values.append(value)
        value += int(line.split()[1]) # add occurs at end of cycle

sum = 0
for i in range(19, len(cycle_values), 40):
    strength = (i+1) * cycle_values[i]
    sum += strength
    print(f"{i+1}: {cycle_values[i]} → {strength}")

print(f"\nPart one: {sum}\n")

print("Part two:")
    
for i in range(len(cycle_values) - 1): # we added a noop
    column = i % 40

    if i % 40 == 0:
        print()

    if abs(column - cycle_values[i]) <= 1:
        print("#", end="")
    else:
        print(" ", end="")

print("\n")
