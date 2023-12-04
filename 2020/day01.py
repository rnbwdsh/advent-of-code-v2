import itertools
from typing import List

import numpy as np

def test_01(data: List[int], level):
    data = sorted(data)
    for line in itertools.product(data, repeat=level + 2):
        if np.sum(line) == 2020:
            return np.prod(line)
