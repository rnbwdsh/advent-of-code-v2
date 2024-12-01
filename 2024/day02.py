from typing import List

import pytest
from collections import Counter

@pytest.mark.data(("""3   4
4   3
2   5
1   3
3   9
3   3"""), 11, 31)
def test_01(data: List[str], level):
    l = [int(d.split(" ")[0]) for d in data]
    r = [int(d.split(" ")[-1]) for d in data]
    if level:
        rc = Counter(r)
        return sum(k * rc[k] for k in l)
    else:
        return sum(abs(ll-rr) for ll, rr in zip(sorted(l), sorted(r)))
