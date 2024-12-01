#!/usr/bin/env python

import fileinput

input = list(fileinput.input())[0].strip()

def unique_window(input, n):
    for i in range(len(input)):
        window = input[i:i+n]
        
        if len(set(window)) == n:
            return i+n

print(f"part one: {unique_window(input, 4)}")
print(f"part two: {unique_window(input, 14)}")
