#!/usr/bin/env python

import fileinput

import networkx as nx
from termcolor import cprint


BYTE = "#"
EMPTY = "."
PATH = "O"

def print_memory(field: list[list[str]], path: list[tuple[int, int]]):
    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            if (i, j) in path:
                cprint(PATH, "white", attrs=["bold"], end="")
            else:
                print(cell, end="")
        print()

def make_memory(length: int) -> list[list[str]]:
    # pad with walls
    memory = [[BYTE] * (length + 2)]
    for _ in range(length):
        memory.append([BYTE] + ([EMPTY] * length) + [BYTE])
    memory.append([BYTE] * (length + 2))

    return memory

def add_bytes_to_memory(memory: list[list[str]], lines: list[str], n_bytes: int):
    # add the the first `n_bytes` lines of the input `lines` to memory
    for line in lines[:n_bytes]:
        col, row = map(int, line.split(","))
        memory[row + 1][col + 1] = BYTE

def memory_to_graph(memory: list[list[str]]) -> nx.Graph:
    G = nx.Graph()
    for i, row in enumerate(memory):
        for j, cell in enumerate(row):
            if cell == BYTE:
                continue

            for offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                di, dj = offset
                if memory[i + di][j + dj] != BYTE:
                    G.add_edge((i, j), (i + di, j + dj))

    return G

lines = [line.strip() for line in fileinput.input()]

if lines[0] == "5,4": # sample input
    memory_size = 7
    bytes = 12
else:
    memory_size = 71 # regular input
    bytes = 1024

memory = make_memory(memory_size)
add_bytes_to_memory(memory, lines, bytes)

start = (1, 1)
end = (memory_size, memory_size)
G = memory_to_graph(memory)
shortest_path = nx.shortest_path(G, source=start, target=end)

print_memory(memory, shortest_path)
print(nx.shortest_path_length(G, source=start, target=end))
