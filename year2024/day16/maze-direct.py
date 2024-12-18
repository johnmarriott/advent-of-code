#!/usr/bin/env python

""" 
build a directed networkx graph, where each cell has four vertices, one for each
direction and with weight 1000 between them, and edges between adjacent cells
with weight 1

use it to find the shortest paths to solve the puzzles

this one creates the graph directly, instead of parsing into data structures first.  This is
about 20% faster, but both are about 1s for this problem's input
"""


from enum import Enum
import fileinput

import networkx as nx


WALL = "#"
START = "S"
END = "E"

class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

def vertex_name(row: int, col: int, direction: Direction) -> str:
    return f"({row},{col})-{direction}"

def vertex_name_to_coordinates(vertex_name: str) -> str:
    """strip the direction from a vertex name, i.e., (1,2)-Direction.NORTH -> (1,2)"""
    return vertex_name.split("-")[0]

def find_start(field: list[list[str]]) -> str:
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == START:
                # find the vertex that's here, facing east
                return vertex_name(i, j, Direction.EAST)

def find_ends(field: list[list[str]]) -> list[str]:
    ends = []
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == END:
                # find any vertex at this position
                for direction in Direction:
                    ends.append(vertex_name(i, j, direction))

    return ends

def field_to_graph(field: list[list[str]]) -> nx.DiGraph:
    G = nx.DiGraph()

    # add all vertices with turns but not edges between adjacent cells    
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == WALL:
                continue

            # add edges to neighbors of this cell
            for direction in Direction:
                if field[i + direction.value[0]][j + direction.value[1]] != WALL:
                    G.add_edge(
                        vertex_name(i, j, direction), 
                        vertex_name(i + direction.value[0], j + direction.value[1], direction), 
                        weight=1
                    )

            # add edges for 90º turns, internal to this cell
            G.add_edge(vertex_name(i, j, Direction.NORTH), vertex_name(i, j, Direction.EAST), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.NORTH), vertex_name(i, j, Direction.WEST), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.SOUTH), vertex_name(i, j, Direction.EAST), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.SOUTH), vertex_name(i, j, Direction.WEST), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.EAST), vertex_name(i, j, Direction.NORTH), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.EAST), vertex_name(i, j, Direction.SOUTH), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.WEST), vertex_name(i, j, Direction.NORTH), weight=1000)
            G.add_edge(vertex_name(i, j, Direction.WEST), vertex_name(i, j, Direction.SOUTH), weight=1000)

    return G

field = [list(line.strip()) for line in fileinput.input()]
G = field_to_graph(field)
start = find_start(field)
ends = find_ends(field)

shortest_path_weight = float("inf")
for end in ends:
    path = nx.shortest_path(G, source=str(start), target=str(end), weight="weight")
    path_weight = nx.path_weight(G, path, weight="weight")

    if path_weight < shortest_path_weight:
        shortest_path_weight = path_weight

print(f"part one: {shortest_path_weight}")

sitting_spots = set()

for end in ends:
    shortest_paths = nx.all_shortest_paths(G, source=str(start), target=str(end), weight="weight")

    for path in shortest_paths:
        path_weight = nx.path_weight(G, path, weight="weight")

        if path_weight == shortest_path_weight:
            path_positions = set(vertex_name_to_coordinates(vertex) for vertex in path)
            sitting_spots = sitting_spots.union(path_positions)

print(f"part two: {len(sitting_spots)}")
