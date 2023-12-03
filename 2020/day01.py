import itertools

import numpy as np

from level_annotations import level_ab

@level_ab(1, apply=int, sep="\n")
def solve(data, level):
    data = sorted(data)
    for line in itertools.product(data, repeat=level + 2):
        if np.sum(line) == 2020:
            return np.prod(line)
