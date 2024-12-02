#!/usr/bin/env python

import fileinput

lines = [line.strip() for line in fileinput.input()]

def is_report_safe(numbers):
    """
    [A] report only counts as safe if both of the following are true:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    """
    # must be monotonic
    if not (numbers == sorted(numbers)
            or numbers == sorted(numbers, reverse=True)):
        return False

    differences = [abs(numbers[i + 1] - numbers[i]) for i in range(len(numbers) - 1)]

    # must be strictly monotonic
    if any([d == 0 for d in differences]):
        return False

    # max diff must be <= 3
    return max(differences) <= 3

totally_safe_lines = 0
kinda_safe_lines = 0

for line in lines:
    numbers = list(map(int, line.split()))

    if is_report_safe(numbers):
        totally_safe_lines += 1
        continue

    for i in range(len(numbers)):
        if is_report_safe(numbers[:i] + numbers[i + 1:]):
            kinda_safe_lines += 1
            break

print(f"part one: {totally_safe_lines}")
print(f"part two: {totally_safe_lines + kinda_safe_lines}")
 