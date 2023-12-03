import re

import aocd
import numpy as np

def parse(d):
    out = []
    for line in d.split("\n"):
        a = re.split("=|>|,", line)
        out.append([int(a[1]), int(a[3]), int(a[5])])
    return np.array(out)

data = aocd.get_data(day=12)

def simulate(pos, vel, t):
    uni_states = [set(), set(), set()]
    divisors = [0, 0, 0]
    for t in range(t):
        for dim in range(3):  # check for repetitions in x,y,z-dimm, return lcm(x,y,z)
            if not divisors[dim]:  # only do divisor-seach for not-yet-found
                dhash = hash(str(pos[:, dim]) + str(vel[:, dim]))
                if dhash in uni_states[dim]:
                    uni_states[dim] = set()
                    divisors[dim] = t
                    if all(divisors):
                        return np.lcm.reduce(divisors)
            uni_states[dim].add(dhash)

        for i in range(1 + len(pos)):  # actual calculation
            shifted = np.concatenate((pos[i:], pos[:i]))  # add last i columns to top, then substract
            vel += np.clip(shifted - pos, -1, 1)  # sub(a-b) + clip => -1 if a<b, +1 if a>b
        pos += vel

def calculate(pos, vel):  # sum of abs of vel and pos
    return sum(np.sum(np.abs(pos[i])) * np.sum(np.abs(vel[i]))
               for i in range(len(pos)))

def run(data, sim_num, calc=True):
    tpos = parse(data)
    vel = np.zeros_like(tpos)
    sim = simulate(tpos, vel, sim_num)
    if not calc:
        return sim
    else:
        return calculate(tpos, vel)

assert run("""<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>""", 10) == 179
assert run("""<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>""", 100) == 1940
assert run("""<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>""", 10000000, calc=False) == 2772

aocd.submit(day=12, answer=run(data, 1000))

aocd.submit(day=12, answer=run(data, 10000000, calc=False))
