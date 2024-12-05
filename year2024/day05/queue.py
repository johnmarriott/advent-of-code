#!/usr/bin/env python

import fileinput
from functools import cmp_to_key

lines = [line.strip() for line in fileinput.input()]

orders = []
updates = []

for line in lines:
    if "|" in line:
        orders.append(list(map(int, line.split("|"))))
    elif "," in line:
        updates.append(list(map(int, line.split(","))))
    # else it's a blank line

def update_compare(a, b):
    """
    helper using `orders` from the problem statement as a comparator 
    used to sort the incorrectly-ordered updates
    """
    if [a, b] in orders:
        return -1
    elif [b, a] in orders:
        return 1
    else:
        return 0

correct_ordered_updates_middle_value_sum = 0
incorrect_ordered_updates_middle_value_sum = 0

for update in updates:
    update_in_correct_order = True
    for i in range(len(update) - 1):
        if not update_in_correct_order:
            break

        for j in range(i + 1, len(update)):
            # index i comes before index j in the given update
            # we want to see if the orders ever show j coming before i
            if [update[j], update[i]] in orders:
                update_in_correct_order = False
    
    if not update_in_correct_order:
        update = sorted(update, key=cmp_to_key(update_compare))

    middle_value = update[len(update) // 2]

    if update_in_correct_order:
        correct_ordered_updates_middle_value_sum += middle_value
    else:
        incorrect_ordered_updates_middle_value_sum += middle_value

print(f"part one: {correct_ordered_updates_middle_value_sum}")
print(f"part two: {incorrect_ordered_updates_middle_value_sum}")
