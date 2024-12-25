import itertools
from typing import List

import numpy as np
import pytest


@pytest.mark.data("""#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""", 3, None)
def test_24(data: List[str], level):
    keys, locks = [], []
    for line in data:
        grid = np.array([[c == "#" for c in row] for row in line.split("\n")])
        (keys if grid[0].all() else locks).append(grid)
    return sum(not np.any(key & lock) for key, lock in itertools.product(keys, locks))
