from typing import List

import numpy as np

def distance(n: np.ndarray, level):
    return n * (n + 1) // 2 if level else n

def test_07(data: List[int], level):
    data = np.array(data)
    return min([distance(np.abs(data - i), level).sum()
                for i in range(min(data), max(data))])
