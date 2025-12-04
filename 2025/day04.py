import pytest
import numpy as np
from scipy.signal import convolve2d


@pytest.mark.data("""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""", 13, 43)
def test_04(data: np.ndarray, level):
    a = (data == "@").astype(int)
    k = np.ones((3,3), dtype=int)
    k[1,1] = 0
    total = 0
    for _ in range(len(a) if level else 1):
        n = convolve2d(a, k, mode='same', boundary="fill", fillvalue=0)
        to_remove = a & (n <= 3)
        total += to_remove.sum()
        a -= to_remove
    return total
