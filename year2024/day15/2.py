#!/usr/bin/env python

import fileinput

ROBOT = "@"
BOX_LEFT = "["
BOX_RIGHT = "]"
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

    single_to_double = {
        "#": "##",
        "O": "[]",
        ".": "..",
        "@": "@."
    }

    for line in lines:
        if len(line) == 0:
            past_warehouse = True
            continue

        if not past_warehouse:
            warehouse.append(list("".join([single_to_double[c] for c in line])))
        else:
            moves.extend(list(line))

    return warehouse, moves

def robot_position(warehouse: list[list[str]]) -> tuple[int, int]:
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == ROBOT:
                return i, j

def box_can_move(warehouse: list[list[str]], move: str, box_position: tuple[int, int]) -> bool:
    if MOVE_OFFSETS[move][0] == 0:
        return box_can_move_horizontally(warehouse, move, box_position)
    else:
        return box_can_move_vertically(warehouse, move, box_position)

def box_can_move_horizontally(warehouse: list[list[str]], move: str, box_position: tuple[int, int]) -> bool:
    # next index horizontally is the second half of the box, check two ahead
    further_i = box_position[0] + MOVE_OFFSETS[move][0] * 2
    further_j = box_position[1] + MOVE_OFFSETS[move][1] * 2

    if warehouse[further_i][further_j] == WALL:
        return False

    if warehouse[further_i][further_j] == EMPTY:
        return True

    # else the next position is a box
    return box_can_move(warehouse, move, (further_i, further_j))

def box_can_move_vertically(warehouse: list[list[str]], move: str, box_position: tuple[int, int]) -> bool:
    move_offset = MOVE_OFFSETS[move]

    if warehouse[box_position[0]][box_position[1]] == BOX_LEFT:
        next_positions = (
            (box_position[0] + move_offset[0], box_position[1] + move_offset[1]), 
            (box_position[0] + move_offset[0], box_position[1] + 1 + move_offset[1])
        )
    else:
        next_positions = (
            (box_position[0] + move_offset[0], box_position[1] + move_offset[1] - 1), 
            (box_position[0] + move_offset[0], box_position[1] + move_offset[1])
        )

    if warehouse[next_positions[0][0]][next_positions[0][1]] == WALL:
        can_move_left_position = False
    elif warehouse[next_positions[0][0]][next_positions[0][1]] == EMPTY:
        can_move_left_position = True
    else: 
        can_move_left_position = box_can_move(warehouse, move, next_positions[0])
    
    if warehouse[next_positions[1][0]][next_positions[1][1]] == WALL:
        can_move_right_position = False
    elif warehouse[next_positions[1][0]][next_positions[1][1]] == EMPTY:
        can_move_right_position = True
    else:
        can_move_right_position = box_can_move(warehouse, move, next_positions[1])

    return can_move_left_position and can_move_right_position

def push_box(warehouse: list[list[str]], move: str, box_position: tuple[int, int]) -> None:
    """
    Assume that it's possible to push the box.  Modifies warehouse in place.
    """
    if MOVE_OFFSETS[move][0] == 0:
        push_box_horizontally(warehouse, move, box_position)
    else:
        push_box_vertically(warehouse, move, box_position)

def push_box_horizontally(warehouse: list[list[str]], move: str, box_position: tuple[int, int]) -> None:
    next_i = box_position[0] + MOVE_OFFSETS[move][0]
    next_j = box_position[1] + MOVE_OFFSETS[move][1]

    # next index horizontally is the second half of the box, check two ahead
    further_i = box_position[0] + MOVE_OFFSETS[move][0] * 2
    further_j = box_position[1] + MOVE_OFFSETS[move][1] * 2

    if warehouse[further_i][further_j] != EMPTY:
        # move the next box before moving this one
        push_box(warehouse, move, (further_i, further_j))

    # move the box
    warehouse[further_i][further_j] = warehouse[next_i][next_j]
    warehouse[next_i][next_j] = warehouse[box_position[0]][box_position[1]]
    warehouse[box_position[0]][box_position[1]] = EMPTY

def push_box_vertically(warehouse: list[list[str]], move: str, box_position: tuple[int, int]) -> None:
    move_offset = MOVE_OFFSETS[move]

    if warehouse[box_position[0]][box_position[1]] == BOX_LEFT:
        box_positions = (
            (box_position[0], box_position[1]), 
            (box_position[0], box_position[1] + 1)
        )
        next_positions = (
            (box_position[0] + move_offset[0], box_position[1] + move_offset[1]), 
            (box_position[0] + move_offset[0], box_position[1] + 1 + move_offset[1])
        )
    else:
        box_positions = (
            (box_position[0], box_position[1] - 1), 
            (box_position[0], box_position[1])
        )
        next_positions = (
            (box_position[0] + move_offset[0], box_position[1] + move_offset[1] - 1), 
            (box_position[0] + move_offset[0], box_position[1] + move_offset[1])
        )

    # move the box above the left position out of the way if needed
    if warehouse[next_positions[0][0]][next_positions[0][1]] != EMPTY:
        push_box(warehouse, move, next_positions[0])
    
    # move the box above the right position out of the way if needed
    if warehouse[next_positions[1][0]][next_positions[1][1]] != EMPTY:
        push_box(warehouse, move, next_positions[1])

    # move the box
    warehouse[next_positions[0][0]][next_positions[0][1]] = BOX_LEFT
    warehouse[next_positions[1][0]][next_positions[1][1]] = BOX_RIGHT
    warehouse[box_positions[0][0]][box_positions[0][1]] = EMPTY
    warehouse[box_positions[1][0]][box_positions[1][1]] = EMPTY

def robot_move(warehouse: list[list[str]], move: str, robot_position: tuple[int, int]) -> tuple[int, int]:
    """
    Modifies warehouse in place
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
    if box_can_move(warehouse, move, (next_i, next_j)):
        push_box(warehouse, move, (next_i, next_j))

        # move the robot
        warehouse[next_i][next_j] = ROBOT
        warehouse[robot_position[0]][robot_position[1]] = EMPTY

        return next_i, next_j
    else:
        return robot_position

def quantify_warehouse(warehouse: list[list[str]]) -> int:
    sum_gps = 0

    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == BOX_LEFT:
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

print(quantify_warehouse(warehouse))
