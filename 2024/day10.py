import numpy as np
import pytest


def follow_trail(x, y, data):
    curr = data[x, y]
    if curr == 9:
        yield (x, y)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= data.shape[0] or ny >= data.shape[1]:
            continue
        if data[nx, ny] == curr + 1:
            yield from follow_trail(nx, ny, data)


@pytest.mark.data(("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""), 36, 81)
def test_09(data: np.ndarray, level):
    data = np.array(data, dtype=np.int16)
    agg_func = list if level else set
    return sum(len((agg_func(follow_trail(x, y, data))))
               for x, y in zip(*np.where(data==0)))
