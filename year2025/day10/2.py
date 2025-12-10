#!/usr/bin/env python
"""
Advent of Code 2025 - Day 10, Part 2
https://adventofcode.com/2025/day/10#part2

Each button press adds a 0/1-vector to the running total.  Use linear programming
to find the minimum number of vector additions to reach the desired joltage values.
"""

from dataclasses import dataclass
import fileinput
from itertools import combinations_with_replacement

import numpy as np
from scipy.optimize import linprog



@dataclass()
class Machine:
    light_diagram: tuple[int]
    wiring_schematics: tuple[tuple[int]]
    joltage_requirements: tuple[int]


def line_to_machine(line: str) -> Machine:
    """
    Change wiring schematics from part one, now it's a list of 0/1 vectors for the positions
    in that schematic, instead of a list of indices.
    """
    first_space_index = line.index(" ")
    light_diagram = tuple(0 if x == "." else 1 for x in line[1:first_space_index - 1])

    first_brace_index = line.index("{")
    wiring_substring = line[first_space_index + 1:first_brace_index - 1]
    wiring_substring_no_parens = "".join([c for c in wiring_substring if c not in "()"])
    wiring_schematic_values = tuple(
        tuple(int(x) for x in part.split(","))
        for part in wiring_substring_no_parens.split(" ")
    )
    wiring_schematics = tuple(
        tuple(int(i in x) for i in range(len(light_diagram)))
        for x in wiring_schematic_values
    )

    joltage_substring = line[first_brace_index + 1:-1]
    joltage_requirements = tuple(int(x) for x in joltage_substring.split(","))

    return Machine(light_diagram, wiring_schematics, joltage_requirements)


def least_button_presses(machine: Machine) -> int:
    """
    State this as a linear programming problem to minimize the number of "button
    presses," sum of coefficients of the wiring schematic vectors, to equal the
    desired vector of joltage requirements.

    Used https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

    Since we are going for equality, A_ub/b_ub and A_eq/b_eq are the same.
    
    Assumes there is an integer solution to the problem.
    """

    wiring_vectors = np.array(machine.wiring_schematics).T
    desired_joltages = np.array(machine.joltage_requirements)

    solution = linprog(
        c=np.ones(wiring_vectors.shape[1]),
        A_ub=wiring_vectors, 
        b_ub=desired_joltages, 
        A_eq=wiring_vectors,
        b_eq=desired_joltages,
        integrality=1 # decision variables are integers
    )

    return int(sum(solution.x))


def main():
    lines = [line.strip() for line in fileinput.input()]

    total_button_presses = 0
    for line in lines:
        machine = line_to_machine(line)
        total_button_presses += least_button_presses(machine)

    print(total_button_presses)


if __name__ == "__main__":
    main()
