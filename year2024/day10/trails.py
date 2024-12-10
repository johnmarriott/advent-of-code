#!/usr/bin/env python

import fileinput

import networkx as nx

neighbor_offsets = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

lines = [line.strip() for line in fileinput.input()]

# pad input with dots

field = [['.'] * (len(lines[0]) + 2)]
for line in lines:
    field.append(['.'] + list(line) + ['.'])
field.append(['.'] * (len(lines[0]) + 2))

G = nx.DiGraph()
zero_vertices = []
nine_vertices = []
for i in range(1, len(field) - 1):
    for j in range(1, len(field[0]) - 1):
        if field[i][j] == ".":
            continue

        vertex = (i, j)
        value = int(field[i][j])
        G.add_node(vertex)

        if value == 0:
            zero_vertices.append(vertex)

        if value == 9:
            nine_vertices.append(vertex)

        for neighbor_offset in neighbor_offsets:
            neighbor_vertex = (i + neighbor_offset[0], j + neighbor_offset[1])

            if field[neighbor_vertex[0]][neighbor_vertex[1]] != ".":
                neighbor_value = int(field[neighbor_vertex[0]][neighbor_vertex[1]])

                if neighbor_value == value + 1:
                    G.add_edge(vertex, neighbor_vertex)

zero_to_nine_pairs = []
n_zero_to_nine_distinct_paths = 0
for zero_vertex in zero_vertices:
    for nine_vertex in nine_vertices:
        n = len(list(nx.all_simple_paths(G, zero_vertex, nine_vertex)))
        n_zero_to_nine_distinct_paths += n
        
        if n > 0:
            zero_to_nine_pairs.append((zero_vertex, nine_vertex))

print(f"part one: {len(zero_to_nine_pairs)}")
print(f"part two: {n_zero_to_nine_distinct_paths}")
