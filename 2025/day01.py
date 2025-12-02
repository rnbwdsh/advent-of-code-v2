from typing import List

import pytest


@pytest.mark.data('L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82', 11, 31)
def test_01(data: List[str], level):
    curr = 50
    zeros = 0
    for line in data:
        sign = (-1 if "R" in line else 1)
        curr += sign * int(line[1:])
        if level:
            for _ in range(abs(curr)):
                curr += sign
                zeros += curr == 0
        else:
            zeros += sign * curr == 0
    return zeros