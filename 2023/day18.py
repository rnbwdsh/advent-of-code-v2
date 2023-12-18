from typing import List

import pytest

from point import Point, LOOKUP_CHR, LOOKUP_INT

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
    area = 2  # +2 for visiting 0/0 twice, *2 because we do //2
    for line in data:
        side, dist, col = line.split(" ")
        if level:
            col = col[2:-1]
            dist = int(col[:5], 16)
            side = LOOKUP_INT[int(col[5])]
        else:
            dist = int(dist)
            side = LOOKUP_CHR[side]
        area += dist
        pos = pos + side * dist
        corners.append(pos)
    return (area // 2) + shoelace_area(corners)


def shoelace_area(corners: List[Point]):
    return abs(sum(x1*y2 - x2*y1 for ((x1, y1), (x2, y2)) in zip(corners, corners[1:] + corners[:1]))) // 2
