from collections import Counter
from functools import lru_cache

import numpy as np

@lru_cache
def dfs(g, u, t):
    return u == t or sum(dfs(g, c, t) for c in range(u + 1, u + 4) if c in g)

def test_10(data, level):
    data = [0] + sorted(map(int, data))
    data += [max(data) + 3]
    if level:
        return dfs(tuple(data), 0, max(data))
    else:
        cd = Counter(np.diff(data))
        return cd[1] * cd[3]
