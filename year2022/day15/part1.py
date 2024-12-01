#!/usr/bin/env python

"""
There's a closed-form solution to the x-limits of the "exclusion interval" of a sensor
for a given y-value.  This is found by:

- the width of the exclusion interval is max(0, 1 + 2*(distance - abs(y - sensor_y)))
- the exclusion interval is centered at sensor_x

The full exclusion for a y-value is the union of the exclusion intervals of all sensors.

so the big idea is to find the exclusion interval for all sensors at a given height,
take the union, and see how many spaces are taken
"""

from dataclasses import dataclass
import fileinput
from functools import cmp_to_key
import re

ROW_IN_QUESTION = 10 # for sample.txt
# ROW_IN_QUESTION = 2000000 # for input.txt

@dataclass
class Sensor:
    x: int
    y: int
    distance_to_beacon: int

def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

def parse_input(lines: list[str]) -> tuple[list[Sensor], set[tuple[int, int]]]:
    sensors = []
    beacons = set()

    for line in lines:
        sensor_text = line.split(':')[0]
        beacon_text = line.split(':')[1]

        sensor_x = int(re.sub(r".*x=(.*),.*", r"\1", sensor_text))
        sensor_y = int(re.sub(r".*y=(.*)", r"\1", sensor_text))
        beacon_x = int(re.sub(r".*x=(.*),.*", r"\1", beacon_text))
        beacon_y = int(re.sub(r".*y=(.*)", r"\1", beacon_text))

        distance = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)

        sensors.append(Sensor(sensor_x, sensor_y, distance))
        beacons.add((beacon_x, beacon_y))

    return sensors, beacons

def exclusion_interval(sensor: Sensor, y: int) -> tuple[int, int]:
    width = 1 + 2 * (sensor.distance_to_beacon - abs(y - sensor.y))

    if width >= 0:
        return (sensor.x - width//2, sensor.x + width//2)
    else:
        return None # no exclusion at this height

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

if __name__ == '__main__':
    lines = [line.strip() for line in fileinput.input()]
    sensors, beacons = parse_input(lines)

    exclusion_intervals = [exclusion_interval(sensor, ROW_IN_QUESTION) for sensor in sensors]

    # find the union of exclusion intervals by combining any that overlap
    merged_intervals = merge_intervals(exclusion_intervals)

    # subtract any spots where there is already a beacon
    beacons_on_row = [beacon[0] for beacon in beacons if beacon[1] == ROW_IN_QUESTION]

    positions_without_beacons = sum([end - start + 1 for start, end in merged_intervals]) - len(beacons_on_row)

    print(positions_without_beacons)
