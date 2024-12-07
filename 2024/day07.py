from typing import List

import pytest


def consume(total: int, rest: List[int], expected: int, level: int) -> bool:
    if len(rest) == 0:
        return total == expected
    else:
        next = (total + rest[0], total * rest[0])
        if level:
            next += (int(str(total) + str(rest[0])),)
        return any(consume(n, rest[1:], expected, level) for n in next)


@pytest.mark.data(("""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""), 3749, 11387)
def test_07(data: List[str], level):
    total = 0
    for line in data:
        expected = int(line.split(":")[0])
        first, *rest = map(int, line.split(":")[1].split())
        if consume(first, rest, expected, level):
            total += expected
    return total