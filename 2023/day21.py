from typing import List

import numpy as np
import pytest
from scipy.signal import convolve2d
from tqdm import tqdm
from sympy import interpolate
from point import Point

@pytest.mark.data("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 16, None)
def test_21(data: np.ndarray, level):
    start = Point([(x, y) for x, row in enumerate(data) for y, cell in enumerate(row) if cell == 'S'][0])
    steps = 6 if len(data) < 15 else 64  # example input only runs for 6 steps, real input for 64
    rep = len(data)

    if level:  # to run the simulation with convolution, we need to expand the field 10x10
        data = np.tile(data, (10, 10))
        start += Point(data.shape) // 2  # shift start to be in the middle of the new field
        steps = int(rep*4.5)  # the highest history value we need is at rep*4.5

    assert data[start] == 'S'  # validate that shifted center is still on the start
    rock_mask = ~np.equal(data, '#')  # required for
    data = np.zeros_like(data, dtype=bool)
    neigh = np.array([[0, 1, 0],[1, 0, 1],[0, 1, 0]]).astype(np.int8)
    hist = [1]  # history starts with 1 place
    data[start] = 1
    for _ in tqdm(range(steps)):  # convolving with the neighborhood matrix
        data = convolve2d(data, neigh, mode='same')  # convolve with neighborhood matrix
        data = np.logical_and(data, rock_mask)
        hist.append(np.sum(data))
    # for debugging, use `plt.imshow(data); plt.show()` to see that you didn't go out of bounds
    return solve_analytical(hist, rep, target=26501365) if level else np.sum(data)

def solve_analytical(hist: List[int], rep, target=26501365):
    """ every 131*2 steps, history repeats itself (*2 because even/odd) and values grow the same as day09 with 2 layers
    3885			96215			311345			649275			1110005
            92330           215130          337930         460730
                  12800             12800            12800

    wolfram is even able to continue my series from 4 values at
    offset 0: https://www.wolframalpha.com/input?i=1%2C61847%2C246493%2C553939
    offset 65: https://www.wolframalpha.com/input?i=3885%2C96215%2C311345%2C649275
    and fill in values https://www.wolframalpha.com/input?i=5+%286871+-+18374+n+%2B+12280+n%5E2%29%2C+n%3D%28floor%2826501365+%2F+262%29+%2B+1%29
    to come to the correct result. the 0-indexed formula would be 5 (777 + 6186 n + 12280 n^2), n=101150 => 628206330073385
    """
    pos_relevant = range(target % rep, len(hist), rep*2)  # 65, 327, 589 for field size of 131
    points = [(i, hist[i]) for i in pos_relevant]
    return int(interpolate(points, target))
