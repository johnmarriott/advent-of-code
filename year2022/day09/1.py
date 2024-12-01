#!/usr/bin/env python

"""
https://adventofcode.com/2022/day/9

Big idea:

Calculate the distance between head and tail vertically and horizontally, and
if they are more than one unit away in either direction, the tail needs to catch up

When the tail is behind and directly above/below/left/right of the head, it is
two units away and needs to catch up to one unit away, i.e., it needs to move
one step closer along the axis they're not equal on

When the tail is behind and diagonal, it is a knight's move away.  The tail needs
to move one step closer along both axes.

In either case, the tail catches up by moving one step closer along each axis that
it's not already equal to the head in that coördinate.
"""

import fileinput
from dataclasses import dataclass

@dataclass
class Point:
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
        
head = Point(0, 0)
tail = Point(0, 0)

tail_coordinates_visited = [(tail.x, tail.y)]

print(f"Head: {head}, Tail: {tail}")
for line in fileinput.input():
    line_parts = line.split()
    direction = line_parts[0]
    moves = int(line_parts[1])

    print(f"\n{line.strip()}")
    for _ in range(moves):
        head.move(direction)
        tail.move_closer_to(head.x, head.y)
        tail_coordinates_visited.append((tail.x, tail.y))

        print(f"Head: {head}, Tail: {tail}")

print(len(set(tail_coordinates_visited)))