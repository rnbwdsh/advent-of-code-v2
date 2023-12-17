import re
from typing import List

import numpy as np
import pytest

@pytest.mark.data("""Time:      7  15   30
Distance:  9  40  200""", 288, 71503)
def test_06(data: List[str], level):
    time, dist = data
    if level:
        time = time.replace(" ", "")
        dist = dist.replace(" ", "")
    time = [int(i) for i in re.findall("\d+", time)]
    dist = [int(i) for i in re.findall("\d+", dist)]
    return np.prod([sum((t - wt) * wt > d
                        for wt in range(1, t))
                    for t, d in zip(time, dist)])
