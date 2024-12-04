#!/usr/bin/env python

import fileinput

offsets = [
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
]

lines = [line.strip() for line in fileinput.input()]

# pad the input with dots
letters = ['.' * (len(lines[0]) + 2)]
for line in lines:
    letters.append('.' + line + '.')
letters.append('.' * (len(lines[0]) + 2))

n_xmas = 0

for i in range(len(letters)):
    for j in range(len(letters[0])):
        for offset in offsets:
            is_xmas = 1
            for k in range(4):
                # are the letters XMAS in a straight line in this offset direction?
                if letters[i + k * offset[0]][j + k * offset[1]] != "XMAS"[k]:
                    is_xmas = 0
                    break

            n_xmas += is_xmas

print(n_xmas)
