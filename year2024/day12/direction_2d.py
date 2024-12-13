from dataclasses import dataclass

@dataclass
class Direction:
    offset: tuple[int, int]
    opposite_direction: "Direction"

directions = {
    "north": Direction((-1, 0), None),
    "east": Direction((0, 1), None),
    "south": Direction((1, 0), None),
    "west": Direction((0, -1), None)
}

directions["north"].opposite_direction = directions["south"]
directions["east"].opposite_direction = directions["west"]
directions["south"].opposite_direction = directions["north"]
directions["west"].opposite_direction = directions["east"]
