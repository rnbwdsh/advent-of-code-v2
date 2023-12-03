from typing import List

import numpy as np

from level_annotations import level_ab

def test_02(data: List[str], level):
    dirs = {"forward": 1j, "up": 1, "down": -1}
    pos = aim = 0
    for line in data:
        dire, dist = line.split()
        dire, dist = dirs[dire], int(dist)
        if level:
            if dire.real:
                aim += dist * dire
            else:
                pos += dist + dist * aim * dire
        else:
            pos += dire * dist
    return np.absolute([pos.real, pos.imag]).prod(dtype=int)
