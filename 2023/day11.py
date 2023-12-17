import itertools

import numpy as np
import pytest

@pytest.mark.data("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 374, 8410)
def test_11(data: np.ndarray, level):
    empty_rows = np.all(data == ".", axis=1)
    empty_cols = np.all(data == ".", axis=0)
    expand_b = 1_000_000 if (len(data) > 20) else 100
    expand = expand_b - 1 if level else 1
    list_xy = list(zip(*np.nonzero(np.equal(data, "#"))))
    return sum(distance(start, end, expand, empty_cols, empty_rows)
               for start, end in itertools.combinations(list_xy, 2))

def distance(start, end, expand_size, empty_cols, empty_rows):
    return (abs(start[0] - end[0]) +
            abs(start[1] - end[1]) +
            sum(expand_size for i in range(min(start[0], end[0]), max(start[0], end[0])) if empty_rows[i]) +
            sum(expand_size for i in range(min(start[1], end[1]), max(start[1], end[1])) if empty_cols[i]))
