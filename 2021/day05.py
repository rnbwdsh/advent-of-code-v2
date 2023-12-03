from collections import defaultdict
from typing import List

from level_annotations import level_ab

def test_05(lines: List[str], level):
    field = defaultdict(int)
    for line in lines:
        start, end = [complex(*[int(i) for i in part.split(",")]) for part in line.split(" -> ")]
        dist = end - start
        dlen = int(max(abs(dist.real), abs(dist.imag)))
        if not dist.real or not dist.imag or (level and dist.real / dist.imag % 1 == 0):
            for d in range(dlen + 1):
                field[start + (dist / dlen) * d] += 1
    return sum([v > 1 for v in field.values()])
