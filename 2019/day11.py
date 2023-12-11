from collections import defaultdict
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from computer import Computer

BLACK, WHITE = 0, 1

def paint_ship(data, start_col=BLACK):
    ship = defaultdict(int)
    pos = 0
    direction = 1j
    lr = {0: 1j, 1: -1j}
    ship[pos] = start_col

    p = Computer(data, ext_mem=1000)
    while not p.done:
        curr_col = ship[pos]
        next_col, next_dir = p.compute([curr_col])
        ship[pos] = next_col
        direction *= lr[next_dir]
        pos += direction
    return ship

def show(ship):
    real = [int(i.real) for i in ship.keys()]  # get real compontents
    imag = [int(i.imag) for i in ship.keys()]  # get imag components
    min_r, max_r, mini, maxi = min(real), max(real), min(imag), max(imag)  # get ranges
    arr = np.zeros((max_r - min_r + 1, maxi - mini + 1))  # create canvas with enough size
    for pos, col in ship.items():
        x, y = pos.real - min_r, pos.imag - mini
        arr[int(x), int(y)] = col
    plt.imshow(np.rot90(arr), cmap="Greys")

def test_11(data: List[int], level_a):
    painted = paint_ship(data, level_a)
    if not level_a:
        return len(painted)
    else:
        show(painted)
