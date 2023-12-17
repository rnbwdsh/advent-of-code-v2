from typing import List

import numpy as np
import pytest

@pytest.mark.data("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""", 114, 2)
def test_09(data: List[str], level):
    data = [[int(i) for i in line.split(" ")][::(-1 if level else 1)] for line in data]
    return sum(map(expand, data))

def expand(line: List[int]):
    child = list(np.diff(line))
    if not all(np.equal(line, 0)):
        child.append(expand(child))
    return line[-1] + child[-1]
