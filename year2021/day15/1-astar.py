#!/usr/bin/env python

import fileinput
import math
from dataclasses import dataclass

@dataclass
class Vertex:
    weight_into: int
    neighbor_keys: list[str]
    i: int # its coordinates in the input text
    j: int

# read input into a matrix ####

matrix = [[int(x) for x in line.strip()] for line in fileinput.input()]

# construct graph ####

# graph is a dict of Vertex objects
# keys of graph are vertex keys (redundant)
# values are vertices
graph: dict[str, Vertex] = {}

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        key = f"{i},{j}"

        neighbors = []
        if i > 0:
            neighbors.append(f"{i-1},{j}") # north
        if j > 0:
            neighbors.append(f"{i},{j-1}") # west
        if i < len(matrix) - 1:
            neighbors.append(f"{i+1},{j}") # south
        if j < len(matrix[0]) - 1:
            neighbors.append(f"{i},{j+1}") # east

        graph[key] = Vertex(
            weight_into=int(matrix[i][j]),
            neighbor_keys=neighbors,
            i=i,
            j=j
        )

# find shortest path from start vertex to all others ####

start_vertex_key = "0,0"
end_vertex_key = f"{len(matrix) - 1},{len(matrix[0]) - 1}"

# follows https://en.wikipedia.org/wiki/A*_search_algorithm closely
# can allow points to be re-added to the open set which we need for 2023.17

def reconstruct_path(came_from: dict, current: list[str]):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current) # prepend

    return total_path

def heuristic(vertex: Vertex, end_vertex: Vertex):
    """
    estimate the cost to reach the goal from node n
    """
    return abs(vertex.i - end_vertex.i) + abs(vertex.j - end_vertex.j)

def a_star(graph: dict[str, Vertex], start_key: str, end_key: str):
    """
    find a path from start to end
    """

    open_set = [start]
    came_from = {}
    g_score = {key: math.inf for key in graph.keys()}
    f_score = {key: math.inf for key in graph.keys()}

    g_score[start_key] = 0
    f_score[start_key] = heuristic(graph[start_key], graph[end_key])

    while len(open_set) > 0:
        current = node in open_set with the lowest fscore

    while openSet is not empty
        // This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)

        openSet.Remove(current)
        for each neighbor of current
            // d(current,neighbor) is the weight of the edge from current to neighbor
            // tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore := gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]
                // This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := tentative_gScore + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)

    // Open set is empty but goal was never reached
    return failure