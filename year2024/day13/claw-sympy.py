#!/usr/bin/env python

from dataclasses import dataclass
import fileinput

from sympy import Matrix, linsolve, symbols

@dataclass
class Coordinate:
    x: int
    y: int

@dataclass
class Machine:
    button_a: Coordinate
    button_b: Coordinate
    prize: Coordinate

def solve_machine(machine: Machine, addend: int = 0) -> tuple[float, float]:
    x, y = symbols("x, y")
    A = Matrix([[machine.button_a.x, machine.button_b.x], [machine.button_a.y, machine.button_b.y]])
    b = Matrix([machine.prize.x + addend, machine.prize.y + addend])
    solution = linsolve((A, b), [x, y])

    return(solution.args[0][0], solution.args[0][1])

def parse_machines(lines: list[str]) -> list[Machine]:
    machines: list[Machine] = []

    for line in lines:
        if len(line) == 0:
            continue

        x = int("".join([x for x in line.split(",")[0] if x.isdigit()]))
        y = int("".join([x for x in line.split(",")[1] if x.isdigit()]))

        if line.startswith("Button A:"):
            button_a = Coordinate(x, y)

        if line.startswith("Button B:"):
            button_b = Coordinate(x, y)

        if line.startswith("Prize:"):
            prize = Coordinate(x, y)
            machines.append(Machine(button_a, button_b, prize))
    
    return machines


lines = [line.strip() for line in fileinput.input()]
machines = parse_machines(lines)

for addend in [0, 10000000000000]:
    prize_cost = 0
    for machine in machines:
        solution_a, solution_b = solve_machine(machine, addend)

        # check for integer counts of button presses
        # no need to check if <=100 presses for part one
        if (int(solution_a) == solution_a and int(solution_b) == solution_b):
            prize_cost += 3 * solution_a + solution_b

    print(f"part {'one' if addend == 0 else 'two'}: {prize_cost}")
