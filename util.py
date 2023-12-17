from typing import Tuple

L, R, U, D = (0, -1), (0, 1), (-1, 0), (1, 0)
DIR = [L, R, U, D]
OPPOSITE = {L: R, R: L, U: D, D: U}

def add_pos(pos: Tuple, direction: Tuple):
    return tuple(p + d for p, d in zip(pos, direction))

def in_bounds(index, array):
    return all(0 <= idx < array.shape[dim] for dim, idx in enumerate(index))