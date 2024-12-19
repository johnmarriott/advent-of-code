#!/usr/bin/env python

import fileinput

import networkx as nx


BYTE = "#"
EMPTY = "."

def make_memory(length: int) -> list[list[str]]:
    # pad with walls
    memory = [[BYTE] * (length + 2)]
    for _ in range(length):
        memory.append([BYTE] + ([EMPTY] * length) + [BYTE])
    memory.append([BYTE] * (length + 2))

    return memory

def memory_paths_to_graph(memory: list[list[str]]) -> nx.Graph:
    G = nx.Graph()
    for i, row in enumerate(memory):
        for j, cell in enumerate(row):
            if cell == BYTE:
                continue
            if memory[i - 1][j] != BYTE:
                G.add_edge((i, j), (i - 1, j))
            if memory[i + 1][j] != BYTE:
                G.add_edge((i, j), (i + 1, j))
            if memory[i][j - 1] != BYTE:
                G.add_edge((i, j), (i, j - 1))
            if memory[i][j + 1] != BYTE:
                G.add_edge((i, j), (i, j + 1))

    return G


lines = [line.strip() for line in fileinput.input()]

if lines[0] == "5,4": # sample input
    memory_size = 7
else:
    memory_size = 71 # regular input

memory = make_memory(memory_size)
start = (1, 1)
end = (memory_size, memory_size)

# make a graph with no bytes blocking paths yet, so all adjacent
# cells share edges
#
# then remove vertices one at a time from input (also removing edges)
# until there is no path from start to end
#
# since the answer is close to the end of the input, it may be faster
# to start with a fully-blocked graph and add vertices back in from the
# end of the input to the start, but this works

G = memory_paths_to_graph(memory)

for line in lines:
    col, row = map(int, line.split(","))

    G.remove_node((row + 1, col + 1))

    if not nx.has_path(G, source=start, target=end):
        print(line)
        break
