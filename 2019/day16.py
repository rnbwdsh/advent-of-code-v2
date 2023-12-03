import aocd
import numpy as np
import pandas as pd

parse = lambda data: [int(i) for i in data]
data = parse(aocd.get_data(day=16))
pd.DataFrame(data).T  # debug statement

def prepare_mul(n):
    mul = np.zeros((n, n), dtype=int)
    for i in range(n):
        row = np.repeat([0, 1, 0, -1], i + 1)  # repeat each number i times
        row = np.tile(row, 1 + n // len(row))  # then repeat the row until len(row) >= len(data)
        mul[i] = row[1:n + 1]  # take offset 1, then trim to same length
    return mul

def process(data, phase=100):
    mul = prepare_mul(len(data))  # prepare multiplication matrix
    for _ in range(phase):  # run loop
        data = abs(mul @ data) % 10  # multiply every row of data with every row of mul, then take each sum as a row
    return "".join([str(i) for i in data[:8]])  # take first 8 as str

assert process(parse("12345678"), phase=4) == "01029498"
assert process(parse("80871224585914546619083218645595")) == "24176176"
aocd.submit(day=16, answer=process(parse(data)))

def process(data, phase=100):
    data = np.array(data * 10000, dtype=int)
    offset = int("".join([str(i) for i in data[:7]])) % len(data)
    for i in range(100):
        data = data[::-1].cumsum()[::-1] % 10  # calculate cumsum from back to front
    # this works because newdata[-1] = data[-1]; data[-2] = data[-2]+newdata[-1]
    # because repeat(0,1,0,-1) for high i produces a diagonal matrix
    return "".join(data[offset:offset + 8].astype(str))  # take 8 at offset as str

assert process(parse("03036732577212944063491565474664")) == "84462026"
aocd.submit(day=16, answer=process(parse(data)))
