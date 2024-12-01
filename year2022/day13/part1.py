#!/usr/bin/env python

# https://adventofcode.com/2022/day/13

import fileinput
from json import loads

def compare(left: list, right: list) -> int:
    """
    Return the comparison value of the two lists

    Return value is -1 if left is ordered less than the right, 
    0 if the two lists are equal, and 1 if left is ordered greater
    """

    # this looks funny but it leaves the caller's inputs alone
    left = left.copy()
    right = right.copy()

    while len(left) > 0 and len(right) > 0:
        left_value = left.pop(0)
        right_value = right.pop(0)

        if isinstance(left_value, int):
            if isinstance(right_value, int):
                if left_value == right_value:
                    continue
                elif left_value < right_value:
                    return -1
                else:
                    return 1
            else: # left_value is an int, right_value is a list
                comparison = compare([left_value], right_value)
        else: 
            if isinstance(right_value, int):
                comparison = compare(left_value, [right_value])
            else:
                comparison = compare(left_value, right_value)
        
        if comparison != 0:
            return comparison
            
    # if here, one of them is now empty
    if len(left) == 0 and len(right) == 0:
        return 0
    elif len(left) == 0:
        return -1
    else:
        return 1

def main():
    lines = [line.strip() for line in fileinput.input() if len(line.strip()) > 0]

    right_order_indices = []

    for i in range(0, len(lines), 2):
        left = loads(lines[i])
        right = loads(lines[i + 1])
        index = (i // 2) + 1

        if compare(left, right) == -1:
            right_order_indices.append(index)

    print(sum(right_order_indices))

if __name__ == "__main__":
    main()