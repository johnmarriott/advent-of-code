#!/usr/bin/env python

from enum import Enum
import fileinput

OBSTRUCTION = "#"
OPEN = "."
EXIT = "*"

Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])

arrow_to_direction = {
    "^": Direction.NORTH,
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
}

next_direction = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
}

direction_offsets = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}

lines = [line.strip() for line in fileinput.input()]

# generate field, padded with exits
field = [[EXIT] * (len(lines[0]) + 2)]
for line in lines:
    field.append([EXIT] + list(line) + [EXIT])
field.append([EXIT] * (len(lines[0]) + 2))

# find guard's start
guard_starting_x = None
guard_starting_y = None
guard_starting_direction = None

for i, row in enumerate(field):
    for j, cell in enumerate(row):
        if cell in arrow_to_direction:
            guard_starting_x = i
            guard_starting_y = j
            guard_starting_direction = arrow_to_direction[cell]
            break

## part one

positions_visited = set()

guard_x = guard_starting_x
guard_y = guard_starting_y
guard_direction = guard_starting_direction

guard_exited = False
while not guard_exited:
    positions_visited.add((guard_x, guard_y))

    next_x = guard_x + direction_offsets[guard_direction][0]
    next_y = guard_y + direction_offsets[guard_direction][1]

    next_cell = field[next_x][next_y]

    if next_cell == OBSTRUCTION:
        guard_direction = next_direction[guard_direction]
    elif next_cell == EXIT:
        guard_exited = True
    else: # next cell is open
        guard_x = next_x
        guard_y = next_y

print(f"part one: {len(positions_visited)}")

## part two

# set the guard's current position to open so it will be pathable
# if she returns to it
field[i][j] = OPEN

viable_obstruction_positions = []

# check every possible starting position for "will putting an obstruction 
# here make the guard go into a loop" which we'll check by "will putting
# and obstruction here prevent the guard from exiting before step max_loop_steps"
for i in range(1, len(field) - 1):
    for j in range(1, len(field[0]) - 1):
        if field[i][j] == OPEN:
            # copy the field and put an obstruction here
            obstructed_field = [row.copy() for row in field]
            obstructed_field[i][j] = OBSTRUCTION

            guard_x = guard_starting_x
            guard_y = guard_starting_y
            guard_direction = guard_starting_direction 

            guard_exited_or_looping = False

            positions_visited = set((guard_x, guard_y, guard_direction))

            while not guard_exited_or_looping:
                next_x = guard_x + direction_offsets[guard_direction][0]
                next_y = guard_y + direction_offsets[guard_direction][1]

                next_cell = obstructed_field[next_x][next_y]

                if next_cell == OBSTRUCTION:
                    guard_direction = next_direction[guard_direction]

                elif next_cell == EXIT:
                    guard_exited_or_looping = True

                else: # guard can move to next position
                    guard_x = next_x
                    guard_y = next_y

                    if (guard_x, guard_y, guard_direction) in positions_visited:
                        # guard has returned to a previous position in the same direction
                        viable_obstruction_positions.append((i, j))
                        guard_exited_or_looping = True
                        break

                    positions_visited.add((guard_x, guard_y, guard_direction))

print(f"part two: {len(viable_obstruction_positions)}")
