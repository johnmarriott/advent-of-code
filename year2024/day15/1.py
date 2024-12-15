#!/usr/bin/env python

import fileinput

ROBOT = "@"
BOX = "O"
WALL = "#"
EMPTY = "."

MOVE_OFFSETS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}

def parse_input(lines: list[str]) -> tuple[list[list[str]], list[str]]:
    past_warehouse = False
    warehouse = []
    moves = []

    for line in lines:
        if len(line) == 0:
            past_warehouse = True
            continue

        if not past_warehouse:
            warehouse.append(list(line))
        else:
            moves.extend(list(line))

    return warehouse, moves

def robot_position(warehouse: list[list[str]]) -> tuple[int, int]:
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == ROBOT:
                return i, j
    
def robot_move(warehouse: list[list[str]], move: str, robot_position: tuple[int, int]) -> tuple[int, int]:
    """
    This modifies warehouse in place
    """
    next_i = robot_position[0] + MOVE_OFFSETS[move][0]
    next_j = robot_position[1] + MOVE_OFFSETS[move][1]

    if warehouse[next_i][next_j] == WALL:
        return robot_position

    if warehouse[next_i][next_j] == EMPTY:
        warehouse[next_i][next_j] = ROBOT
        warehouse[robot_position[0]][robot_position[1]] = EMPTY
        return next_i, next_j

    # else the next position is a box
    # the robot can move if it's a line of boxes with an empty space before a wall
    boxes_in_front_of_robot = []
    next_box_i = next_i 
    next_box_j = next_j 

    while warehouse[next_box_i][next_box_j] == BOX:
        boxes_in_front_of_robot.append((next_box_i, next_box_j))
        next_box_i += MOVE_OFFSETS[move][0]
        next_box_j += MOVE_OFFSETS[move][1]

    # now next_box_i, next_box_j is the first non-box position
    if warehouse[next_box_i][next_box_j] == WALL:
        return robot_position
    # else we can shift these boxes and this robot

    # move the robot
    warehouse[next_i][next_j] = ROBOT
    warehouse[robot_position[0]][robot_position[1]] = EMPTY

    # move the boxes
    for box_i, box_j in boxes_in_front_of_robot:
        warehouse[box_i + MOVE_OFFSETS[move][0]][box_j + MOVE_OFFSETS[move][1]] = BOX

    return next_i, next_j

def quantify_warehouse(warehouse: list[list[str]]) -> int:
    sum_gps = 0

    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == BOX:
                sum_gps += 100 * (i) + j 

    return sum_gps

def print_warehouse(warehouse: list[list[str]]) -> None:
    for row in warehouse:
        print("".join(row))
    print()


lines = [line.strip() for line in fileinput.input()]
warehouse, moves = parse_input(lines) 
i, j = robot_position(warehouse)

for move in moves:
    i, j = robot_move(warehouse, move, (i, j))

print_warehouse(warehouse)
print(quantify_warehouse(warehouse))