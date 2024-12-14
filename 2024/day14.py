import re
from typing import List, Tuple

import numpy as np
import pytest


def simulate(robots: List[Tuple[complex, complex]], wrap: complex, time: int):
    area = np.zeros((int(wrap.imag), int(wrap.real)), dtype=int)
    for p, v in robots:
        z = p + v * time
        area[int(z.imag % wrap.imag), int(z.real % wrap.real)] += 1
    return area

@pytest.mark.data("""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""", 12, None)
def test_14(data: List[str], level):
    wrap_around = complex(11 if len(data) <= 30 else 101, 7 if len(data) <= 30 else 103)
    robots = []
    for segment in data:
        match = re.search(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", segment)
        px, py, vx, vy = map(int, match.groups())
        robots.append((complex(px, py), complex(vx, vy)))
    if level:
        return np.argmax([np.max(np.sum(simulate(robots, wrap_around, i) > 0, axis=1)) for i in range(10_000)])
    else:
        grid = simulate(robots, wrap_around, 100)
        xm, ym = int(wrap_around.real // 2), int(wrap_around.imag // 2)
        quadrants = [grid[:ym, :xm], grid[:ym, xm+1:], grid[ym+1:, :xm], grid[ym+1:, xm+1:]]
        return np.prod([np.sum(quad) for quad in quadrants])
