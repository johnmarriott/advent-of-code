#!/usr/bin/env python

import fileinput

from termcolor import colored

tree_heights = []

for line in fileinput.input():
    row = [int(x) for x in line.strip()]
    tree_heights.append(row)

trees_visible = [[0 for x in row] for row in tree_heights]

# make first and last rows visible
for i in range(len(tree_heights)):
    trees_visible[i][0] = 1
    trees_visible[i][len(tree_heights) - 1] = 1

# make first and last columns visible
for j in range(len(tree_heights[0])):
    trees_visible[0][j] = 1
    trees_visible[len(tree_heights[0]) - 1][j] = 1

# check if trees are visible, skipping first/last rows/columns
# since those are already known to be visible (and can avoid boundaries)
for i in range(len(tree_heights)):
    if i == 0 or i == len(tree_heights) - 1:
        continue

    for j in range(len(tree_heights[0])):
        if j == 0 or j == len(tree_heights[0]) - 1:
            continue

        tree_height = tree_heights[i][j]

        heights_to_left = [tree_heights[i][k] for k in range(j)]
        heights_to_right = [tree_heights[i][k] for k in range(j + 1, len(tree_heights[0]))]
        heights_above = [tree_heights[k][j] for k in range(i)]
        heights_below = [tree_heights[k][j] for k in range(i + 1, len(tree_heights))]

        if (
            all([height < tree_height for height in heights_to_left]) 
            or all([height < tree_height for height in heights_to_right]) 
            or all([height < tree_height for height in heights_above]) or 
            all([height < tree_height for height in heights_below])
        ):
            trees_visible[i][j] = 1

for i in range(len(tree_heights)):
    for j in range(len(tree_heights[0])):
        print(colored(tree_heights[i][j], "green" if trees_visible[i][j] else "white"), end='')
    print()

print()
print(sum(sum(row) for row in trees_visible))