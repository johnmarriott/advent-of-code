#!/usr/bin/env python

# https://adventofcode.com/2022/day/11

import fileinput
from dataclasses import dataclass

@dataclass 
class Monkey:
    items: list[int]
    operation: any
    test: any 
    true_receiver: str
    false_receiver: str
    inspections: int

def make_monkey(lines: list[str]) -> Monkey:
    items = [int(item) for item in lines[0].split(":")[1].split(",")]

    operation_text = lines[1].split("=")[1].strip()
    operation = lambda old: eval(operation_text)

    test_value = int(lines[2].split("by")[1].strip())
    test = lambda x: x % test_value == 0

    true_receiver = int(lines[3].split("monkey")[1].strip()) 
    false_receiver = int(lines[4].split("monkey")[1].strip())
        
    return Monkey(
        items, 
        operation,
        test,
        true_receiver, 
        false_receiver,
        0
    )

def make_monkeys(lines: list[str]) -> list[Monkey]:
    monkeys: list[Monkey] = []

    for i in range(len(lines)):
        if lines[i].startswith("Monkey"):
            monkey_lines = lines[i+1 : i+6]
            monkeys.append(make_monkey(monkey_lines))

    return monkeys

def run_monkey_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            monkey.inspections += 1
            item = monkey.items.pop(0)
            item = monkey.operation(item)
            item = item // 3

            if monkey.test(item):
                monkeys[monkey.true_receiver].items.append(item)
            else:
                monkeys[monkey.false_receiver].items.append(item)

lines = [line.strip() for line in fileinput.input()]
monkeys = make_monkeys(lines)

for _ in range(20):
    run_monkey_round(monkeys)

inspections = [monkey.inspections for monkey in monkeys]
top_two = list(reversed(sorted(inspections)))[0:2]
print(top_two[0] * top_two[1])
