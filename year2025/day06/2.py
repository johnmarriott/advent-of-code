#!/usr/bin/env python
"""
Advent of Code - 2025 Day 6, Part 2
https://adventofcode.com/2025/day/6#part2

Scan the operator (last) line to get the operators and widths, then process the input values
using the known widths.  Could be improved by not modifying the input lines in place.
"""


import fileinput
from functools import reduce
from operator import add, mul


def operator_line_to_operators_and_widths(operator_line: str) -> tuple[list[str], list[int]]:
    operators = []
    input_widths = []

    # The line starts with the first operator: trim it off the front of the string
    # and count how many spaces there are until the next operator: this is the width
    # of this column.
    #
    # If it's the last column, there are only spaces remaining in the string, and
    # that width + 1 is the width of the last column.
    while len(operator_line) > 0:
        operators.append(operator_line[0])
        operator_line = operator_line[1:]

        if operator_line.isspace():
            # this was the last operator
            input_widths.append(len(operator_line) + 1)
            break

        # count spaces until the next operator
        current_width = 0
        while len(operator_line) > 0 and operator_line[0] == " ":
            current_width += 1
            operator_line = operator_line[1:]

        input_widths.append(current_width)

    return operators, input_widths


def problem_value(lines: list[str], operator: str, input_width: int) -> int:
    """
    Calculates the value of the math problem for the given operator and input width.
    Modifies `lines` in place: the first `input_width` + 1 characters of each line are removed.
    """

    # grab the first `input_width` characters of each line as the problem inputs, and trim them 
    # from the lines (for successive calls)
    input_characters = [line[0:input_width] for line in lines]
    for i in range(len(lines)):
        lines[i] = lines[i][input_width + 1 :]

    # transpose the input characters to get the values for this problem
    values = [[input_characters[i][j] for i in range(len(input_characters))] for j in range(input_width)]
    problem_values = [int("".join(x).strip()) for x in values]

    operation = add if operator == "+" else mul
    return reduce(operation, problem_values)


def main():
    lines = [line for line in fileinput.input()]
    operator_line = lines.pop()

    operators, input_widths = operator_line_to_operators_and_widths(operator_line)

    math_problem_sum = 0
    for i in range(len(operators)):
        math_problem_sum += problem_value(lines, operators[i], input_widths[i])

    print(math_problem_sum)


if __name__ == "__main__":
    main()
