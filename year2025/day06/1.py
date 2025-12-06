#!/usr/bin/env python
"""
Advent of Code - 2025 Day 6, Part 1
https://adventofcode.com/2025/day/6
"""

import fileinput
from functools import reduce
from operator import add, mul


lines = [line.strip().split() for line in fileinput.input()]

math_problem_sum = 0

for i in range(len(lines[0])):
    problem_inputs = [line[i] for line in lines]
    problem_values = [int(x) for x in problem_inputs[0:-1]]
    problem_operator = problem_inputs[-1]

    operation = add if problem_operator == "+" else mul

    math_problem = reduce(operation, problem_values)
    math_problem_sum += math_problem

print(math_problem_sum)
