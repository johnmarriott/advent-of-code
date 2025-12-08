#!/usr/bin/env python
"""
Advent of Code 2025 Day 8 Part 1
https://adventofcode.com/2025/day/8
"""


import fileinput
from itertools import combinations

import networkx as nx

from part1 import (
    all_pair_box_distances,
    JunctionBox, 
    parse_boxes
)


def last_edge_to_connect_graph(boxes: dict[str, JunctionBox]) -> tuple[str, str]:
    """
    Return the last edge needed to fully connect the vertices in in `boxes` with edges added in order
    of increasing Euclidean distance.
    """

    box_pair_distances = all_pair_box_distances(boxes) 

    graph = nx.Graph()

    for name in boxes.keys():
        graph.add_node(name)

    for pair, _ in box_pair_distances:
        last_connection = pair
        graph.add_edge(pair[0], pair[1])
        if nx.is_connected(graph):
            break

    return last_connection


def main() -> None:
    lines = [line.strip() for line in fileinput.input()]
    boxes = parse_boxes(lines)

    last_connection = last_edge_to_connect_graph(boxes)
    first_x = boxes[last_connection[0]].x
    second_x = boxes[last_connection[1]].x

    print(abs(first_x * second_x))


if __name__ == "__main__":
    main()
