#!/usr/bin/env python
"""
Advent of Code 2025 - Day 10, Part 1
https://adventofcode.com/2025/day/10

Consider all combinations of button presses iteratively: all one-button presses,
then all two-button presses, until matching the given configuration.
"""

from dataclasses import dataclass
import fileinput
from itertools import combinations_with_replacement


@dataclass()
class Machine:
    light_diagram: tuple[int]
    wiring_schematics: tuple[tuple[int]]
    joltage_requirements: tuple[int]


def line_to_machine(line: str) -> Machine:
    first_space_index = line.index(" ")
    light_diagram = tuple(0 if x == "." else 1 for x in line[1:first_space_index - 1])

    first_brace_index = line.index("{")
    wiring_substring = line[first_space_index + 1:first_brace_index - 1]
    wiring_substring_no_parens = "".join([c for c in wiring_substring if c not in "()"])
    wiring_schematics = tuple(
        tuple(int(x) for x in part.split(","))
        for part in wiring_substring_no_parens.split(" ")
    )

    joltage_substring = line[first_brace_index + 1:-1]
    joltage_requirements = tuple(int(x) for x in joltage_substring.split(","))

    return Machine(light_diagram, wiring_schematics, joltage_requirements)


def least_button_presses(machine: Machine) -> int:
    """
    Try each button once.  If that doesn't work, try each button twice.
    Repeat until we find a solution.
    """

    n_button_presses = 1
    desired_state = list(machine.light_diagram)

    while True:
        button_combinations = combinations_with_replacement(
            machine.wiring_schematics, n_button_presses
        )

        for button_combination in button_combinations:
            state = [0 for _ in machine.light_diagram]

            # button combination is something like (0, 2), (1,), (0, 2)
            for button_presses in button_combination:
                # button_presses is something like (0, 2)
                for button_index in button_presses:
                    state[button_index] ^= 1  # toggle the light

            if state == desired_state:
                return n_button_presses

        n_button_presses += 1


def main():
    lines = [line.strip() for line in fileinput.input()]

    total_button_presses = 0
    for line in lines:
        machine = line_to_machine(line)
        total_button_presses += least_button_presses(machine)

    print(total_button_presses)


if __name__ == "__main__":
    main()
