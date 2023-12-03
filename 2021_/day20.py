import numpy as np
from scipy.signal import convolve2d

from level_annotations import level_ab

@level_ab(20, sep="\n\n")
def test(lines, level):
    mapping, field = lines
    mapping = (np.array(list(mapping)) == "#").astype(int)
    field = np.pad((np.array([list(line) for line in field.split("\n")]) == "#").astype(int), 100 if level else 4)
    for _ in range(50 if level else 2):
        field = convolve2d(field, [[1, 2, 4], [8, 16, 32], [64, 128, 256]], mode="valid")
        for pos, val in np.ndenumerate(field): field[pos] = mapping[val]
    return field.sum()
