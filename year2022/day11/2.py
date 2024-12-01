#!/usr/bin/env python

# https://adventofcode.com/2022/day/11#part2

# big idea: throw out multiple of the monkeys' divisors to keep the item values small
# while yielding the same test results

from dataclasses import dataclass
import fileinput
import math

@dataclass 
class Monkey:
    items: list[int]
    operation: any
    test_value: int
    true_receiver: str
    false_receiver: str
    inspections: int

def make_monkey(lines: list[str]) -> Monkey:
    items = [int(item) for item in lines[0].split(":")[1].split(",")]

    operation_text = lines[1].split("=")[1].strip()
    operation = lambda old: eval(operation_text)

    test_value = int(lines[2].split("by")[1].strip())

    true_receiver = int(lines[3].split("monkey")[1].strip()) 
    false_receiver = int(lines[4].split("monkey")[1].strip())
        
    return Monkey(
        items, 
        operation,
        test_value,
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

def run_monkey_round(monkeys: list[Monkey], divisor: int):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            monkey.inspections += 1
            item = monkey.items.pop(0)
            item = monkey.operation(item)

            item = item % (2 * 3 * 5 * 7 * 11 * 13 * 17 * 19) # TODO if this works mod function with amount and calculate this from input

            if item % monkey.test_value == 0:
                monkeys[monkey.true_receiver].items.append(item)
            else:
                monkeys[monkey.false_receiver].items.append(item)

lines = [line.strip() for line in fileinput.input()]
monkeys = make_monkeys(lines)

# to keep numbers small and compatible with the test operations, we will throw out
# the product of the monkeys' divisors
divisor = math.prod([monkey.test_value for monkey in monkeys])

for i in range(10000):
    run_monkey_round(monkeys, divisor)

    # match output of problem statement
    if i in [0, 19, 999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999]:
        print(f"== After round {i + 1} ==")
        for j in range(len(monkeys)):
            print(f"Monkey {j} inspected items {monkeys[j].inspections} times.")
        print()

inspections = [monkey.inspections for monkey in monkeys]
top_two = list(reversed(sorted(inspections)))[0:2]
print(top_two[0] * top_two[1])
