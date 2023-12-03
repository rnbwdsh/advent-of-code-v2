import re

import numba
import numpy as np

@numba.njit()
def simulate(x1, x2, y1, y2, limit=200):
    res = []
    for idx in numba.prange(1, limit):
        for idy in range(-limit, limit):
            dx, dy = idx, idy  # create copy, to not modify the loop var
            x, y, y_max = 0, 0, 0
            while x < x2 and y > y1 and not (dx == 0 and not (x1 <= x <= x2)):
                x += dx
                y += dy
                y_max = max(y_max, y)
                dx -= np.sign(dx)
                dy -= 1
                if x1 <= x <= x2 and y1 <= y <= y2:
                    res.append(y_max)
                    break
    return res

def test_17(data, level):
    high = list(simulate(*map(int, re.findall("-?\\d+", data[0]))))
    return len(high) if level else max(high)
