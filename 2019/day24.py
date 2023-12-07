


import aocd
import numpy as np

def step(world):
    w = np.zeros_like((world))
    xmax, ymax = world.shape
    score = 0

    for idx, ((x, y), val) in enumerate(np.ndenumerate(world)):
        nsum = sum([world[xp, yp]  # calculate score for 4 neighbors
                    for (xp, yp) in [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]  # calculate neighbors
                    if xp in range(xmax) and yp in range(ymax)])  # bounds check
        w[x, y] = (val and nsum == 1) or (not val and nsum in [1, 2])  # calculate next step field
        score += val * 2 ** idx  # increment total score if bug exists by 2^index
    return w, score

def solve(data):
    world = np.array([list(d) for d in data.split()]) == "#"  # boolean field that's true if "#"
    patterns = set()
    for i in range(100):
        world, score = step(world)
        if score in patterns:
            return score
        else:
            patterns.add(score)

assert solve("""....#
#..#.
#..##
..#..
#....""") == 2129920

aocd.submit(solve(aocd.get_data(day=24)), day=24)




from copy import copy
from collections import defaultdict

CENTER = (2, 2)
SIZE = 5
RS = range(SIZE)
CREATE_EMTPY = lambda: np.zeros((SIZE, SIZE))

def step(worlds):
    w = defaultdict(CREATE_EMTPY)
    xmax, ymax = worlds[0].shape

    for wi, world in copy(worlds).items():
        w[wi] = np.zeros_like(world, dtype=bool)
        for (x, y), val in np.ndenumerate(world):
            if (x, y) == CENTER: continue  # skip center
            nsum = 0  # accumulate number of neighbors into this
            for (xm, ym) in [[0, -1], [0, +1], [-1, 0], [+1, 0]]:  # set neighbor-directions
                xp, yp = x + xm, y + ym  # set neighbors
                if (xp, yp) == CENTER:
                    # if right/left neighbor, take left/right row otherwise top/bot row of recursion depth -1
                    if xm == 1:
                        idx = (0, RS)
                    elif xm == -1:
                        idx = (-1, RS)
                    elif ym == 1:
                        idx = (RS, 0)
                    elif ym == -1:
                        idx = (RS, -1)
                    nsum += worlds[wi - 1][idx].sum()
                elif xp in range(xmax) and yp in range(ymax):
                    nsum += world[xp, yp]
                else:  # outside recursion
                    nsum += worlds[wi + 1][2 + xm, 2 + ym]
            # calculate next time step field
            w[wi][x, y] = (val and nsum == 1) or (not val and (nsum == 1 or nsum == 2))
    return w

def solve(data, steps=200):
    world = np.array([list(d) for d in data.split()]) == "#"  # boolean field that's true if "#"
    worlds = defaultdict(CREATE_EMTPY, {0: world})
    for i in range(steps):
        worlds[min(worlds) - 1]  # expand -1 dim
        worlds[max(worlds) + 1]  # expand +1 dim
        worlds = step(worlds)
        # print(*worlds.items())  # debug output
    return sum([world.sum() for world in worlds.values()])  # sum of all values in all dim

assert solve("""....#
#..#.
#..##
..#..
#....""", 10) == 99

aocd.submit(solve(aocd.get_data(day=24)), day=24)
