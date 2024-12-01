#!/usr/bin/env python

"""
https://adventofcode.com/2022/day/9#part2

Extend part 1 to a list of ten nodes
"""

import fileinput
from dataclasses import dataclass

@dataclass
class Node:
    x: int
    y: int

    def move(self, direction):
        if direction == "U":
            self.y += 1
        elif direction == "D":
            self.y -= 1
        elif direction == "L":
            self.x -= 1
        elif direction == "R":
            self.x += 1
        else:
            raise ValueError(f"Invalid direction: {direction}")
        
    def move_closer_to(self, x, y):
        if abs(self.x - x) > 1 or abs(self.y - y) > 1:
            # at least one of the coördinates is more than one unit away

            if self.x < x:
                self.x += 1
            elif self.x > x:
                self.x -= 1

            if self.y < y:
                self.y += 1
            elif self.y > y:
                self.y -= 1

def print_nodes(nodes: list[Node]):
    min_x = min(min(node.x for node in nodes), 0)
    max_x = max(max(node.x for node in nodes), 0)
    min_y = min(min(node.y for node in nodes), 0)
    max_y = max(max(node.y for node in nodes), 0)

    field = [["." for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]

    field[-min_y][-min_x] = "s"

    for i in reversed(range(len(nodes))):
        field[nodes[i].y - min_y][nodes[i].x - min_x] = str(i)
    
    for row in reversed(field):
        print("".join(row))

nodes = [Node(0, 0) for _ in range(10)]
head = nodes[0]
tail = nodes[-1]
        
tail_coordinates_visited = [(tail.x, tail.y)]

print_nodes(nodes)

for line in fileinput.input():
    line_parts = line.split()
    direction = line_parts[0]
    moves = int(line_parts[1])

    print(f"\n{line.strip()}\n")
    for _ in range(moves):
        head.move(direction)

        for i in range(1, len(nodes)):
            nodes[i].move_closer_to(nodes[i - 1].x, nodes[i - 1].y)

        tail_coordinates_visited.append((tail.x, tail.y))

    print_nodes(nodes)

print(len(set(tail_coordinates_visited)))
