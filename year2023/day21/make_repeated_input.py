#!/usr/bin/env python

import fileinput

lines = [line.strip() for line in fileinput.input()]
lines_without_start = [line.replace("S", ".") for line in lines]

paddings = [5] # number of paddings around original, so 1 is 3x3, 2 is 5x5, ...

for padding in paddings:
    columns = 2 * padding + 1

    with open(f"input_{columns}x{columns}.txt", "w") as output:

        # top rows
        for _ in range(padding):
            for i in range(len(lines)):
                for _ in range(columns):
                    output.write(lines_without_start[i])
                output.write(f"\n")

        # middle row (with S in middle column)
        for i in range(len(lines)):
            for _ in range(padding):
                output.write(lines_without_start[i])

            output.write(lines[i])

            for _ in range(padding):
                output.write(lines_without_start[i])

            output.write(f"\n")

        # bottom rows
        for _ in range(padding):
            for i in range(len(lines)):
                for _ in range(columns):
                    output.write(lines_without_start[i])
                output.write(f"\n")