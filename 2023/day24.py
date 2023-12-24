from itertools import combinations
from typing import List

import z3
import numpy as np
import pytest

from point import Point


@pytest.mark.data("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""", 2, 47)
def test_24(data: List[str], level):
    point_vel_list = [[Point([int(n) for n in part.split(", ")])
                       for part in line.split(" @ ")]
                      for line in data]
    if level:
        return sum(find_intersecting_p(point_vel_list))
    else:  # test data is only length 5, this is how we distinguish between the cases
        return collide_2d_future(pvl=point_vel_list,
                                 test_min=200000000000000 if len(data) > 5 else 7,
                                 test_max=400000000000000 if len(data) > 5 else 27)


def find_intersecting_p(pvl):
    sol = z3.Solver()
    ps = z3.IntVector("p", 3)
    vs = z3.IntVector("v", 3)
    ts = z3.IntVector("t", len(pvl))
    sol.add(z3.And([t >= 0 for t in ts]))
    for t, (p, v) in zip(ts, pvl):  # for each point
        for j in range(3):  # for x, y, z
            sol.add(ps[j] + vs[j] * t == p[j] + v[j] * t)
    sol.check()  # total of 3+3+pd variables and 3*pd constraints -> over-constrained
    model = sol.model()
    return [model[ps[i]].as_long() for i in range(3)]


def collide_2d_future(pvl, test_min, test_max):
    total = 0
    for p1, p2 in combinations(pvl, 2):
        ip = line_intersection(*p1, *p2)
        total += int(ip is not None and np.all(test_min <= ip) and np.all(ip <= test_max))
    return total


def line_intersection(p1, v1, p2, v2):
    p1, v1, p2, v2 = [np.array(p)[:2] for p in [p1, v1, p2, v2]]  # throw away z dimension
    a = np.array([v1, -v2]).T
    if np.linalg.det(a) == 0:  # check linear independence
        return None
    b = p2 - p1
    t = np.linalg.solve(a, b)
    if np.any(t < 0):
        return None
    return p1 + t[0] * v1
