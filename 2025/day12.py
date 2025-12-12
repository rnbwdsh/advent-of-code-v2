from typing import List

import numpy as np
import pytest


def check(area, counts, shapes) -> int:
    area_a = area[0] * area[1]
    space_per_shape = np.array([s.sum() for s in shapes])
    return sum(space_per_shape * counts) < area_a * 0.85


@pytest.mark.data('''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2''', 2, None)
def test_12(data: List[List[str]], level):
    if level:
        return 0
    shapes = [np.array([list(l) for l in line[1:]], dtype=str) == '#' for line in data[:-1]]
    total = 0
    for line in data[-1]:
        area, *counts = line.split(' ')
        area = [int(i) for i in area[:-1].split("x")]
        counts = np.array([int(c) for c in counts])
        total += check(area, counts, shapes)
    return total