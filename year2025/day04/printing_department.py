#!/usr/bin/env python

import fileinput
import itertools


EMPTY = "."
ROLL_OF_PAPER = "@"


def input_to_field(lines) -> list[list[str]]:
    """
    Convert input lines (strings of "@", roll of paper, and ".", empty) to 
    a "playing field" array padded with empty spaces.
    """
    field = []
    for line in lines:
        row = [EMPTY] + list(line) + [EMPTY]
        field.append(row)

    dots = [EMPTY for x in field[0]]
    field.insert(0, dots)
    field.append(dots)
    return field


def n_rolls_around_roll(field, i, j) -> int:
    """
    Returns the number of rolls of paper adjacent, up to eight, around the
    roll of paper at (i, j).  Assumes the given position is a roll of paper.
    """
    rolls = 0

    adjacent_positions = itertools.product((1, 0, -1), (1, 0, -1))
    for di, dj in adjacent_positions:
        if field[i + di][j + dj] == ROLL_OF_PAPER:
            rolls += 1

    # subtract the roll itself
    return rolls - 1


def remove_removable_rolls(field) -> int:
    """
    Removes all rolls of paper that have fewer than four adjacent rolls of
    paper.  Returns the number of rolls removed.  Modifies `field` in place.
    """
    removable_rolls = []
    for i in range(1, len(field) - 1):
        for j in range(1, len(field[0]) - 1):
            if (
                field[i][j] == ROLL_OF_PAPER
                and n_rolls_around_roll(field, i, j) < 4
            ):
                removable_rolls.append((i, j))

    for i, j in removable_rolls:
        field[i][j] = EMPTY

    return len(removable_rolls)


def main():
    lines = [line.strip() for line in fileinput.input()]
    field = input_to_field(lines)

    total_rolls_removed = 0
    rolls_removed = 1
    while rolls_removed > 0:
        rolls_removed = remove_removable_rolls(field)

        if total_rolls_removed == 0:
            print(f"Part one: {rolls_removed}")

        total_rolls_removed += rolls_removed

    print(f"Part two: {total_rolls_removed}")


if __name__ == "__main__":
    main()
