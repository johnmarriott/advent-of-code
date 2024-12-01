#!/usr/bin/env python

import fileinput
import math

tree_heights = []

for line in fileinput.input():
    row = [int(x) for x in line.strip()]
    tree_heights.append(row)

tree_scenic_scores = [[0 for _ in range(len(tree_heights[0]))] for _ in range(len(tree_heights))]

# find the scenic scores, skipping the first and last rows and columns
# since they always have a score of zero (border trees always have a
# zero in the product)
for i in range(len(tree_heights)):
    if i == 0 or i == len(tree_heights) - 1:
        continue

    for j in range(len(tree_heights[0])):
        if j == 0 or j == len(tree_heights[0]) - 1:
            continue

        tree_height = tree_heights[i][j]

        # reverse the heights above and to the left so that
        # all four lists are ordered by proximity to this tree
        heights_to_left = list(reversed([tree_heights[i][k] for k in range(j)]))
        heights_to_right = [tree_heights[i][k] for k in range(j + 1, len(tree_heights[0]))]
        heights_above = list(reversed([tree_heights[k][j] for k in range(i)]))
        heights_below = [tree_heights[k][j] for k in range(i + 1, len(tree_heights))]

        scores = []

        for heights in [heights_to_left, heights_to_right, heights_above, heights_below]:
            score = 0
            for height in heights:
                score += 1
                if height >= tree_height:
                    break
            scores.append(score)

        tree_scenic_scores[i][j] = math.prod(scores)

print(max([max(row) for row in tree_scenic_scores]))