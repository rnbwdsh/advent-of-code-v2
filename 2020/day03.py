from typing import List

import numpy as np

def test_03(data: List[str], level):
    def sol(lines, x_mov, y_mov):
        d = np.array([list(d) for d in lines]).__eq__('#')
        x = y = cnt = 0
        while True:
            x += x_mov
            y += y_mov
            if x >= d.shape[0]:
                return cnt
            cnt += d[x, y % d.shape[1]]

    if level:
        return np.prod([sol(data, xm, ym) for xm, ym in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]])
    else:
        return sol(data, 1, 3)
