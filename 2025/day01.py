from typing import List

import pytest


@pytest.mark.data('L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82', 3, 6)
def test_01(data: List[str], level):
    curr = 50
    zeros = 0
    for line in data:
        sign = (-1 if "R" in line else 1)
        if level:
            for _ in range(abs(int(line[1:]))):
                curr += sign
                curr %= 100
                zeros += curr == 0
        else:
            curr += sign * int(line[1:])
            curr %= 100
            zeros += curr == 0
    return zeros