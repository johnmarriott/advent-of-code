#!/usr/bin/env python

import fileinput

MS = "MS"

lines = [line.strip() for line in fileinput.input()]

# we'll look for X-MAS rooted at the top left corners, so
# double pad the right and bottom with dots
letters = []
for line in lines:
    letters.append(line + '..')
letters.append('.' * (len(lines[0]) + 2))
letters.append('.' * (len(lines[0]) + 2))

n_xmas = 0

for i in range(len(letters) - 2):
    for j in range(len(letters[0]) - 2):
        top_left = letters[i][j]
        top_right = letters[i][j+2]
        middle = letters[i+1][j+1]
        bottom_left = letters[i+2][j]
        bottom_right = letters[i+2][j+2]

        if middle == "A":
            if top_left in MS and top_right in MS and bottom_left in MS and bottom_right in MS:
                if top_left != bottom_right and top_right != bottom_left:
                    n_xmas += 1
            
print(n_xmas)
