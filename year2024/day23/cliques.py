#!/usr/bin/env python

import fileinput

import networkx as nx


lines = [line.strip() for line in fileinput.input()]

G = nx.Graph()
for line in lines:
    a, b = line.split("-")
    G.add_edge(a, b)

cliques = nx.enumerate_all_cliques(G)

n_t_cliques = 0
max_clique_size = 0
max_clique = None

for clique in cliques:
    if len(clique) == 3 and any(c[0] == "t" for c in clique):
        n_t_cliques += 1

    if len(clique) > max_clique_size:
        max_clique_size = len(clique)
        max_clique = clique

print(f"part one: {n_t_cliques}")
print(f'part two: {",".join(sorted(max_clique))}')
