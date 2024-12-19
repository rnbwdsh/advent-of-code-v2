from functools import cache
from typing import List

import pytest


@cache
def can_be_made(line, available_patterns) -> bool:
    return line == "" or any(line.startswith(pattern) and can_be_made(line[len(pattern):], available_patterns) for pattern in available_patterns)


@cache
def ways_to_make(line, available_patterns) -> int:
    return line == "" or sum(ways_to_make(line[len(pattern):], available_patterns) for pattern in available_patterns if line.startswith(pattern))


@pytest.mark.data("""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""", 6, 16)
def test_19(data: List[str], level):
    total = 0
    available_patterns = tuple(data[0].split(", "))
    for line in data[1].split("\n"):
        if level:
            total += ways_to_make(line, available_patterns)
        if can_be_made(line, available_patterns) and not level:
            total += 1
    return total
