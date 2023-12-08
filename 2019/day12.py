import re
from typing import List

import numpy as np
import pytest

def simulate(pos, vel, t):
    uni_states = [set(), set(), set()]
    divisors = [0, 0, 0]
    for t in range(t):
        for dim in range(3):  # check for repetitions in x,y,z-dimm, return lcm(x,y,z)
            dhash = 0  # avoid "local variable referenced before assignment"
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

@pytest.mark.notest
def test_12(data: List[str], level):
    data = [re.split("[=>,]", line)[1::2] for line in data]
    data = np.array([[int(a) for a in line] for line in data])
    sim_num = 1000000 if level else 1000
    vel = np.zeros_like(data)
    return simulate(data, vel, sim_num) if level else sum(np.sum(np.abs(data[i])) * np.sum(np.abs(vel[i])) for i in range(len(data)))
