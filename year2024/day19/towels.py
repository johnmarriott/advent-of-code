#!/usr/bin/env python

import fileinput
from functools import cache


def parse_input(lines: list[str]) -> tuple[tuple[str], list[str]]:
    towels = tuple(lines[0].split(", "))
    designs = lines[2:]
    return towels, designs

@cache
def n_design_towel_arrangements(towels: tuple[str], design: str) -> int:
    n_arrangements = 0
    for towel in towels:
        if design == "":
            return 1

        if design.startswith(towel):
            n_arrangements += n_design_towel_arrangements(towels, design[len(towel):])

    return n_arrangements


lines = [line.strip() for line in fileinput.input()]
towels, designs = parse_input(lines)
designs_possible = [n_design_towel_arrangements(towels, design) for design in designs]

print(f"part one: {sum([design > 0 for design in designs_possible])}")
print(f"part two: {sum(designs_possible)}")