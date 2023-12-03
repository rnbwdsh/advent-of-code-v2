from typing import List

import numpy as np

from level_annotations import level_ab

def test_01(data: List[int], level):
    data = np.array(data)
    if level:
        data = data[2:] + data[1:-1] + data[:-2]  # 3-frame-windowing
    return ((data[1:] - data[:-1]) > 0).sum()
