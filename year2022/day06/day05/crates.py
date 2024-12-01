#!/usr/bin/env python

import copy
import fileinput

from dataclasses import dataclass

@dataclass
class MoveInstruction:
    source: str
    destination: str
    n_moves: int

def move_crates_p1(source: list, destination: list, n: int):
    """Move crates singly from source stack to destination stack."""

    for _ in range(n):
        crate = source.pop()
        destination.append(crate)

def move_crates_p2(source: list, destination: list, n: int):
    """Move crates together from source stack to destination stack."""

    crates = source[-n:] # grab crates to move
    source[-n:] = [] # remove these crates from the source
    destination.extend(crates)

def parse_stacks(lines: list[str], empty_line: int) -> tuple[dict[str, list], list[str]]:
    stacks: dict[str, list] = {}

    # the line above the empty line has the stack names
    stack_names = lines[empty_line - 1].split()

    for stack_name in stack_names:
        stacks[stack_name] = []

    for i in range(empty_line - 2, -1, -1):
        line = lines[i]
        for j in range(len(stack_names)):
            crate = line[1 + 4*j : 2 + 4*j]
            if crate != ' ' and crate != '':
                stacks[stack_names[j]].append(crate)

    return stacks, stack_names

def parse_moves(lines: list[str], empty_line: str) -> list[MoveInstruction]:
    moves = []

    for line in lines[empty_line + 1:]:
        line_parts = line.split()
        moves.append(MoveInstruction(
            line_parts[3],
            line_parts[5],
            int(line_parts[1])
        ))

    return moves

lines = [line.rstrip('\r\n') for line in fileinput.input()]

# find the empty line that separates the halves of the input
empty_line = 0
for i in range(len(lines)):
    if len(lines[i]) == 0:
        empty_line = i
        continue

stacks_p1, stack_names = parse_stacks(lines, empty_line)
moves = parse_moves(lines, empty_line)

stacks_p2 = copy.deepcopy(stacks_p1)

for move in moves:
    move_crates_p1(
        stacks_p1[move.source], 
        stacks_p1[move.destination], 
        move.n_moves
    )

print("part 1: ", end='')
for stack_name in stack_names:
    print(stacks_p1[stack_name].pop(), end='')

print()

for move in moves:
    move_crates_p2(
        stacks_p2[move.source], 
        stacks_p2[move.destination], 
        move.n_moves
    )

print("part 2: ", end='')
for stack_name in stack_names:
    print(stacks_p2[stack_name].pop(), end='')

print()