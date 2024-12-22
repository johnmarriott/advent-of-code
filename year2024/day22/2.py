#!/usr/bin/env python

"""
https://adventofcode.com/2024/day/22#part2

brute force, pretty slow

take every possible sequence of four price changes, then for each monkey's price changes,
see if that occurs for that monkey and if so which price it corresponds to.  Take the max
price across all monkeys
"""

from dataclasses import dataclass
import fileinput


@dataclass
class PriceAndChanges:
    price: int
    preceding_changes: tuple[int]

    def __repr__(self) -> str:
        return f"{self.preceding_changes} -> {self.price}"

def mix(a: int, b: int) -> int:
    return a ^ b

def prune(secret: int) -> int:
    return secret % 16777216

def next_secret_nummber(secret: int) -> int:
    secret = mix(secret * 64, secret)
    secret = prune(secret)

    secret = mix(secret // 32, secret)
    secret = prune(secret)

    secret = mix(secret * 2048, secret)
    secret = prune(secret) 

    return secret


monkeys_secrets = [[int(line.strip())] for line in fileinput.input()]

for _ in range(2000): 
    for monkey_secrets in monkeys_secrets:
        monkey_secrets.append(next_secret_nummber(monkey_secrets[-1]))

monkeys_prices = [
    [x % 10 for x in monkey_secrets]
    for monkey_secrets 
    in monkeys_secrets
]

monkeys_price_changes = [
    [current - previous for previous, current in zip(monkey_prices, monkey_prices[1:])]
    for monkey_prices
    in monkeys_prices
]

# look at all possible runs of four price changes
monkeys_prices_and_changes: list[list[PriceAndChanges]] = []
for monkey_index in range(len(monkeys_prices)):
    monkey_prices_and_changes = []
    for i in range(4, len(monkeys_prices[monkey_index])):
        price = monkeys_prices[monkey_index][i]
        preceding_changes = tuple(monkeys_price_changes[monkey_index][i-4:i])
        monkey_prices_and_changes.append(PriceAndChanges(price, preceding_changes))

    monkeys_prices_and_changes.append(monkey_prices_and_changes)

# all runs of four price changes across all monkeys
all_price_changes: set[tuple[int]] = {
    price_change.preceding_changes
    for monkey_prices_and_changes in monkeys_prices_and_changes
    for price_change in monkey_prices_and_changes
}        

max_profit = 0
for price_change in all_price_changes:
    profit = 0

    for monkey_price_and_changes in monkeys_prices_and_changes:
        # if this monkey has this run of price changes, add the price of the first
        # occrrence of this run of price changes to this run's total profit
        first_match = next((x for x in monkey_price_and_changes if x.preceding_changes == price_change), None)

        if first_match is not None:
            profit += first_match.price

    max_profit = max(max_profit, profit)

print(max_profit)
