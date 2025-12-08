#!/usr/bin/env python
"""
Advent of Code 2025 Day 8 Part 1
https://adventofcode.com/2025/day/8

Big idea: find the first 10/1000 closest connections, put those into a graph,
and find the product of the sizes of the three largest connected components.

Assumes that the top three components will be at least a pair of vertices.
"""

from dataclasses import dataclass
import fileinput
from itertools import combinations
from math import inf, pow, sqrt

import networkx as nx


@dataclass
class JunctionBox:
    name: str
    x: int
    y: int
    z: int


def parse_boxes(lines: list[str]) -> tuple[list[str], dict[str, JunctionBox]]:
    """
    Parse input lines into a list of junction box names and a dictionary of JunctionBox objects.
    """
    box_names = []
    boxes = {}
    for line in lines:
        box_names.append(line)
        x, y, z = map(int, line.split(','))
        boxes[line] = JunctionBox(line, x, y, z)

    return boxes


def box_distance(box_a: JunctionBox, box_b: JunctionBox) -> float:
    """
    Return the Euclidean distance between two junction boxes.
    """
    return sqrt(pow(box_a.x - box_b.x, 2) + pow(box_a.y - box_b.y, 2) + pow(box_a.z - box_b.z, 2))


def all_pair_box_distances(boxes: dict[str, JunctionBox]) -> list[tuple[tuple[str, str], float]]:
    """
    Return a list of all pairs of junction boxes and their Euclidean distances.
    """

    box_names = boxes.keys()

    all_box_pairs = combinations(box_names, 2)
    box_pair_distances = [(pair, box_distance(boxes[pair[0]], boxes[pair[1]])) for pair in all_box_pairs]
    box_pair_distances.sort(key=lambda x: x[1])

    return box_pair_distances


def connect_boxes(boxes: dict[str, JunctionBox], n_connections: int) -> nx.Graph:
    """
    Returns a graph where the `n_connections` closest pairs of junction boxes share edges, and other vertices
    are not present.
    """

    box_pair_distances = all_pair_box_distances(boxes)

    graph = nx.Graph()
    for pair, _ in box_pair_distances[:n_connections]:
        graph.add_edge(pair[0], pair[1])

    return graph


def main() -> None:
    lines = [line.strip() for line in fileinput.input()]
    boxes = parse_boxes(lines)

    n_connections = 10 if len(lines) < 1000 else 1000 # sample vs full problem statements
    connection_graph = connect_boxes(boxes, n_connections)

    sizes = [len(c) for c in nx.connected_components(connection_graph)]
    sizes_sorted = sorted(sizes, reverse=True)

    # assume there are at least three non-one-sized circuits
    print(sizes_sorted[0] * sizes_sorted[1] * sizes_sorted[2])


if __name__ == "__main__":
    main()
