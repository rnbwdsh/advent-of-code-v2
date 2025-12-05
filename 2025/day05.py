from typing import List

import pytest


@pytest.mark.data('3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32', 3, 14)
def test_05(data: List[List[str]], level):
    ranges = [list(map(int, r.split("-"))) for r in data[0]]
    numbers = list(map(int, data[1]))
    if level:
        merged = []
        for start, end in sorted(ranges):
            if merged and merged[-1][1] >= start - 1:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return sum(end - start + 1 for start, end in merged)
    else:
        return sum(1 for n in numbers if any(start <= n <= end for start, end in ranges))