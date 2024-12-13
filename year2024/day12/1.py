#!/usr/bin/env python

import fileinput

from direction_2d import directions

EMPTY = "."

def quantify_region(field, perimeter_contributions, i, j) -> tuple[int, int]:
    """
    Return the area and perimeter for a region containing the plant at (i, j).
    Modifies `field` by emptying out plants as they are counted.
    """

    plant = field[i][j]
    field[i][j] = EMPTY

    area = 1 # self
    perimeter = perimeter_contributions[i][j]

    for direction in directions.values():
        neighbor_coordinates = (i + direction.offset[0], j + direction.offset[1])
        neighbor = field[neighbor_coordinates[0]][neighbor_coordinates[1]]

        if neighbor == plant:
            a, p = quantify_region(field, perimeter_contributions, neighbor_coordinates[0], neighbor_coordinates[1])
            area += a
            perimeter += p

    return area, perimeter

lines = [line.strip() for line in fileinput.input()]

# pad input with dots
field = []
field.append([EMPTY] * (len(lines[0]) + 2))
for line in lines:
    field.append([EMPTY] + list(line) + [EMPTY])
field.append([EMPTY] * (len(lines[0]) + 2))

# do a first pass to store the "perimeter contribution" of each 
# position in the field.  This is (4 - # of neighbors of each plant type)
perimeter_contributions = [[0] * len(field[0]) for _ in range(len(field))]

for i in range(1, len(field) - 1):
    for j in range(1, len(field[0]) - 1):
        plant = field[i][j]

        if plant == EMPTY:
            continue

        perimeter_contribution = 4
        for direction in directions.values():
            neighbor = field[i + direction.offset[0]][j + direction.offset[1]]
            if neighbor == plant:
                perimeter_contribution -= 1

        perimeter_contributions[i][j] = perimeter_contribution

# next do an area search, emptying out plants as they are added to the region
region_quantities = {}
for i in range(1, len(field) - 1):
    for j in range(1, len(field[0]) - 1):
        plant = field[i][j]

        if plant == EMPTY:
            continue

        region_quantities[(i, j)] = quantify_region(field, perimeter_contributions, i, j)
                   
print(sum([region_quantity[0] * region_quantity[1] for region_quantity in region_quantities.values()]))
