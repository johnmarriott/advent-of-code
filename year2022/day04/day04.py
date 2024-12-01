#!/usr/bin/env python

import fileinput

lines = [line.strip() for line in fileinput.input()]

n_subset_pairs = 0
n_intersection_pairs = 0

for line in lines:
    elves = line.split(',')
    left_elf_start = elves[0].split('-')[0]
    left_elf_end = elves[0].split('-')[1]
    right_elf_start = elves[1].split('-')[0]
    right_elf_end = elves[1].split('-')[1]

    left_elf_assignment = set(range(int(left_elf_start), int(left_elf_end) + 1))
    right_elf_assignment = set(range(int(right_elf_start), int(right_elf_end) + 1))

    if left_elf_assignment.issubset(right_elf_assignment) or right_elf_assignment.issubset(left_elf_assignment):
        n_subset_pairs += 1

    if len(left_elf_assignment.intersection(right_elf_assignment)) > 0:
        n_intersection_pairs += 1

# part 1
print(n_subset_pairs)

# part 2
print(n_intersection_pairs)
