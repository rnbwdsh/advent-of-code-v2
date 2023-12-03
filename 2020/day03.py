import numpy as np

from level_annotations import level_ab

@level_ab(3)
def solve(data, method=0):
    def sol(data, x_mov, y_mov):
        d = np.array(list(map(list, data.split("\n")))).__eq__('#')
        x = y = cnt = 0
        while True:
            x += x_mov
            y += y_mov
            if x >= d.shape[0]:
                return cnt
            cnt += d[x, y % d.shape[1]]

    if method:
        return np.prod([sol(data, xm, ym) for xm, ym in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]])
    else:
        return sol(data, 1, 3)
