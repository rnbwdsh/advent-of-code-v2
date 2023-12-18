from typing import List

import numpy as np

class Point(tuple):
    def __new__(cls, *args, **kwargs):
        """ If the given argument is of type tuple or list, create a Point from it. If it's more than one argument, make them a list and call self. """
        if len(args) > 1:
            args = tuple(args)
        elif isinstance(args[0], (tuple, list)):
            args = args[0]
        return super().__new__(cls, args)

    def __add__(self, other) -> "Point":
        assert len(self) == len(other)
        return Point(tuple(p + o for p, o in zip(self, other)))

    def __sub__(self, other) -> "Point":
        assert len(self) == len(other)
        return Point(tuple(p - o for p, o in zip(self, other)))

    def __mul__(self, other) -> "Point":
        assert isinstance(other, int)
        return Point(tuple(p * other for p in self))

    def __repr__(self) -> str:
        return super().__repr__()[1:-1]

    def in_bounds(self, array: np.ndarray) -> bool:
        assert len(array.shape) == len(self)
        return all(0 <= idx < array.shape[dim] for dim, idx in enumerate(self))

    @property
    def neighbors(self) -> List["Point"]:
        return [self + d for d in DIR]

    @property
    def opposite(self):
        if self in OPPOSITE.values():
            return Point(OPPOSITE[self])

L = Point(0, -1)
R = Point(0, 1)
U = Point(-1, 0)
D = Point(1, 0)
DIR = [L, R, U, D]
OPPOSITE = {L: R, R: L, U: D, D: U}
LOOKUP_CHR = {"U": U, "D": D, "L": L, "R": R}
LOOKUP_INT = {0: R, 1: D, 2: L, 3: U}
