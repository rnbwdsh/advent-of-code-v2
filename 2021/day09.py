from typing import List

import numpy as np

neighbors = lambda i, j: [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

def watershed_size(d, i, j):
    d[i, j] = 9
    return 1 + sum([watershed_size(d, *n) for n in neighbors(i, j) if d[n] != 9])

def test_09(data: List[str], level):
    data = np.pad([[int(i) for i in line] for line in data], (1, 1), constant_values=9)  # pad corner with 9
    h, w = data.shape
    basins = [watershed_size(data, i, j) if level else  # recursive watershedding size algo
              data[i][j] + 1  # risk level = min peak + 1
              for i in range(1, h - 1) for j in range(1, w - 1)  # exclude padding
              if all([data[i][j] < data[n] for n in neighbors(i, j)])]  # all neighbors must be smaller
    return np.prod(sorted(basins)[-3:]) if level else sum(basins)
