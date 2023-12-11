from typing import List

import numpy as np
from scipy.signal import convolve2d

from computer import Computer

def compute(data, x, y):
    mask = np.ones((x, y), dtype=int)
    # for big images, create a mask to find the rough area to search. as we search a 10x10 area
    # if we expand every 10th pixel, we can reduce the search space by a factor of 100
    if x > 1000 or y > 1000:
        mask = np.array([(pos[0] % 10 == 0 and pos[1] % 10 == 0) and Computer(data).compute(list(pos))[0]
                         for pos in np.ndindex(x, y)], dtype=int).reshape((x, y))
        mask = convolve2d(mask, np.ones((20, 20)), mode="same")
    return np.array([mask[pos] and Computer(data).compute(list(pos))[0]
                     for pos in np.ndindex(x, y)], dtype=int).reshape((x, y))


def test_19(data: List[int], level):
    if level:
        a = compute(data, 1100, 700)
        a = a.copy()  # do not modify the original!
        res = [(x, y) for (x, y), _ in np.ndenumerate(a) if np.sum(a[x:x + 100, y:y + 100]) == 100 * 100]
        res = min(res) if res else []
        return res[0] + res[1] * 10_000
    else:
        return np.sum(compute(data, 50, 50))
