from collections import Counter

from typing import List
import pytest


def replace_ints(data: Counter) -> Counter:
    result = Counter()
    for stone, count in data.items():
        if stone == 0:
            result[1] += count
        elif len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            first_half = int(str(stone)[:half])
            second_half = int(str(stone)[half:])
            result[first_half] += count
            result[second_half] += count
        else:
            result[stone * 2024] += count
    return result



@pytest.mark.data("125 17", 55312, 65601038650482)
def test_11(data: List[int], level):
    data = Counter(data)  # Convert the list to a Counter
    for i in range(75 if level else 25):
        data = replace_ints(data)
    return sum(data.values())