import itertools
from typing import List

def test_09(data: List[int], level):
    preamble_len = 5 if len(data) == 20 else 25  # if test-set, we have shorter preamble
    for i in range(preamble_len, len(data)):
        if data[i] not in {sum(tup) for tup in itertools.permutations(data[i - preamble_len:i], 2)}:  # noqa typing
            if level:
                number_to_find = data[i]
                break
            return data[i]  # method 0 returns here
    for i in range(len(data)):
        for lookback in range(i + 1):
            sub_array = data[i - lookback:i]
            if sum(sub_array) == number_to_find:  # noqa typing
                return min(sub_array) + max(sub_array)
