#!/usr/bin/env python

import fileinput
import itertools

def line_calibration_result(line: str) -> int:
    """Value of the line if it's feasible, zero otherwise"""
    desired_value = int(line.split(":")[0])
    operands = list(map(int, line.split(":")[1].strip().split(" ")))
    
    operator_permutations = list(itertools.product(["+", "*", "|"], repeat=len(operands) - 1))

    for operator_permutation in operator_permutations:
        computed_value = operands[0]
        for i, operator in enumerate(operator_permutation):
            if operator == "+":
                computed_value += operands[i + 1]
            elif operator == "*":
                computed_value *= operands[i + 1]
            else:
                computed_value = int(str(computed_value) + str(operands[i + 1]))

        if computed_value == desired_value:
            return desired_value
        
    return 0

lines = [line.strip() for line in fileinput.input()]

print(sum([line_calibration_result(line) for line in lines]))
