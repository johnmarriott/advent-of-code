#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum
import fileinput
import math

# 439

"""
big idea:

reverse the start/end

Create the graph with an edge to a neighbor if you can reach the current vertex
from the neighbor on the hiking path, i.e., if the neighbor is at most one less
than the current vertex

Then find the shortest path lengths from E to all other vertices, and from this
take the shortest distance from E to one of the a/S vertices
"""

class Direction(Enum):
    def __init__(self, vertical_offset, horizontal_offset):
        self.vertical_offset = vertical_offset
        self.horizontal_offset = horizontal_offset

    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

@dataclass
class Vertex:
    weight_into: int
    neighbor_keys: list[str]

def read_field(lines) -> tuple[list[list[int]], list[str], str]:
    start_keys = []
    end_key = None

    # Add a border of infinities around the field
    row_of_infinities = [math.inf] * (len(lines[0]) + 2)
    field = [row_of_infinities]

    for i in range(len(lines)):
        row = [math.inf]

        for j in range(len(lines[i])):
            if lines[i][j] == 'S' or lines[i][j] == 'a':
                start_keys.append(f"{i + 1},{j + 1}")
                row.append(0)
            elif lines[i][j] == 'E':
                end_key = f"{i + 1},{j + 1}"
                row.append(25)
            else:
                row.append(ord(lines[i][j]) - ord('a'))

        row.append(math.inf)
        field.append(row)

    field.append(row_of_infinities)

    return field, start_keys, end_key

def make_graph(field: list[list[str]]) -> dict[str, Vertex]:
    """
    Parse field into a directed graph represented by Vertex nodes, with an 
    edge to a neighbor if the height of the neighbor is at least one less
    than the height of the current vertex
    """
    graph: dict[str, Vertex] = {}

    for i in range(1, len(field) - 1):
        for j in range(1, len(field[i]) - 1):
            key = f"{i},{j}"
            neighbors = []

            for direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                neighbor_i = i + direction.vertical_offset
                neighbor_j = j + direction.horizontal_offset

                if field[i][j] - field[neighbor_i][neighbor_j] <= 1:
                    neighbors.append(f"{neighbor_i},{neighbor_j}")

            graph[key] = Vertex(
                weight_into=1,
                neighbor_keys=neighbors
            )

    return graph

def shortest_path_from_start_to_all(graph: dict[str, Vertex], start_vertex_key: str) -> dict[str, int]:
    """ Find shortest path from start vertex to all others """

    # basic Dijkstra
    #
    # track the distance from the start vertex in both places, it's nice to have on the 
    # unvisited list because you can search for the min among unvisited in one place,
    # and the full vertex distance from start doesn't get deleted from.
    # but you do have to do extra bookkeeping
    unvisited_vertex_distance_from_start_vertex = { key: math.inf for key in graph.keys() }
    vertex_distance_from_start_vertex = { key: math.inf for key in graph.keys() }
    vertex_predecessor_key_from_start_vertex = { key: None for key in graph.keys() }

    unvisited_vertex_distance_from_start_vertex[start_vertex_key] = 0
    vertex_distance_from_start_vertex[start_vertex_key] = 0

    while len(unvisited_vertex_distance_from_start_vertex) > 0:
        current_vertex_key = min(unvisited_vertex_distance_from_start_vertex, key=unvisited_vertex_distance_from_start_vertex.get)
        current_distance_from_start = vertex_distance_from_start_vertex[current_vertex_key]

        del unvisited_vertex_distance_from_start_vertex[current_vertex_key]

        # check if distances/paths of neighbors should be updated
        for neighbor_key in graph[current_vertex_key].neighbor_keys:
            if not neighbor_key in unvisited_vertex_distance_from_start_vertex:
                continue

            distance_from_start_to_neighbor = current_distance_from_start + graph[neighbor_key].weight_into

            if distance_from_start_to_neighbor < vertex_distance_from_start_vertex[neighbor_key]:
                unvisited_vertex_distance_from_start_vertex[neighbor_key] = distance_from_start_to_neighbor
                vertex_distance_from_start_vertex[neighbor_key] = distance_from_start_to_neighbor
                vertex_predecessor_key_from_start_vertex[neighbor_key] = current_vertex_key

    return vertex_distance_from_start_vertex

lines = [line.strip() for line in fileinput.input()]
field, start_keys, end_key = read_field(lines)
graph = make_graph(field)

shortest_distances = shortest_path_from_start_to_all(graph, end_key)

print(min([shortest_distances[start_key] for start_key in start_keys]))
