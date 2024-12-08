from multiprocessing import Pool
from typing import List

import numba
import numpy as np
import pytest


@numba.jit
def follow_path(data: np.array, pos: complex, dir: complex) -> int:
    seen = set()
    seen_dir = set()
    for step in range(10_000):
        seen.add(pos)
        if (pos, dir) in seen_dir:
            return -1
        seen_dir.add((pos, dir))
        npos = pos + dir
        if npos.real < 0 or npos.real >= data.shape[0] or npos.imag < 0 or npos.imag >= data.shape[1]:
            break
        if data[int(npos.real), int(npos.imag)] == "#":
            dir *= -1j
        else:
            pos = npos
    return len(seen)

def process_position(args):
    data, pos, dir, i, j = args
    dc = data.copy()
    dc[j, i] = "#"
    return follow_path(dc, pos, dir)

@pytest.mark.data(("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""), 41, 6)
def test_06(data: np.array, level):
    pos = np.where(data == "^")
    pos = pos[0][0] + pos[1][0] * 1j
    dir = -1

    if level:
        tasks = [(data, pos, dir, i, j) for i in range(len(data)) for j in range(len(data[0]))]
        with Pool() as pool:
            results = pool.map(process_position, tasks)
        return sum(1 for result in results if result == -1)
    else:
        return follow_path(data, pos, dir)