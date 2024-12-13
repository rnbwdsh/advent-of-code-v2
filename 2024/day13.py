from typing import List

import pytest
import re
import sympy as sp


@pytest.mark.data("""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""", 480, 875318608908)
def test_13(data: List[str], level):
    total = 0
    for segment in data:
        pattern = r"Button A: X\+(\d+), Y\+(\d+)\s*Button B: X\+(\d+), Y\+(\d+)\s*Prize: X=(\d+), Y=(\d+)"
        match = re.search(pattern, segment)
        if not match:
            continue
        x1, y1, x2, y2, x, y = map(int, match.groups())
        if level:
            x += 10000000000000
            y += 10000000000000
        i, j = sp.symbols('i j', integer=True, nonnegative=True)
        eq1 = sp.Eq(x1 * i + x2 * j, x)
        eq2 = sp.Eq(y1 * i + y2 * j, y)
        sol = sp.solve((eq1, eq2), (i, j), dict=True, integer=True)
        a, b = (int(sol[0][i]), int(sol[0][j])) if sol and sol[0] else (None, None)
        if a is None:
            continue
        assert x1 * a + x2 * b == x
        assert y1 * a + y2 * b == y
        total += a * 3 + b
    return total
