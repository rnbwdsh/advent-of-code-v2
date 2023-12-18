from typing import Tuple

import numpy as np
import pytest

from point import Point, U, R, L, D

LOOKUP = {"/": {U: R, R: U, D: L, L: D},
          "\\": {U: L, L: U, D: R, R: D}}

@pytest.mark.data(r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""", 46, 51)
def test_16(data: np.ndarray, level):
    if level:
        h, w = data.shape
        return max([track_beam(data, (-1, x), D) for x in range(w)] +
                   [track_beam(data, (h, x), U) for x in range(w)] +
                   [track_beam(data, (y, -1), R) for y in range(h)] +
                   [track_beam(data, (y, w), L) for y in range(h)])
    return track_beam(data, (0, -1), R)

def track_beam(data: np.ndarray, p: Tuple, d: Tuple) -> int:
    todo = [(Point(p), d)]
    seen = set()
    while todo:
        p, d = todo.pop()
        p += d
        if not p.in_bounds(data) or (p, d) in seen:
            continue
        seen.add((p, d))
        val = data[p]
        if (val == "." or
                val == "|" and d in (U, D) or
                val == "-" and d in (L, R)):
            todo.append((p, d))
        elif val == "|":
            todo.append((p, U))
            todo.append((p, D))
        elif val == "-":
            todo.append((p, R))
            todo.append((p, L))
        else:
            todo.append((p, LOOKUP[val][d]))
    return len(set(map(lambda x: x[0], seen)))
