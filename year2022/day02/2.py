# https://adventofcode.com/2022/day/2

import fileinput

tool_points = {
    "A": 1,
    "B": 2,
    "C": 3
}

outcome_points = {
    "lose": 0,
    "draw": 3,
    "win": 6
}

# A, B, C are opponent playing rock, paper, scissors
# X, Y, Z are my outcomes: lose, draw, win
# response is the tool I should play (A, B, or C) and the match outcome
responses = {
    "A": {
        "X": ("C", "lose"), 
        "Y": ("A", "draw"),
        "Z": ("B", "win")
    },
    "B": {
        "X": ("A", "lose"),
        "Y": ("B", "draw"),
        "Z": ("C", "win")
    },
    "C": {
        "X": ("B", "lose"),
        "Y": ("C", "draw"),
        "Z": ("A", "win")
    }
}

plays = [line.strip() for line in fileinput.input()]

score = 0

for play in plays:
    opponent_tool = play[0]
    my_tool = play[2]

    response = responses[opponent_tool][my_tool]

    score += tool_points[response[0]] + outcome_points[response[1]]

print(score)
