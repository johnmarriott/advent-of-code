#!/usr/bin/env python

"""
This script makes a CSV of the positions of the robots after each time step.
Used that to plot the positions, then noticed that they were in horizontal and
vertical alignment periodically, for my input these were

    vertical alignment at 99 + 101*v seconds, for v = 0, 1, 2, ...
    horizontal alignment at 42 + 103*h seconds, for h = 0, 1, 2, ...

these both align at v = 79 + 101*n, h = 80 + 103*n

so the image appears at t=8179, 18582, ...
"""

from dataclasses import dataclass
import fileinput

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

def init_robot_position_output():
    with open(f"positions.csv", "w") as f:
        print("t,robot,x,y", file=f)

def append_robot_position_output(i: int, robots: list[Robot]):
    with open(f"positions.csv", "a") as f:
        for j, robot in enumerate(robots):
            print(f"{i},{j},{robot.px},{robot.py}", file=f)

lines = [line.strip() for line in fileinput.input()]

robots = parse_robots(lines)

init_robot_position_output()
for i in range(20000):
    append_robot_position_output(i, robots)

    if i == 8179:
        for x in range(FIELD_HEIGHT):
            for y in range(FIELD_WIDTH):
                if any(robot.px == y and robot.py == x for robot in robots):
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()

    move_robots(robots)
