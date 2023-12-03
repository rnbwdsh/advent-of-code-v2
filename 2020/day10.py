from collections import Counter
from functools import lru_cache

import numpy as np

from level_annotations import level_ab

@lru_cache
def dfs(g, u, t):
    return u == t or sum(dfs(g, c, t) for c in range(u + 1, u + 4) if c in g)

@level_ab(10, apply=int, sep="\n")
def solve(data, method=0):
    data = [0] + sorted(data)
    data += [max(data) + 3]
    if method:
        return dfs(tuple(data), 0, max(data))
    else:
        cd = Counter(np.diff(data))
        return cd[1] * cd[3]
