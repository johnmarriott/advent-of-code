#!/usr/bin/env python

import fileinput

import networkx as nx

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

# for each face of each cube, if the next spot over from a face is open and has
# a path to the outside (use the coordinate (-1, -1, -1) for this since each
# given coordinate is positive), then this face contributes 1 to the surface area

# do this by constructing a graph of the space, where if a space doesn't contain
# a cube then it's a vertex in the graph, and this vertex has nondirected edges
# to any orthogonally adjacent vertices

max_x = max(cube[0] for cube in cube_coordinates) + 1
max_y = max(cube[1] for cube in cube_coordinates) + 1
max_z = max(cube[2] for cube in cube_coordinates) + 1

graph_of_empty_space: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {}

G = nx.Graph()
for x in range(-1, max_x + 1, 1):
    for y in range(-1, max_y + 1, 1):
        for z in range(-1, max_z + 1, 1):
            vertex = (x, y, z)
            if vertex in cube_coordinates:
                continue

            G.add_node(vertex)

            for offset in neighboring_cube_offsets:
                neighbor = (x + offset[0], y + offset[1], z + offset[2])
                if not neighbor in cube_coordinates:
                    G.add_edge(vertex, neighbor)

exterior_vertex = (-1, -1, -1)

surface_area = 0
for cube in cube_coordinates:
    x, y, z = cube

    for offset in neighboring_cube_offsets:
        neighbor = (x + offset[0], y + offset[1], z + offset[2])

        if neighbor in cube_coordinates:
            continue

        if nx.has_path(G, neighbor, exterior_vertex):
            surface_area += 1

print(surface_area)
