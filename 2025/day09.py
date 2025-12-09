from typing import List, Optional

import pytest
from shapely import Polygon, Point, box


@pytest.mark.data('7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3', 50, 24)
def test_09(data: List[str], level):
    points = [Point(tuple(map(int, line.split(",")))) for line in data]
    poly = Polygon(points)
    return int(max(get_area(p1, p2, poly if level else None)
                   for i, p1 in enumerate(points)
                   for j, p2 in enumerate(points)
                   if i > j))

def get_area(p1: Point, p2: Point, poly: Optional[Polygon]) -> int:
    xmin = min(p1.x, p2.x)
    xmax = max(p1.x, p2.x)
    ymin = min(p1.y, p2.y)
    ymax = max(p1.y, p2.y)
    bbox = box(xmin, ymin, xmax, ymax)
    if poly is None or poly.contains(bbox):
        return box(xmin, ymin, xmax + 1, ymax + 1).area
    return 0
