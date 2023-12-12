import cmath
from collections import defaultdict
from math import pi

import numpy as np

def raytrace(data):
    pos_count = {}
    for spos, sval in np.ndenumerate(data):
        if sval == "#":
            found = set()
            for pos, val in np.ndenumerate(data):
                if val == "#" and spos != pos:
                    diff = complex(*spos) - complex(*pos)
                    found.add(cmath.phase(diff))
            pos_count[len(found)] = spos
    return max(pos_count.items())

def test_10(data: np.ndarray, level):
    data = data.T  # make data x/y instead of y/x
    if level:
        spos = raytrace(data)[1]
        targets = defaultdict(dict)  # dict of dicts
        for pos, val in np.ndenumerate(data):  # collect all targets
            if val == "#" and spos != pos:
                diff = complex(*spos) - complex(*pos)
                angle = (cmath.phase(diff) - pi / 2) % (2 * pi)  # rotate by -90
                targets[angle][abs(diff)] = pos
        cnt = 0
        for angle in sorted(targets):  # rotate
            ta = targets[angle]
            if ta:
                cnt += 1  # targets count from 1, not from 0, for some drunk reason
                cta = ta.pop(min(ta))
                if cnt == 200:
                    return cta[0] * 100 + cta[1]
    return raytrace(data)[0]
