# https://adventofcode.com/2022/day/2

import fileinput

tool_points = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

outcome_points = {
    "lose": 0,
    "draw": 3,
    "win": 6
}

# A, B, C are rock, paper, scissors
# X, Y, Z are rock, paper, scissors
# outcome is if opponent plays A, B, C and I play X, Y, Z
outcomes = {
    "A": {
        "X": "draw", 
        "Y": "win",
        "Z": "lose"
    },
    "B": {
        "X": "lose",
        "Y": "draw",
        "Z": "win"
    },
    "C": {
        "X": "win",
        "Y": "lose",
        "Z": "draw"
    }
}

plays = [line.strip() for line in fileinput.input()]

score = 0

for play in plays:
    opponent_tool = play[0]
    my_tool = play[2]

    score += tool_points[my_tool] + outcome_points[outcomes[opponent_tool][my_tool]]

print(score)
