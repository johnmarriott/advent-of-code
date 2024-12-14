#!/usr/bin/env python

from dataclasses import dataclass
import fileinput
import math

FIELD_WIDTH = 101
FIELD_HEIGHT = 103

@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

def parse_robots(lines: list[str]) -> list[Robot]:
    robots = []
    for line in lines:
        parts = line.split(" ")
        px, py = map(int, parts[0][2:].split(','))
        vx, vy = map(int, parts[1][2:].split(','))
        robots.append(Robot(px, py, vx, vy))
    return robots

def move_robots(robots: list[Robot]):
    for robot in robots:
        robot.px = (robot.px + robot.vx) % FIELD_WIDTH
        robot.py = (robot.py + robot.vy) % FIELD_HEIGHT

lines = [line.strip() for line in fileinput.input()]

robots = parse_robots(lines)

for _ in range(100):
    move_robots(robots)

# inclusive min, exclusive max indices of quadrants
quadrants = [
    {
        "x_min": 0,
        "x_max": FIELD_WIDTH // 2,
        "y_min": 0,
        "y_max": FIELD_HEIGHT // 2,
    },
    {
        "x_min": FIELD_WIDTH // 2 + 1,
        "x_max": FIELD_WIDTH,
        "y_min": 0,
        "y_max": FIELD_HEIGHT // 2,
    },
    {
        "x_min": 0,
        "x_max": FIELD_WIDTH // 2,
        "y_min": FIELD_HEIGHT // 2 + 1,
        "y_max": FIELD_HEIGHT,
    },
    {
        "x_min": FIELD_WIDTH // 2 + 1,
        "x_max": FIELD_WIDTH,
        "y_min": FIELD_HEIGHT // 2 + 1,
        "y_max": FIELD_HEIGHT,
    }
]

quandrant_robots = [0, 0, 0, 0]

for robot in robots:
    for i, quadrant in enumerate(quadrants):
        if (
            quadrant["x_min"] <= robot.px < quadrant["x_max"] 
            and quadrant["y_min"] <= robot.py < quadrant["y_max"]
        ):
            quandrant_robots[i] += 1

print(quandrant_robots)
print(math.prod(quandrant_robots))
