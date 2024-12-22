#!/usr/bin/env python

"""
https://adventofcode.com/2024/day/20#part1

brute force adding each non-border wall as a viable path to the graph,
testing it, and removing it

this is slow: runs in about a minute for the problem input
"""

from collections import defaultdict
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

def find_start(field: list[list[str]]) -> tuple[int, int]:
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == START:
                return (i, j)

def find_end(field: list[list[str]]) -> tuple[int, int]:
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == END:
                return (i, j)
            
def add_edges_to_neighbors_of(G: nx.Graph, i: int, j: int, field: list[list[str]]) -> None:
    """
    Add edges to the neighbors of the vertex at (i, j) in the field.
    """
    for direction in Direction:
        if field[i + direction.value[0]][j + direction.value[1]] != WALL:
            G.add_edge(
                (i, j),
                (i + direction.value[0], j + direction.value[1]),
                weight=1
            )

def field_to_graph(field: list[list[str]]) -> nx.Graph:
    G = nx.Graph()

    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == WALL:
                continue

            add_edges_to_neighbors_of(G, i, j, field)

    return G

field = [list(line.strip()) for line in fileinput.input()]
G = field_to_graph(field)
start = find_start(field)
end = find_end(field)

path = nx.shortest_path(G, source=start, target=end)
fair_shortest_path_weight = nx.path_weight(G, path, weight="weight")

"""
for each non-border wall in the given puzzle, try cheating through this wall
by adding a vertex with edges to existing vertices at the wall's position, 
finding the shortest path on this modified graph, then putting the wall back
by removing the temporary vertex
"""
cheat_paths_savings = defaultdict(int)
for i, row in enumerate(field):
    for j, cell in enumerate(row):
        # don't remove walls on the border
        if i == 0 or i == len(field) - 1 or j == 0 or j == len(row) - 1:
            continue

        # only temporarily remove walls
        if field[i][j] != WALL:
            continue

        # try removing this wall, i.e., add a vertex here
        add_edges_to_neighbors_of(G, i, j, field)

        if not G.has_node((i, j)):
            # if it's a completely interior wall, nothing happened when we added edges just above
            continue

        # see if cheating through this wall is an improvement
        cheating_shortest_path = nx.shortest_path(G, source=start, target=end)
        cheating_shortest_path_weight = nx.path_weight(G, cheating_shortest_path, weight="weight")
        G.remove_node((i, j))

        if cheating_shortest_path_weight < fair_shortest_path_weight:
            cheat_savings = fair_shortest_path_weight - cheating_shortest_path_weight
            cheat_paths_savings[cheat_savings] += 1

if len(cheat_paths_savings.keys()) < 20:
    # sample input - compare counts of each amount
    print(cheat_paths_savings)
else:
    # answer for actual problem
    print(sum([v for k, v in cheat_paths_savings.items() if k >= 100]))
