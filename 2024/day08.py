import itertools
from collections import defaultdict

import numpy as np
import pytest


@pytest.mark.data(("""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""), 14, 34)
def test_08(data: np.array, level):
    x, y = data.shape
    lookup = defaultdict(list)
    mask = np.logical_or(np.char.isalpha(data), np.char.isdigit(data))
    for (j, i), val in zip(np.argwhere(mask), data[mask]):
        lookup[val].append(i + j * 1j)

    antinodes = set()
    for k, v in lookup.items():
        for a, b in itertools.permutations(v, 2):
            for i in range(-x, x) if level else [2]:
                pb = a + (b - a) * i
                if 0 <= pb.real < x and 0 <= pb.imag < y:
                    antinodes.add(pb)
    return len(antinodes)