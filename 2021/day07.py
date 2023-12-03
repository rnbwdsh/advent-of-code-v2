from typing import List

import numpy as np

from level_annotations import level_ab

def distance(n: int, level):
    return n * (n + 1) // 2 if level else n

def test_07(data, level):
    return min([distance(np.abs(data - i), level).sum()
                for i in range(min(data), max(data))])
