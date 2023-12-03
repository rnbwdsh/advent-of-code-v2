from typing import List

import numpy as np

from level_annotations import level_ab

def inner(arr, level):
    for pos in range(arr.shape[1]):
        curr = arr[:, pos].mean(axis=0) >= 0.5  # unlike np.round, round UP on 0.5
        curr = int(curr == level)  # invert for epsilon
        arr = arr[arr[:, pos] == curr]  # filter array at position pos
        if len(arr) == 1:
            return arr[0]

def bin2dec(x):
    return int("".join(map(str, x)), 2)

def test_03(data: List[str], level):
    data = np.array([[int(i) for i in line] for line in data])
    if level:
        return bin2dec(inner(data, 1)) * bin2dec(inner(data, 0))
    else:
        gamma = data.mean(axis=0).round().astype(int)
        epsilon = 1 - gamma  # boolean invert
        return bin2dec(gamma) * bin2dec(epsilon)
