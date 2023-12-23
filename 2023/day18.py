from typing import List

import pytest

from point import Point, PointList, L, R, U, D

LOOKUP_CHR = {"U": U, "D": D, "L": L, "R": R}
LOOKUP_INT = {0: R, 1: D, 2: L, 3: U}

@pytest.mark.data("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""", 62, 952408144115)
def test_18(data: List[str], level):
    pos = Point(0, 0)
    corners = [pos]
    for line in data:
        side, dist, col = line.split(" ")
        if level:
            col = col[2:-1]
            dist = int(col[:5], 16)
            side = LOOKUP_INT[int(col[5])]
        else:
            dist = int(dist)
            side = LOOKUP_CHR[side]
        pos = pos + side * dist
        corners.append(pos)
    pl = PointList(corners)
    return pl.area + pl.sum_len
