import cmath
from collections import defaultdict
from math import pi

import aocd
import numpy as np

def parse(d):
    return np.array([list(dd) for dd in d.split("\n")]).T

data = parse(aocd.get_data(day=10))

small = """.#..#
.....
#####
....#
...##"""

mid = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

big = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

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

assert (raytrace(parse(small))) == (8, (3, 4))
assert (raytrace(parse(mid))) == (33, (5, 8))
assert (raytrace(parse(big))) == (210, (11, 13))

aocd.submit(day=10, answer=raytrace(data)[0])

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

assert pulverize(parse(big)) == (8, 2)

score = lambda a: a[0] * 100 + a[1]
aocd.submit(day=10, answer=score(pulverize(data)))
