#!/usr/bin/env python

import fileinput


lines = [line.strip() for line in fileinput.input()]

fresh_ingredient_id_ranges = list()
available_ingredient_ids = set()
n_available_fresh_ingredients = 0

# file starts with fresh ingredient id ranges, then a blank line, 
# then available ingredient ids
reading_ids = True
for line in lines:
    if line == "":
        reading_ids = False
        continue

    if reading_ids:
        line_parts = line.split("-")

        start_id = int(line_parts[0])
        end_id = int(line_parts[1])

        fresh_ingredient_id_ranges.append((start_id, end_id))

    else: # reading available ingredient ids
        ingredient_id = int(line)
        available_ingredient_ids.add(ingredient_id)

# check which of the ingredient ids are fresh
for ingredient_id in available_ingredient_ids:
    for start_id, end_id in fresh_ingredient_id_ranges:
        if start_id <= ingredient_id <= end_id:
            n_available_fresh_ingredients += 1
            break

print(n_available_fresh_ingredients)
