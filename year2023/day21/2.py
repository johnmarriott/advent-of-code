""" 
Idea: it's a fact (thanks to hints) that the a function that's a closed-form
solution (f: steps -> paths) to this is quadratic.

Use solution to part 1 to get three pairs of (steps, plots) to fit the solution to.

Since the final number of steps is 131*n + 65, where n is even,
we will find steps for n = 0, 2, 4, i.e., steps = 65, 327, 589.

We need to append copies of the field to itself to take these steps.  Since
there is a clear path N/E/S/W from the start, the 65th step will go into the
first cell of "ring two" of the appended fields.  

Use make_repeated_input.py to make an "infinite" field large enough for this,
then call the day 1 solution with the values of steps_1, steps_2, and steps_3 as
the STEPS value in that file to get the values of paths_1, paths_2, and paths_3.
Then run this script to get the answer.
"""

import numpy as np

steps_1 = 65
paths_1 = 3738

steps_2 = 327
paths_2 = 92194

steps_3 = 589
paths_3 = 298218

a = np.array([
    [steps_1 * steps_1, steps_1, 1], 
    [steps_2 * steps_2, steps_2, 1], 
    [steps_3 * steps_3, steps_3, 1], 
])
b = np.array([
    paths_1,
    paths_2,
    paths_3
])
x = np.linalg.solve(a, b)

steps_final = 26501365

print(x[0] * steps_final * steps_final + x[1] * steps_final + x[2])