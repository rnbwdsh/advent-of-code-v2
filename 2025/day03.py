from typing import List

import pytest

def largest(number_str, k=12):
    if len(number_str) == k:
        return int(number_str)
    possible_without = [int(number_str[:i] + number_str[i+1:]) for i in range(len(number_str))]
    return largest(str(max(possible_without)), k)

@pytest.mark.data(("""987654321111111
811111111111119
234234234234278
818181911112111"""), 357, 3121910778619)
def test_03(data: List[str], level):
    return sum(largest(line, 12 if level else 2) for line in data)