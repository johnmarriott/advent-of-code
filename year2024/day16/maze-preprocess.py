#!/usr/bin/env python

"""
build a directed graph, where each cell has four vertices: one for each direction and with
weight 1000 between them, and edges between adjacent cells with weight 1

turn this into a networkx graph and use it to find the shortest paths to solve the puzzles

This one has an intermediate step of parsing the input into data structures.  It's about 20%
slower than the direct construction, but both are about 1s for this problem's input
"""


from dataclasses import dataclass
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

@dataclass
class Edge:
    start: str
    end: str
    weight: int

@dataclass
class Vertex:
    row: int
    col: int
    direction: Direction
    edges: list[Edge]

    def __str__(self):
        return vertex_name(self.row, self.col, self.direction)

def vertex_name_to_coordinates(vertex_name: str) -> str:
    """strip the direction from a vertex name, e.g., (1,2)-Direction.NORTH -> (1,2)"""
    return vertex_name.split("-")[0]

def find_start(field: list[list[str]], vertices: dict[str, Vertex]) -> Vertex:
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == START:
                return vertices[vertex_name(i, j, Direction.EAST)]

def find_ends(field: list[list[str]], vertices: dict[str, Vertex]) -> list[Vertex]:
    ends = []
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == END:
                # find any vertex at this position
                for direction in Direction:
                    end = vertex_name(i, j, direction)

                    if end in vertices:
                        ends.append(end)
    return ends

def map_vertices(field: list[list[str]]) -> dict[str, Vertex]:
    vertices: dict[str, Vertex] = {}

    # add all vertices with turns but not edges between adjacent cells    
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if cell == WALL:
                continue

            interior_vertices = [
                Vertex(row=i, col=j, direction=Direction.NORTH, edges=[]),
                Vertex(row=i, col=j, direction=Direction.EAST, edges=[]),
                Vertex(row=i, col=j, direction=Direction.SOUTH, edges=[]),
                Vertex(row=i, col=j, direction=Direction.WEST, edges=[])
            ]

            # connect the facing directions
            interior_vertices[0].edges = [
                Edge(start=str(interior_vertices[0]), end=str(interior_vertices[1]), weight=1000),
                Edge(start=str(interior_vertices[0]), end=str(interior_vertices[3]), weight=1000)
            ]
            interior_vertices[1].edges = [
                Edge(start=str(interior_vertices[1]), end=str(interior_vertices[0]), weight=1000),
                Edge(start=str(interior_vertices[1]), end=str(interior_vertices[2]), weight=1000)
            ]
            interior_vertices[2].edges = [
                Edge(start=str(interior_vertices[2]), end=str(interior_vertices[1]), weight=1000),
                Edge(start=str(interior_vertices[2]), end=str(interior_vertices[3]), weight=1000)
            ]
            interior_vertices[3].edges = [
                Edge(start=str(interior_vertices[3]), end=str(interior_vertices[0]), weight=1000),
                Edge(start=str(interior_vertices[3]), end=str(interior_vertices[2]), weight=1000)
            ]

            for vertex in interior_vertices:
                vertices[str(vertex)] = vertex

    # add edges between adjacent cells
    for vertex in vertices.values():
        vertex_ahead = vertex_name(vertex.row + vertex.direction.value[0], vertex.col + vertex.direction.value[1], vertex.direction)

        if vertex_ahead in vertices:
            vertex.edges.append(Edge(start=str(vertex), end=vertex_ahead, weight=1))

    return vertices

def vertices_to_networkx_graph(vertices: dict[str, Vertex]) -> nx.DiGraph:
    import networkx as nx
    G = nx.DiGraph()

    for vertex in vertices.values():
        G.add_node(str(vertex))

        for edge in vertex.edges:
            G.add_edge(str(edge.start), str(edge.end), weight=edge.weight)

    return G

field = [list(line.strip()) for line in fileinput.input()]
vertices = map_vertices(field)
start = find_start(field, vertices)
ends = find_ends(field, vertices)

G = vertices_to_networkx_graph(vertices)

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
