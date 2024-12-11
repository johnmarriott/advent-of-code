#!/usr/bin/env python

import fileinput
from functools import cache

BLINKS = 75

@cache
def blink_at_stone(value, blinks_remaining) -> int:
    if blinks_remaining == 0:
        return 1

    if value == 0:
        return blink_at_stone(1, blinks_remaining - 1)

    if len(str(value)) % 2 == 0:
        mid_index = len(str(value)) // 2
        left = int(str(value)[:mid_index])
        right = int(str(value)[mid_index:])

        return blink_at_stone(left, blinks_remaining - 1) + blink_at_stone(right, blinks_remaining - 1)

    else:
        return blink_at_stone(value * 2024, blinks_remaining - 1)

lines = [line.strip() for line in fileinput.input()]
stones = list(map(int, lines[0].split(" ")))

n_stones = 0
for stone in stones:
    n_stones += blink_at_stone(stone, BLINKS)

print(n_stones)
