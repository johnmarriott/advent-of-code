#!/usr/bin/env python

"""
instead of counting perimeter edges, track points that this cell contributes to
tracing the perimeter of the region.  In the A region here, the top left A has three 
points for its top left, top right, and bottom left.

  AA
  AA

These perimeter points are stored with the direction for the side of the cell.

for the region, throw out any vertices that are doubled up when counting this
way; those are points not on the endpoints of the face, e.g.

  [ A1 ][ A2 ]

along the top, A1's right top point is shared with A2's left top point, and this
get counted twice => it is not a vertex of the region's polygon

once a region is pared down to its essential vertices, the number of edges is
equal to the number of vertices
"""

import fileinput

from direction_2d import directions

EMPTY = "."

def identify_region(field, perimeter_points, i, j, region_indices: set) -> tuple[int, int]:
    plant = field[i][j]
    field[i][j] = EMPTY
    region_indices.add((i, j))

    for direction in directions.values():
        neighbor_coordinates = (i + direction.offset[0], j + direction.offset[1])
        neighbor = field[neighbor_coordinates[0]][neighbor_coordinates[1]]

        if neighbor == plant:
            neighbor_region_indices = identify_region(field, perimeter_points, neighbor_coordinates[0], neighbor_coordinates[1], region_indices)
            region_indices.update(neighbor_region_indices)

    return region_indices

lines = [line.strip() for line in fileinput.input()]

# pad input with dots
field = []
field.append([EMPTY] * (len(lines[0]) + 2))
for line in lines:
    field.append([EMPTY] + list(line) + [EMPTY])
field.append([EMPTY] * (len(lines[0]) + 2))

# if a plant is at (i, j) and its side to the {direction} is not in this plant's
# region, then these are the offsets to the points that this cell contributes to
# that region's perimenter (including points that aren't vertices of the
# region's polygon)
perimeter_point_offsets = {
    "north": [(0, 0), (0, 1)],
    "east": [(0, 1), (1, 1)],
    "south": [(1, 0), (1, 1)],
    "west": [(0, 0), (1, 0)]
}

# do a first pass to store the perimeter points of each 
# plant in the field.  A plant contributes perimeter points
# in a direction if there's not another of the same plant in that 
# position.  A plant is in the center of a cell.  In the, e.g., north
# direction, a plant out add two points with the same row index, different
# column index.
perimeter_points = [[None] * len(field[0]) for _ in range(len(field))]
for i in range(1, len(field) - 1):
    for j in range(1, len(field[0]) - 1):
        plant = field[i][j]

        if plant == EMPTY:
            continue

        plant_perimeter_points = set()
        for direction in directions.keys():
            neighbor = field[i + directions[direction].offset[0]][j + directions[direction].offset[1]]
            if neighbor != plant:
                for offset in perimeter_point_offsets[direction]:
                    plant_perimeter_points.add((direction, i + offset[0], j + offset[1]))

        perimeter_points[i][j] = plant_perimeter_points

# find out the plant indices of the regions of plants
regions = {}
for i in range(1, len(field) - 1):
    for j in range(1, len(field[0]) - 1):
        plant = field[i][j]

        if plant == EMPTY:
            continue

        regions[(i, j)] = identify_region(field, perimeter_points, i, j, set())
                   
region_prices = []
for region in regions.keys():
    region_indices = regions[region]
    area = len(region_indices)

    # the region's perimeter vertices are found by taking all of
    # the perimeter points of the plants in the region, and then
    # discarding points from the plants in the region that are
    # shared by neighboring plants in the region
    # 
    # that is, we do want to get rid of the shared point of 1+2 here
    # but not the shared point of 5+6 here
    #
    #  1234
    #  56 7
    #  8 9A
    #  BCDE
    #
    # the perimeter points are stored with originating direction, so 
    # first discard the points shared between neighboring plants in the same
    # direction.  This leaves two points at every vertex, e.g., a ⌝ has a
    # has a north and easy copy. 

    region_points = []
    for (i, j) in region_indices:
        for point in perimeter_points[i][j]:
            point_is_shared_with_a_neighbor = False
            for direction in directions.keys():
                neighbor_indices = (i + directions[direction].offset[0], j + directions[direction].offset[1])
                if neighbor_indices in region_indices:
                    if point in perimeter_points[neighbor_indices[0]][neighbor_indices[1]]:
                        point_is_shared_with_a_neighbor = True
                        break
            
            if not point_is_shared_with_a_neighbor:
                region_points.append(point[1:])

    # divide by two because each vertex is counted from two directions
    region_prices.append(int(len(region_points) * area / 2))

print(sum(region_prices))
