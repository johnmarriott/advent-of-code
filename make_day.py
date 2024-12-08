#!/usr/bin/env python

import os
import sys
from datetime import datetime

import aocd

# assume the script is run from the aoc repository root or in a year directory

if os.path.basename(os.getcwd()) == "advent-of-code":
    os.chdir(f"year{datetime.now().year}")

if not os.path.basename(os.getcwd()).startswith("year"):
    print("Run this script from the root of the advent-of-code repository or from a year's directory.")
    sys.exit(1)

year = os.path.basename(os.getcwd())[4:]

if len(sys.argv) == 1:
    day = datetime.now().strftime("%d")
else:
    day = f"{int(sys.argv[1]):02d}"

day_dir = f"day{day}"
os.makedirs(day_dir, exist_ok=True)
os.chdir(day_dir)

# create input.txt and sample.txt files
# will attempt to populate them below
open("input.txt", "w").close()
open("sample.txt", "w").close()

template_path = os.path.join("..", "..", ".template.py")
destination_path = "1.py"
if os.path.exists(template_path):
    with open(template_path, "r") as src, open(destination_path, "w") as dst:
        dst.write(src.read())

# populate the sample and input files from the AOC page
try:
    puzzle = aocd.get_puzzle(day=int(day), year=int(year))

    with open("input.txt", "w") as f:
        f.write(puzzle.input_data)

    if len(puzzle.examples) == 1:
        with open("sample.txt", "w") as f:
            f.write(puzzle.examples[0].input_data)
    else:
        for i, example in enumerate(puzzle.examples):
            with open(f"sample-{i + 1}.txt", "w") as f:
                f.write(example.input_data)

        # remove the empty sample.txt file
        os.remove("sample.txt")
except: 
    print("Failed to fetch problem input, do you have the AOC_SESSION environemnt variable set?")
