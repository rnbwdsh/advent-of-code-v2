# Imports and utility functions
import re
from itertools import product

import numpy as np

def manhattanDist(a, b):  # this can be found in scipy.spatial.distance.cityblock
    return sum(abs(np.array(a) - np.array(b)))

def calc_InRange_DistTo0_metric(pos, nanobots, ranges=None):
    dist = np.array([manhattanDist(pos, n2["pos"]) for n2 in nanobots])
    if not ranges:  # if ranges is not set, calculate bot-to-pos ranges, else calculate pos-with-range-to-bots distance
        ranges = np.array([bot["range"] for bot in nanobots])
    in_range = sum(dist <= ranges)
    dist_to_0 = manhattanDist(pos, (0, 0, 0))
    # as we try to maximize this function, the dist_to_0 (where we want a small one) should be negative
    return in_range, - dist_to_0

# Read and parse data
a = open("day23.txt").read()
b = a.split("\n")
c = [re.findall(r"(-?\d+)", bb) for bb in b]
nanobots = [{"id": id, "pos": (int(a), int(b), int(c)), "range": int(d)} for id, (a, b, c, d) in enumerate(c)]

# Part 1: Find how many drones are in range of master (drone with max range)
master = max(nanobots, key=lambda bot: bot["range"])
master_dist = calc_InRange_DistTo0_metric(master["pos"], nanobots, master["range"])
print(master)
print(master_dist)
print("number of drones in range of master:", master_dist[0], "\n\n")

# In[ ]:


# Part 2: Binary search the best position
best_pos, bs = (0, 0, 0), (0, 0)
for _ in range(5):  # start from new best_pos 5 times
    for bexp in range(30, -1, -1):
        for xyz in product(range(-1, 2), repeat=3):
            expo = 2 ** bexp
            pos = best_pos + np.array(xyz) * expo
            score = calc_InRange_DistTo0_metric(pos, nanobots)
            if score > bs:
                bs, bp = score, pos
                print("new best distance", bs, bp)
        best_pos = bp  # start searching from bp now, and repeat binary search
print("manhattan distance from 0,0,0 to best pos:", -bs[1])
