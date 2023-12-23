from typing import List

MOD = 20201227

def test_25(data: List[int], level_a):
    a, b = data
    x = 1
    for i in range(1, 10000000000):
        x = (x * 7 % MOD)
        if a == x:
            return pow(b, i, MOD)
