#!/usr/bin/env python
""" 
Advent of Code 2025 - Day 9, Part 2
https://adventofcode.com/2025/day/9#part2

By plotting, we see that the shape is roughly a circle with a thin horizontal
rectangle cut out of the middle (like pac-man with the mouth almost closed, and
with a rectangle instead of a triangle as the mouth opening).  Assume that if
the top/bottom y-coordinates of a candidate rectangle are on either side of
y=50000 (which is inside the rectangle mouth opening) then the rectangle is not
viable (it is either small, on the right, or will be interrupted by the cut-out
rectangle).

Sort all pairs of given coordinates by the area of the rectangle they would form,
skipping any that violate the above assumption.  Then test each of these in order,
and the first rectangle that is fully contained in the polygon is the winner.
"""


import fileinput
from itertools import combinations, product

from shapely.geometry import box, Point, Polygon


# found by eyeballing the graph of the polygon, see plot-polygon.R
Y_CENTERLINE_COORDINATE = 50000


def sorted_rectangle_areas(polygon: list[tuple[int, int]]) -> list[tuple[tuple[int, int]], int]:
    """
    Return a list of all possible rectangles formed by pairs of coordinates, sorted
    by area in descending order and excludig any rectangles that cross the centerline.
    """

    all_coordinate_pairs = combinations(polygon, 2)

    rectangle_areas = [
        [
            ((x1, y1), (x2, y2)),
            (1 + abs(x1 - x2)) * (1 + abs(y1 - y2)) # pad each "center" out to the full box
        ]
        for (x1, y1), (x2, y2) in all_coordinate_pairs
        if not (
            min(y1, y2) < Y_CENTERLINE_COORDINATE
            and max(y1, y2) > Y_CENTERLINE_COORDINATE
        )
    ]

    return sorted(rectangle_areas, key=lambda x: x[1], reverse=True)


def first_rectangle_contained_in_polygon(
        rectangle_coordinate_areas: list[tuple[tuple[int, int]], int],
        polygon_coordinates: list[tuple[int, int]]
    ) -> int:
    """
    Returns the area of the first rectangle in `rectangle_coordinate_areas` that is fully
    contained in the polygon defined by `polygon_coordinates`.
    """

    polygon = Polygon(polygon_coordinates)

    for rectangle_coordinates, area in rectangle_coordinate_areas:
        (x1, y1), (x2, y2) = rectangle_coordinates

        rectangle = box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        if polygon.contains(rectangle):
            return area


def main():
    lines = [line.strip() for line in fileinput.input()]
    polygon_coordinates = [tuple(map(int, line.split(','))) for line in lines]
    rectangle_coordinate_areas = sorted_rectangle_areas(polygon_coordinates)
    largest_area = first_rectangle_contained_in_polygon(rectangle_coordinate_areas, polygon_coordinates)

    print(largest_area)


if __name__ == "__main__":
    main()
