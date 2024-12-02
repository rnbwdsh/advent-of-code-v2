from typing import List

import numpy as np
import pytest


def check(line) -> bool:
    line_inc = np.array(line)
    line_inc = line_inc[:-1] - line_inc[1:]
    return (all(line_inc > 0) and all(line_inc <= 3)) or (all(line_inc < 0) and all(line_inc >= -3))

@pytest.mark.data(("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""), 2, None)
def test_02(data: List[str], level):
    ret = 0
    for d in data:
        line = [int(i) for i in d.split(" ")]
        if check(line):
            ret += 1
            continue
        if level:
            for i in range(len(line)):
                cpy = np.delete(line, i)
                if check(cpy):
                    ret += 1
                    break
    return ret
