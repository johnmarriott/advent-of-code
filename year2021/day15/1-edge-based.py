#!/usr/bin/env python

"""
big idea:

do shortest path Dijkstra, but:

- keep a history of the symbols to reach a vertex, e.g. ">>vv<v"
- if you just went twice in the same direction (you are "facing" that directino), 
  edit the connections of the current vertex to swap out the edge going forward
  to have a direction of "{forward-character}{right-character}" and a weight
  that's the sum of those two weights
- don't think we'll have to worry about going backward or coming across
  this vertex another way since Dijkstra is greedy?
"""

import fileinput
import math
from dataclasses import dataclass
from enum import Enum

# read input into a matrix ####

matrix = [[int(x) for x in line.strip()] for line in fileinput.input()]

# construct graph ####

# graph = (vertices, edges)
# vertices is a list of vertex label/key strings
# edges is a dict of dict of Edge objects, which is indexed as:
# edges[from_vertex_label][to_vertex_label] = Edge( weight/direction between these )

Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])

@dataclass
class Edge:
    weight: int
    direction: Direction

vertices: list[str] = []
edges: dict[str, dict[str, Edge]] = {}

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        key = f"{i},{j}"
        vertices.append(key)
        edges[key] = {}

        # an edge from this vertex to a neighbor costs the neighbor's weight
        if i > 0:
            edges[key][f"{i - 1},{j}"] = Edge(int(matrix[i - 1][j]), Direction.NORTH)
        if j > 0:
            edges[key][f"{i},{j - 1}"] = Edge(int(matrix[i][j - 1]), Direction.WEST)
        if i < len(matrix) - 1:
            edges[key][f"{i + 1},{j}"] = Edge(int(matrix[i + 1][j]), Direction.SOUTH)
        if j < len(matrix[0]) - 1:
            edges[key][f"{i},{j + 1}"] = Edge(int(matrix[i][j + 1]), Direction.EAST)

# find shortest path from start vertex to all others ####

start_vertex_key = "0,0"
end_vertex_key = f"{len(matrix) - 1},{len(matrix[0]) - 1}"

# basic djikstra
# track the distance from the start vertex in both places, it's nice to have on the 
# unvisited list because you can search for the min among unvisited in one place,
# and the full vertex distance from start doesn't get deleted from.
# but you do have to do extra bookkeeping
unvisited_vertex_distance_from_start_vertex = { key: math.inf for key in vertices }
vertex_distance_from_start_vertex = { key: math.inf for key in vertices }

# track shortest-path predecessors from start to the vertex by a list of vertex keys and the 
# direction taken to get there
vertex_predecessors_from_start_vertex = { key: { "vertex_keys": [], "directions": [] } for key in vertices }

unvisited_vertex_distance_from_start_vertex[start_vertex_key] = 0
vertex_distance_from_start_vertex[start_vertex_key] = 0

while len(unvisited_vertex_distance_from_start_vertex) > 0:
    current_vertex_key = min(unvisited_vertex_distance_from_start_vertex, key=unvisited_vertex_distance_from_start_vertex.get)
    current_distance_from_start = vertex_distance_from_start_vertex[current_vertex_key]

    print(f"visiting {current_vertex_key}")
    del unvisited_vertex_distance_from_start_vertex[current_vertex_key]

    # check if distances/paths of neighbors should be updated
    for neighbor_key in edges[current_vertex_key].keys():
        direction_to_neighbor = "TODO" # TODO

        if not neighbor_key in unvisited_vertex_distance_from_start_vertex:
            continue

        distance_from_start_to_neighbor = current_distance_from_start + edges[current_vertex_key][neighbor_key].weight

        if distance_from_start_to_neighbor < vertex_distance_from_start_vertex[neighbor_key]:
            # we found a better way to get to this neighbor
            unvisited_vertex_distance_from_start_vertex[neighbor_key] = distance_from_start_to_neighbor
            vertex_distance_from_start_vertex[neighbor_key] = distance_from_start_to_neighbor
            #vertex_predecessors_from_start_vertex[neighbor_key] = {
            #    "vertex_keys": vertex_predecessors_from_start_vertex[current_vertex_key] + [current_vertex_key],
            #    "directions": vertex_predecessors_from_start_vertex[current_vertex_key] + [direction_to_neighbor]
            #}
            print(f"updating {neighbor_key} to {current_distance_from_start} + {edges[current_vertex_key][neighbor_key].weight} = {distance_from_start_to_neighbor} via {current_vertex_key}")

print(vertex_distance_from_start_vertex[end_vertex_key])