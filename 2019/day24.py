from collections import defaultdict
from copy import copy

import numpy as np

def step0(world):
    w = np.zeros_like(world)
    x_max, y_max = world.shape
    score = 0

    for idx, ((x, y), val) in enumerate(np.ndenumerate(world)):
        n_sum = 0
        for (xp, yp) in [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]:
            if xp in range(x_max) and yp in range(y_max):
                n_sum += world[xp, yp]
        w[x, y] = (val and n_sum == 1) or (not val and n_sum in [1, 2])  # calculate next step field
        score += val * 2 ** idx  # increment total score if bug exists by 2^index
    return w, score

def step1(worlds):
    w = defaultdict(lambda: np.zeros((5, 5)))
    x_max, y_max = worlds[0].shape
    idx = 0

    for wi, world in copy(worlds).items():
        w[wi] = np.zeros_like(world, dtype=bool)
        for (x, y), val in np.ndenumerate(world):
            if (x, y) == (2, 2): continue  # skip center
            n_sum = 0  # accumulate number of neighbors into this
            for (xm, ym) in [[0, -1], [0, +1], [-1, 0], [+1, 0]]:  # set neighbor-directions
                xp, yp = x + xm, y + ym  # set neighbors
                if (xp, yp) == (2, 2):
                    # if right/left neighbor, take left/right row otherwise top/bot row of recursion depth -1
                    if xm == 1:
                        idx = (0, range(5))
                    elif xm == -1:
                        idx = (-1, range(5))
                    elif ym == 1:
                        idx = (range(5), 0)
                    elif ym == -1:
                        idx = (range(5), -1)
                    n_sum += worlds[wi - 1][idx].sum()
                elif xp in range(x_max) and yp in range(y_max):
                    n_sum += world[xp, yp]
                else:  # outside recursion
                    n_sum += worlds[wi + 1][2 + xm, 2 + ym]
            # calculate next time step field
            w[wi][x, y] = (val and n_sum == 1) or (not val and (n_sum == 1 or n_sum == 2))
    return w

def test_24(data: np.ndarray, level):
    data = np.equal(data, "#")  # boolean field that's true if "#"
    if level:
        worlds = defaultdict(lambda: np.zeros((5, 5)), {0: data})
        is_testcase = "".join(map(str, data.flatten().astype(int))) == '0000110010100110010010000'
        for _ in range(10 if is_testcase else 200):
            worlds[min(worlds) - 1] = np.zeros((5, 5))  # expand -1 dim
            worlds[max(worlds) + 1] = np.zeros((5, 5))  # expand +1 dim
            worlds = step1(worlds)
        return sum([world.sum() for world in worlds.values()])  # sum of all values in all dim
    else:
        seen = set()
        while True:
            data, score = step0(data)
            if score in seen:
                break
            seen.add(score)
        return score
