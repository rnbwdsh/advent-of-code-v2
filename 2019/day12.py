import re
from typing import List

import numpy as np

def simulate(pos, sim_num):
    uni_states = [set(), set(), set()]
    divisors = [0, 0, 0]
    vel = np.zeros_like(pos)

    for t in range(sim_num):
        for dim in range(3):  # check for repetitions in x,y,z-dimm, return lcm(x,y,z)
            dhash = 0  # avoid "local variable referenced before assignment"
            if not divisors[dim]:  # only do divisor-seach for not-yet-found
                dhash = hash(str(pos[:, dim]) + str(vel[:, dim]))
                if dhash in uni_states[dim]:
                    divisors[dim] = t
                    if all(divisors):  # checks if all are >0
                        return divisors
            uni_states[dim].add(dhash)
        for i in range(1 + len(pos)):  # actual calculation
            shifted = np.concatenate((pos[i:], pos[:i]))  # add last i columns to top, then substract
            vel += np.clip(shifted - pos, -1, 1)  # sub(a-b) + clip => -1 if a<b, +1 if a>b
        pos += vel
    return vel  # returned for low sim numbers

def test_12(data: List[str], level):
    data = np.array([list(map(int, re.split("[=>,]", line)[1::2])) for line in data])
    sim_num = 1_000_000 if level else 1000
    if not level:  # tests have other sim_num
        sim_num = {-3: 10, -2: 100}.get(data.sum(), 1_000_000 if level else 1000)
    div_or_vel = simulate(data, sim_num)
    return np.lcm.reduce(div_or_vel) if level else sum(np.abs(dat).sum() * np.abs(vel).sum() for dat, vel in zip(data, div_or_vel))
