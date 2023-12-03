import numpy as np
from scipy.signal import convolve2d


def test_20(data: str, level):
    mapping, field = data.split("\n\n")
    mapping = (np.array(list(mapping.replace("\n", ""))) == "#").astype(int)
    field = (np.array([list(line) for line in field.split("\n")]) == "#").astype(int)
    field = np.pad(field, 100 if level else 4)
    for _ in range(50 if level else 2):
        field = convolve2d(field, [[1, 2, 4], [8, 16, 32], [64, 128, 256]], mode="valid")
        for pos, val in np.ndenumerate(field): field[pos] = mapping[val]
    return field.sum()
