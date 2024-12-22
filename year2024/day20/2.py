#!/usr/bin/env python

"""
https://adventofcode.com/2024/day/20#part2

brute force 

this is really slow 

consider every possible cheat: from one non-wall
to another non-wall, within 20 steps of each other

temporarily add that cheat to the graph and see
what is the shortest path using it
"""

from collections import defaultdict
from enum import Enum
import fileinput

import networkx as nx


WALL = "#"
START = "S"
END = "E"
EMPTY = "."

CHEAT_STEPS = 20

class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

def print_field(field: list[list[str]]) -> None:
    for row in field:
        print("".join(row))

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

def l1_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

def cheats(field: list[list[str]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    return all possible cheats:
    - starting at a non-wall wall
    - ending at a non-wall
    - within 20 units of each other (inclusive)
    """

    cheat_positions = set()
    for i in range(1, len(field) - 1):
        for j in range(1, len(field[0]) - 1):
            if field[i][j] != WALL:
                for k in range(1, len(field) - 1):
                    for l in range(1, len(field[0]) - 1):
                        distance = l1_distance((i, j), (k, l))
                        if field[k][l] != WALL and 1 < distance <= CHEAT_STEPS:
                            # since this is an undirected graph, don't look at the opposite pair
                            if not ((k, l), (i, j)) in cheat_positions:
                                cheat_positions.add(((i, j), (k, l)))

    return list(cheat_positions)


field = [list(line.strip()) for line in fileinput.input()]
G = field_to_graph(field)
start = find_start(field)
end = find_end(field)

path = nx.shortest_path(G, source=start, target=end)
fair_shortest_path_weight = nx.path_weight(G, path, weight="weight")

cheat_positions = cheats(field)
cheat_paths_weights = {}
for cheat_position in cheat_positions:
    G.add_edge(cheat_position[0], cheat_position[1], weight=l1_distance(cheat_position[0], cheat_position[1]))

    # see if using this cheat is an improvement
    cheating_shortest_path = nx.shortest_path(G, source=start, target=end)
    cheating_shortest_path_weight = nx.path_weight(G, cheating_shortest_path, weight="weight")
    cheat_paths_weights[cheat_position] = cheating_shortest_path_weight

    G.remove_edge(cheat_position[0], cheat_position[1])

cheat_savings = defaultdict(int)

if len(field) < 20:
    threshold = 50 # sample input
else:
    threshold = 100 # full input

for positions, weight in cheat_paths_weights.items():
    cheat_saving = fair_shortest_path_weight - weight
    if cheat_saving >= threshold:
        cheat_savings[cheat_saving] += 1

if len(field) < 20:
    # compare with the sample counts
    print(cheat_savings)
else:
    # answer for full input
    print(sum(cheat_savings.values()))