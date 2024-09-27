#!/usr/bin/env python

import fileinput

STEPS = 64

# read input into graph ####

lines = [line.strip() for line in fileinput.input()]

# pad the input with a line of rocks so we don't need to check boundaries
row_of_rocks = ["#" for _ in range(len(lines[0]) + 2)]
field = [row_of_rocks]
for line in lines:
    field.append(["#"] + list(line) + ["#"])
field.append(row_of_rocks)

# edges will be a dict with key: "from" vertex label keys and value: list of "to" vertex labels
edges: dict[str, list[str]] = {}
# don't need a full list of vertices, can just keep a list of which ones are currently occupied
occupied_vertices: list[str] = []

for i in range(len(field)):
    for j in range(len(field[0])):
        if field[i][j] != "#":
            label = f"{i},{j}"

            edges[label] = []

            if field[i][j] == "S":
                occupied_vertices.append(label)

            # add edges going N/E/S/W if they aren't rocks
            if field[i - 1][j] != "#":
                edges[label].append(f"{i - 1},{j}")
            if field[i][j + 1] != "#":
                edges[label].append(f"{i},{j + 1}")
            if field[i + 1][j] != "#":
                edges[label].append(f"{i + 1},{j}")
            if field[i][j - 1] != "#":
                edges[label].append(f"{i},{j - 1}")

# set up ####

def take_a_step(occupied_vertices, edges):
    """
    return a list of vertices that are reachable from any of the occupied vertices
    """

    reachable_vertices = []

    for occupied_vertex in occupied_vertices:
        reachable_vertices.extend(edges[occupied_vertex])

    return list(set(reachable_vertices))

def print_field(field, occupied_vertices):
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] != "#":
                if f"{i},{j}" in occupied_vertices:
                    print("O", end="")
                else:
                    print(" ", end="")
            else:
                print("#", end="")
        print()

# take steps ####

print_field(field, occupied_vertices)
for i in range(STEPS):
    occupied_vertices = take_a_step(occupied_vertices, edges)
    print(f"\nAfter step {i+1}, vertices occupied: {len(occupied_vertices)}")
    print_field(field, occupied_vertices)

print(f"\n\n{len(occupied_vertices)}")