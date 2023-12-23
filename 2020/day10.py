from collections import Counter
from functools import lru_cache
from typing import List, Dict, Tuple

import numpy as np

@lru_cache
def dfs(g: Tuple[int], u: int, t: int):
    return u == t or sum(dfs(g, c, t) for c in range(u + 1, u + 4) if c in g)

def test_10(data: List[int], level):
    data = [0] + sorted(data)
    data += [max(data) + 3]
    if level:
        return dfs(tuple(data), 0, max(data))
    else:
        cd: Dict[int, int] = Counter(np.diff(data))
        return cd[1] * cd[3]
