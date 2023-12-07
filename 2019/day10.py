import cmath
from collections import defaultdict
from math import pi

import aocd
import numpy as np
import pytest

def raytrace(d):
    pos_count = {}  # dict of 
    for spos, sval in np.ndenumerate(d):
        if sval == "#":
            found = set()
            for tpos, tval in np.ndenumerate(d):
                if tval == "#" and spos != tpos:
                    diff = complex(*spos) - complex(*tpos)
                    found.add(cmath.phase(diff))
            pos_count[len(found)] = spos
    return max(pos_count.items())


def pulverize(d):
    spos = raytrace(d)[1]
    targets = defaultdict(dict)  # dict of dicts
    for tpos, tval in np.ndenumerate(d):  # collect all targets
        if tval == "#" and spos != tpos:
            diff = complex(*spos) - complex(*tpos)
            angle = (cmath.phase(diff) - pi / 2) % (2 * pi)  # rotate by -90
            targets[angle][abs(diff)] = tpos

    cnt = 0
    while targets:
        for angle in sorted(targets):  # rotate
            ta = targets[angle]
            if ta:
                cnt += 1  # targets count from 1, not from 0, for some drunk reason
                cta = ta.pop(min(ta))
                if cnt == 200:
                    return cta

@pytest.mark.notest
def test_10(data: np.ndarray, level):
    if level:
        a, b = pulverize(data)
        return a + b * 100
    return raytrace(data.T)[0]
