from typing import List

def calc_0(mass):
    return mass // 3 - 2

def calc_1(mass: int):
    fl = [calc_0(mass)]
    while calc_0(fl[-1]) > 0:
        fl.append(calc_0(fl[-1]))
    return sum(fl)

def test_01(data: List[int], level):
    return sum(map(calc_1, data)) if level else sum(map(calc_0, data))
