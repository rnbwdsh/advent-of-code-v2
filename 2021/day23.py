from dataclasses import dataclass, field
from functools import cache, cached_property
from typing import List, Generator, Optional, ClassVar, Tuple

@dataclass(frozen=True, repr=True, eq=True, order=True)
class Position:
    row_max: ClassVar[int] = 2
    col_max: ClassVar[int] = 4
    row_max_top: ClassVar[int] = 11
    top_forbidden_pos: ClassVar = [2, 4, 6, 8]  # positions next to columns

    row: int
    col: int
    val: int = field(default=None, hash=False)

    @property
    def is_top(self) -> bool:
        return self.row == -1

    @property
    def col_top(self) -> int:
        return self.col if self.is_top else self.col * 2 + 2

    @cache
    def distance(self, other: "Position") -> int:
        if self > other:
            return other.distance(self)
        if not self.is_top and not other.is_top:
            if self.col == other.col:
                raise RuntimeError(f"Invalid positions: {self}, {other}")
            return (self.row + other.row + 2) + abs(self.col_top - other.col_top)
        elif self.is_top and other.is_top:
            return abs(self.col_top - other.col_top)
        else:
            return abs(self.col_top - other.col_top) + abs(self.row) + abs(other.row)


@dataclass(repr=True, frozen=True, eq=True)
class State:
    col_cost: ClassVar = (None, 1, 10, 100, 1000)

    cols: Tuple[Tuple[int]]
    top: Tuple[int] = field(default=tuple([0] * Position.row_max_top))
    cost: int = 0

    @staticmethod
    @cache
    def check_taking(c, col):
        for i in range(Position.row_max):
            if col == tuple([0] * (Position.row_max - i) + [c + 1] * i):
                return Position.row_max - i - 1

    @cached_property
    def cols_done(self) -> List[bool]:
        return [all(rv == c + 1 for rv in col) for c, col in enumerate(self.cols)]

    @cached_property
    def cols_taking(self) -> List[Optional[int]]:
        return [State.check_taking(c, col) for c, (col, done) in enumerate(zip(self.cols, self.cols_done))]

    def next_states(self):
        starts = list(Position(-1, c, cv) for c, cv in enumerate(self.top) if cv)
        for c, col in enumerate(self.cols):
            if self.cols_done[c] or self.cols_taking[c] is not None:
                continue
            for r, rv in enumerate(col):
                if rv:
                    starts.append(Position(r, c, rv))
                    break
        return ([self.move_copy(s, t) for s in starts for t in self.targets_bot(s)] or
                [self.move_copy(s, t) for s in starts if not s.is_top for t in self.targets_top(s)])

    def targets_top(self, start: Position) -> Generator[Position, None, None]:
        for ran in [range(start.col_top - 1, -1, -1), range(start.col_top + 1, Position.row_max_top)]:
            for c in ran:
                if self.top[c] != 0:
                    break
                if c not in Position.top_forbidden_pos:
                    yield Position(-1, c)

    def targets_bot(self, start: Position):
        for ran in [range(start.col_top - 1, -1, -1), range(start.col_top + 1, Position.row_max_top)]:
            for c in ran:
                if self.top[c] != 0:
                    break
                if c in Position.top_forbidden_pos:
                    col_id = (c - 1) // 2
                    if self.cols_taking[col_id] is not None and start.val == col_id + 1:
                        yield Position(self.cols_taking[col_id], col_id)

    def move_copy(self, start, target) -> "State":
        cp_top = list(self.top)
        cp_cols = [list(c) for c in self.cols]
        if start.is_top:
            cp_top[start.col] = 0
        else:
            cp_cols[start.col][start.row] = 0
        if target.is_top:
            cp_top[target.col] = start.val
        else:
            cp_cols[target.col][target.row] = start.val
        return State(tuple(tuple(c) for c in cp_cols), tuple(cp_top), # noqa
                     self.cost + start.distance(target) * State.col_cost[start.val])

def test_23(data, level):
    # data parsing + per level setup
    start_top = data[2][3:11:2]
    start_bot = data[3][3:11:2]
    data = zip(start_top, "DCBA", "DBAC", start_bot) if level else zip(start_top, start_bot)
    Position.row_max = 4 if level else 2

    start = State(tuple([tuple([ord(i) - ord('A') + 1 for i in items]) for items in data]))
    todo = [start]
    seen = {hash(start)}
    best = 100_000

    while todo:
        state = todo.pop()
        if state.cost > best:
            continue
        for ns in state.next_states():
            hns = hash(ns)
            if hns not in seen:
                if ns.cost < best:
                    todo.append(ns)
                seen.add(hns)
                if all(ns.cols_done) and ns.cost < best:
                    best = ns.cost
    return best

def test_distance():
    top0 = Position(-1, 0)
    top1 = Position(-1, 10)
    col0 = Position(0, 0)
    col1 = Position(0, 1)
    col2 = Position(1, 0)
    assert top0.distance(top1) == 10
    assert top0.distance(col0) == 3
    assert col0.distance(col1) == 4
    assert col2.distance(col1) == 5
