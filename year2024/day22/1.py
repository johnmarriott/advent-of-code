#!/usr/bin/env python

"""
https://adventofcode.com/2024/day/22
"""

import fileinput


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

secret_sum = 0
for monkey_secrets in monkeys_secrets:
    secret_sum += monkey_secrets[-1]
    print(f"{monkey_secrets[0]}: {monkey_secrets[-1]}")

print()
print(secret_sum)
