#!/usr/bin/env python

import fileinput

neighboring_cube_offsets = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]

lines = [line.strip() for line in fileinput.input()]

cube_coordinates = []

for line in lines:
    x, y, z = map(int, line.split(","))
    cube_coordinates.append((x, y, z))

surface_areas = []

# each cube contributes (6 - number_of_neighbors) to the surface area
for cube in cube_coordinates:
    x, y, z = cube
    surface_area = 6

    for offset in neighboring_cube_offsets:
        neighbor = (x + offset[0], y + offset[1], z + offset[2])
        if neighbor in cube_coordinates:
            surface_area -= 1

    surface_areas.append(surface_area)

print(sum(surface_areas))
