#!/usr/bin/env python

import fileinput
from functools import cmp_to_key


# interval_compare and merge_intervals from year2022, day15
def interval_compare(a: tuple[int, int], b: tuple[int, int]) -> int:
    if a[0] < b[0]:
        return -1
    elif a[0] > b[0]:
        return 1
    elif a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    else:
        return 0


# merge ranges - did this in year 2022, day 15 previously
def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals_sorted = sorted(
        [interval for interval in intervals if interval is not None], 
        key=cmp_to_key(interval_compare)
    )

    merged_intervals = set() # in case we add the same one twice in the loop and post-loop
    current_interval = intervals_sorted[0]

    for next_interval in intervals_sorted[1:]:
        if (next_interval[0] <= current_interval[1]
            and current_interval[0] <= next_interval[1]):
            current_interval = (current_interval[0], max(current_interval[1], next_interval[1]))
        else:
            merged_intervals.add(current_interval)
            current_interval = next_interval

    merged_intervals.add(current_interval)
    return sorted(list(merged_intervals))


def parse_lines_to_intervals(lines: list[str]) -> list[tuple[int, int]]:
    intervals = list()

     # file starts with fresh ingredient id ranges, then a blank line, then ignore
    for line in lines:
        if line == "":
            break

        line_parts = line.split("-")
        start_id = int(line_parts[0])
        end_id = int(line_parts[1])

        intervals.append((start_id, end_id))

    return intervals


def main():
    lines = [line.strip() for line in fileinput.input()]

    fresh_ingredient_id_ranges = parse_lines_to_intervals(lines)
    fresh_ingredient_id_ranges_merged = merge_intervals(fresh_ingredient_id_ranges)

    n_available_fresh_ingredients = 0
    for start, end in fresh_ingredient_id_ranges_merged:
        n_available_fresh_ingredients += end - start + 1

    print(n_available_fresh_ingredients)


if __name__ == "__main__":
    main()