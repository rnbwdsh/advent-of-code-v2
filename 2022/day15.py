import re

import pytest
import z3

@pytest.mark.notest
def test_15(data, level):
    sensor = []
    example = len(data) == 14
    for line in data:
        x, y, a, b = map(int, re.findall(r"-?\d+", line))
        dist = abs(x - a) + abs(y - b)
        sensor.append((x, y, dist))
    if level:
        search_space = 20 if example else 4000000
        solver = z3.Solver()
        xt, yt = z3.Ints("x y")
        solver.add(xt >= 0, yt >= 0, xt <= search_space, yt <= search_space)
        solver.add(*[z3.Abs(xt - x) + z3.Abs(yt - y) > dist
                     for x, y, dist in sensor])
        solver.check()
        model = solver.model()
        return model[xt].as_long() * 4000000 + model[yt].as_long()
    else:
        search_space = 10 if example else 2000000
        possible_points = set()
        for x, y, dist in sensor:
            lr_dist = (dist - abs(y - search_space))
            for p in range(x - lr_dist, x + lr_dist):
                possible_points.add(p)
        return len(possible_points)
