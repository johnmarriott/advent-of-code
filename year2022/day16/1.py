#!/usr/bin/env python

"""
big idea

draw this as a graph, where each valve vertex, and at a vertex you can stay there to open it

weights between edges are 1, the time to travel between them / open the valve

each vertex has a value, the flow rate * (MAX_STEPS - steps taken)

The given valves (say, XX) are called XX_closed.  The open version of the valve is called XX_open.

Map out the graph, then keep state as a tuple of which valves are open so that they can be
passed around in recursion



"""

from dataclasses import dataclass
import fileinput

MAX_STEPS = 30

lines = [line.strip() for line in fileinput.input()]

@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    neighbors: list[str]

@dataclass
class Step:
    from_valve: str
    to_valve: str
    pressure_released: int
    index: int

    def __str__(self):
        return f"{self.from_valve} → {self.to_valve} ({self.pressure_released})"

def parse_valves(lines: list[str]) -> dict[str, Valve]:
    valves = {}

    for index, line in enumerate(lines):
        name = line[6:8] # names are all two letters in this problem
        flow_rate = int(line.split("=")[1].split(";")[0])
        neighbors_text = line.split("valve")[1]
        if neighbors_text.startswith("s"):
            neighbors_text = neighbors_text[1:]

        neighbors = [neighbor.strip() for neighbor in neighbors_text[1:].split(",")]

        valves[name] = Valve(name, flow_rate, neighbors, index)

    return valves

def find_path(valves: list[Valve], current_valve: Valve, open_valves: tuple[str], pressure_released: int, steps_taken: int) -> int:
    """
    Recursively find the path that releases the most pressure, returns the pressure released
    """
    if steps_taken == MAX_STEPS:
        return pressure_released

    best_path = None
    best_pressure_released = 0

    # take the path of opening this valve then moving
    if current_valve.name not in open_valves:
        best_path = find_path(
            valves,
            current_valve, 
            open_valves + [current_valve.name]
        )
        best_pressure_released = path_pressure_released(best_path)

    for neighbor in current_valve.neighbors:
        neighbor_path = find_path(
            valves[neighbor], 
            path + [Step(current_valve.name, neighbor, valves[neighbor].flow_rate)], 
            open_valves + [current_valve.name]
        )

        if path_pressure_released(neighbor_path) > best_pressure_released:
            best_path = neighbor_path
            best_pressure_released = path_pressure_released(neighbor_path)

            #print(f"new best path with {best_pressure_released}: {best_path}")
            #input()


    return best_path

valves = parse_valves(lines)
print(find_path(valves, 0, (0,) * len(valves), 0, 0))