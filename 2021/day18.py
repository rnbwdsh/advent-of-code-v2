import itertools
import json
import math
from copy import deepcopy

from more_itertools import windowed

def magnitude(d):
    if isinstance(d, int):
        return d
    return magnitude(d[0]) * 3 + magnitude(d[1]) * 2

def addd(d, side, num, switch_side=True):
    if isinstance(d[side], int):
        d[side] += num
    else:
        addd(d[side], side != switch_side, num, switch_side=False)

def split(parent):
    for kid in parent:
        if isinstance(kid, int) and kid > 9:
            parent[parent.index(kid)] = [math.floor(kid / 2), math.ceil(kid / 2)]
            return True
        elif isinstance(kid, list) and split(kid):
            return True
    return None

def sublists(l):
    return [sub for sub in l if isinstance(sub, list)]

def explode(d0):
    for d1 in sublists(d0):
        for d2 in sublists(d1):
            for d3 in sublists(d2):
                for d4 in sublists(d3):
                    for side in [0, 1]:
                        for parent, kid in windowed((d4, d3, d2, d1, d0), 2):
                            if kid.index(parent) == int(not side):
                                addd(kid, side, d4[side])
                                break
                    d3[d3.index(d4)] = 0
                    return True

def run(lines):
    lines = deepcopy(lines)
    curr = lines[0]
    for line in lines[1:]:
        curr = [curr] + [line]
        while explode(curr) or split(curr):
            continue
    return magnitude(curr)

def test_18(data, level):
    for method, inp, expected in [
        [explode, [[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]],
        [explode, [7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]],
        [explode, [[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]],
        [explode, [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]],
        [split, [11], [[5, 6]]], ]:
        oinp = str(inp)
    method(inp)
    assert inp == expected, f"Failed for {method.__name__}({oinp})\n{inp} !=\n{expected}"

    assert magnitude([9, 1]) == 29
    assert magnitude([[9, 1], [1, 9]]) == 129
    assert magnitude([[1, 2], [[3, 4], 5]]) == 143
    assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
    assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
    assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
    assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
    assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == 3488

    assert run([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == 1384
    assert run([[1, 1], [2, 2], [3, 3], [4, 4]]) == 445
    assert run([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]) == 791
    assert run([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]) == 1137

    data = [json.loads(line) for line in data]
    return max(run([a, b]) for a, b in itertools.permutations(data, 2)) if level else run(data)
