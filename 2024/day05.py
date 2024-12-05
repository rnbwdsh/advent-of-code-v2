from collections import defaultdict
from typing import List

import numpy as np
import pytest
import re

def sortv(v: List[int], dependencies: dict):
    """ check if the modified sorted list is better """
    for idx, val in enumerate(v):
        if set(v[:idx]) & dependencies[val]:
            v2 = v[:idx-1] + [val, v[idx-1]] + v[idx+1:]
            return sortv(v2, dependencies)
    return v

@pytest.mark.data(("""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""), 143, 123)
def test_05(data: List[List[str]], level):
    total = 0
    dependencies = defaultdict(set)
    for line in data[0]:
        if line == "":
            break
        a, b = map(int, line.split("|"))
        dependencies[a].add(b)
    for line in data[1]:
        v = [int(x) for x in line.split(",")]
        for idx, val in enumerate(v):
            if set(v[:idx]) & dependencies[val]:
                break
        else:
            if not level:
                total += v[len(v) // 2]
        if level:
            v2 = sortv(v, dependencies)
            if v != v2:
                total += v2[len(v2) // 2]

    return total