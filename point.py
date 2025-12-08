from typing import List, Tuple

import numpy as np

class Point(tuple):
    def __new__(cls, *args, **kwargs):
        """ If the given argument is of type tuple or list, create a Point from it. If it's more than one argument, make them a list and call self. """
        if len(args) > 1:
            args = tuple(args)
        elif isinstance(args[0], (tuple, list, Point)):
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
        return super().__repr__()[1:-1].replace(" ", "")

    def __abs__(self) -> int:
        return sum(abs(i) for i in self)

    def __floordiv__(self, other):
        assert isinstance(other, int)
        return Point(tuple(p // other for p in self))

    def dist(self, other: "Point") -> int:
        return sum((p - o)**2 for p, o in zip(self, other))

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

class PointList(List[Point]):  # @see: https://github.com/blu3r4y/AdventOfCode2023/blob/main/src/day10.py
    @property
    def adjacent_pairs(self) -> List[Tuple[Point, Point]]:
        return list(zip(self, self[1:] + self[:1]))

    @property
    def shoelace_area(self) -> int:  # https://en.m.wikipedia.org/wiki/Shoelace_formula#Triangle_formula
        return abs(sum(x1*y2 - x2*y1 for ((x1, y1), (x2, y2)) in self.adjacent_pairs)) // 2

    @property
    def sum_len(self) -> int:
        return sum(abs(pa-pb) for pa, pb in self.adjacent_pairs)

    @property
    def area(self):  # https://en.wikipedia.org/wiki/Pick%27s_theorem
        return self.shoelace_area - self.sum_len // 2 + 1


L = Point(0, -1)
R = Point(0, 1)
U = Point(-1, 0)
D = Point(1, 0)
DIR = [L, R, U, D]
OPPOSITE = {L: R, R: L, U: D, D: U}
