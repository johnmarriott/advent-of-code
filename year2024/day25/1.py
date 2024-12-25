#!/usr/bin/env python

import fileinput

import numpy as np


lines: list[str] = [line.strip() for line in fileinput.input()]
# put a blank line at the start so all keys/locks are preceded by that
lines.insert(0, "")

locks = []
keys = []

for i, line in enumerate(lines):
    if line == "":
        object = []

        for col in range(5):
            column_count = 0
            for row in range(i+2, i+7):
                if lines[row][col] == "#":
                    column_count += 1

            object.append(column_count)

        # next line is '#####' or '.....'
        if lines[i+1].startswith("#"):
            locks.append(np.array(object))
        else:
            keys.append(np.array(object))

n_matching_locks_and_keys = 0
for lock in locks:
    for key in keys:
        if all(lock + key < [6, 6, 6, 6, 6]):
            n_matching_locks_and_keys += 1

print(n_matching_locks_and_keys)
