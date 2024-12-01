#!/usr/bin/env python

"""
Use part 1, then truncate the merged intervals to (0, max coordinate) and
stop if there are two intervals after merging

This isn't elegant, but it runs in about 30 seconds
"""

import fileinput

from part1 import Sensor, parse_input, exclusion_interval, merge_intervals

MAX_COORDINATE = 4000000 

def exclusion_interval_truncated(sensor: Sensor, y: int) -> tuple[int, int]:
    interval = exclusion_interval(sensor, y)

    if interval is not None:
        min_x, max_x = interval
        return (max(0, min_x), min(MAX_COORDINATE, max_x))
    else:
        return None

lines = [line.strip() for line in fileinput.input()]
sensors, beacons = parse_input(lines)

def combine_adjacent_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    After merging intervals, can end up with intervals like [(1, 2), (3, 4)] and since these
    coordinates are for blocks, these exclusion intervals exclude all of the blocks from 1 to 4
    inclusive, so we can combine them into a single interval (1, 4)

    Assumes input is sorted (it is from merge_intervals)
    """

    combined_intervals = set()
    current_interval = intervals[0]

    for next_interval in intervals[1:]:
        if next_interval[0] == current_interval[1] + 1:
            current_interval = (current_interval[0], next_interval[1])
        else:
            combined_intervals.add(current_interval)
            current_interval = next_interval

    combined_intervals.add(current_interval)

    return sorted(list(combined_intervals))

def tuning_frequency(x: int, y: int) -> int:
    return 4000000 * x + y

for row in range(MAX_COORDINATE):
    exclusion_intervals = [exclusion_interval_truncated(sensor, row) for sensor in sensors]

    merged_intervals = merge_intervals(exclusion_intervals)

    combined_intervals = combine_adjacent_intervals(merged_intervals)

    # according to problem statement, there should be exactly one line where the interval
    # is not [0, MAX_COORDINATE - 1], which could be one of:
    #
    # - interval starts at 1 (instead of 0)
    # - interval ends at MAX_COORDINATE - 1 (instead of MAX_COORDINATE)
    # - there are two intervals, [a, b] and [c, d], with one space between b and c

    free_position = None

    if len(combined_intervals) > 1:
        free_position = combined_intervals[0][1] + 1
    elif combined_intervals[0][0] == 1:
        free_position = 1
    elif combined_intervals[0][1] == MAX_COORDINATE - 1:
        free_position = MAX_COORDINATE - 1

    if free_position is not None:
        print(f"{combined_intervals} at {row}")
        print(tuning_frequency(free_position, row))
        break

