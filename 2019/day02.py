from typing import List

def process(d: List[int]) -> int:
    d = d[:]  # Make a copy of the data to avoid modifying the original list
    for ptr in range(0, len(d), 4):
        if d[ptr] == 1:
            d[d[ptr + 3]] = d[d[ptr + 1]] + d[d[ptr + 2]]
        elif d[ptr] == 2:
            d[d[ptr + 3]] = d[d[ptr + 1]] * d[d[ptr + 2]]
        elif d[ptr] == 99:
            break
    return d[0]

def test_02(data: List[int], level):
    if level:
        for i in range(100):
            for j in range(100):
                data_copy = data[:]
                data_copy[1:3] = i, j
                if process(data_copy) == 19690720:
                    return i * 100 + j

    data_copy = data[:]
    data_copy[1:3] = 12, 2
    return process(data_copy)
