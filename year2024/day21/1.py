#!/usr/bin/env python

""" 
https://adventofcode.com/2024/day/21

Robot would prefer to do the same motion consecutively, e.g., up left up is 
more expensive in key presses than up up left.  So consider all alternatives
when there are "equal" paths like those.
"""


import fileinput
from functools import cache

import networkx as nx


def code_to_number(code: str) -> int:
    return int(code[0:3])

def numeric_keypad_graph() -> nx.DiGraph:
    keypad = nx.DiGraph()

    keypad.add_edge("7", "8", weight=1, label=">")
    keypad.add_edge("7", "4", weight=1, label="v")

    keypad.add_edge("8", "7", weight=1, label="<")
    keypad.add_edge("8", "9", weight=1, label=">")
    keypad.add_edge("8", "5", weight=1, label="v")

    keypad.add_edge("9", "8", weight=1, label="<")
    keypad.add_edge("9", "6", weight=1, label="v")

    keypad.add_edge("4", "7", weight=1, label="^")
    keypad.add_edge("4", "5", weight=1, label=">")
    keypad.add_edge("4", "1", weight=1, label="v")

    keypad.add_edge("5", "8", weight=1, label="^")
    keypad.add_edge("5", "4", weight=1, label="<")
    keypad.add_edge("5", "6", weight=1, label=">")
    keypad.add_edge("5", "2", weight=1, label="v")

    keypad.add_edge("6", "9", weight=1, label="^")
    keypad.add_edge("6", "5", weight=1, label="<")
    keypad.add_edge("6", "3", weight=1, label="v")

    keypad.add_edge("1", "4", weight=1, label="^")
    keypad.add_edge("1", "2", weight=1, label=">")

    keypad.add_edge("2", "5", weight=1, label="^")
    keypad.add_edge("2", "1", weight=1, label="<")
    keypad.add_edge("2", "3", weight=1, label=">")
    keypad.add_edge("2", "0", weight=1, label="v")

    keypad.add_edge("3", "6", weight=1, label="^")
    keypad.add_edge("3", "2", weight=1, label="<")
    keypad.add_edge("3", "A", weight=1, label="v")

    keypad.add_edge("0", "2", weight=1, label="^")
    keypad.add_edge("0", "A", weight=1, label=">")

    keypad.add_edge("A", "3", weight=1, label="^")
    keypad.add_edge("A", "0", weight=1, label="<")

    return keypad

def arrow_keypad_graph() -> nx.DiGraph:
    keypad = nx.DiGraph()

    keypad.add_edge("^", "A", weight=1, label=">")
    keypad.add_edge("^", "v", weight=1, label="v")

    keypad.add_edge("A", "^", weight=1, label="<")
    keypad.add_edge("A", ">", weight=1, label="v")
    
    keypad.add_edge("<", "v", weight=1, label=">")

    keypad.add_edge("v", "<", weight=1, label="<")
    keypad.add_edge("v", "^", weight=1, label="^")
    keypad.add_edge("v", ">", weight=1, label=">")

    keypad.add_edge(">", "A", weight=1, label="^")
    keypad.add_edge(">", "v", weight=1, label="<")

    return keypad

@cache
def move_numeric_keypad(current_digit: str, next_digit: str) -> int:
    """
    returns the number of human key presses needed to move the numeric
    keypad from current_digit to next_digit 
    """

    current_first_arrow_keypad = "A"
    min_cost = float("inf")

    paths = nx.all_shortest_paths(numeric_keypad, current_digit, next_digit)

    for path in paths:
        path_cost = 0
        first_arrow_keypad_code = [
            numeric_keypad[numeric_keypad_step[0]][numeric_keypad_step[1]]["label"] 
            for numeric_keypad_step 
            in zip(path, path[1:])
        ] + ["A"]

        for next_first_arrow_keypad in first_arrow_keypad_code:
            path_cost += move_first_arrow_keypad(current_first_arrow_keypad, next_first_arrow_keypad)
            current_first_arrow_keypad = next_first_arrow_keypad

        min_cost = min(min_cost, path_cost)

    return min_cost

@cache
def move_first_arrow_keypad(current_digit: str, next_digit: str) -> int:
    """
    returns the number of human key presses needed to move the first
    arrow keypad from current_digit to next_digit 
    """

    current_second_arrow_keypad = "A"
    min_cost = float("inf")

    paths = nx.all_shortest_paths(arrow_keypad, current_digit, next_digit)

    for path in paths:
        path_cost = 0

        second_arrow_keypad_code = [
            arrow_keypad[first_arrow_keypad_step[0]][first_arrow_keypad_step[1]]["label"]
            for first_arrow_keypad_step
            in zip(path, path[1:])
        ] + ["A"]

        for next_second_arrow_keypad in second_arrow_keypad_code:
            path_cost += move_second_arrow_keypad(current_second_arrow_keypad, next_second_arrow_keypad)
            current_second_arrow_keypad = next_second_arrow_keypad

        min_cost = min(min_cost, path_cost)

    return min_cost

@cache
def move_second_arrow_keypad(current_digit: str, next_digit: str) -> int:
    """
    returns the number of human key presses needed to move the second
    arrow keypad from current_digit to next_digit 
    """

    min_cost = float("inf")

    paths = nx.all_shortest_paths(arrow_keypad, current_digit, next_digit)

    for path in paths:
        human_arrow_keypad_code = [
            arrow_keypad[second_arrow_keypad_step[0]][second_arrow_keypad_step[1]]["label"]
            for second_arrow_keypad_step
            in zip(path, path[1:])
        ] + ["A"]

        min_cost = min(min_cost, len(human_arrow_keypad_code))

    return min_cost


codes = [line.strip() for line in fileinput.input()]

numeric_keypad = numeric_keypad_graph()
arrow_keypad = arrow_keypad_graph()

numeric_keypad_current_digit = "A"
first_arrow_keypad_current_digit = "A"
second_arrow_keypad_current_digit = "A"

code_costs = []
for code in codes:
    code_cost = 0
    for digit in code:
        code_cost += move_numeric_keypad(numeric_keypad_current_digit, digit)
        numeric_keypad_current_digit = digit

    code_costs.append(code_cost)

sum_complexity = 0
for i in range(len(code_costs)):
    sum_complexity += code_costs[i] * code_to_number(codes[i])

print(sum_complexity)
