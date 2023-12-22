from functools import cache
from itertools import product
from typing import List, Set, Optional

import pytest
from tqdm import tqdm

from point import Point

@pytest.mark.data("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""", 5, 7)
def test_22(data: List[str], level):
    total = 0
    bricks = [Brick.create(line) for line in data]
    bricks = sorted(bricks, key=lambda b: -list(b)[0][2])
    simulate_falling(bricks)
    points = set().union(*bricks)
    for curr in tqdm(bricks):
        disintegrate = curr.can_disintegrate(bricks, points - curr)
        if disintegrate and not level:
            total += 1
        elif level and not disintegrate:
            total += simulate_falling([b for b in bricks if b != curr])
    return total

class Brick(frozenset[Point]):
    @staticmethod
    def create(line: str):
        start, end = line.split('~')
        start, end = start.split(','), end.split(',')
        coordinates = product(*[range(int(start[i]), int(end[i])+1) for i in range(3)])
        return Brick(Point(*c) for c in coordinates)

    @cache
    def fallen(self):
        b = Brick({p + Point(0, 0, -1) for p in self})
        return b if all(p[2] >= 0 for p in b) else None

    def fall(self, collision: Set[Point]) -> Optional['Brick']:
        fallen = self.fallen()
        if not fallen or bool(fallen & collision):
            return None
        return fallen

    def can_disintegrate(self, other: List["Brick"], collision: Set[Point]):
        return all(not to_test.fall(collision - to_test)
                   for to_test in other if self != to_test)

def simulate_falling(bricks: List[Brick]):
    fallen_ids = set()
    points = set().union(*bricks)
    repeat = True
    while repeat:
        repeat = False
        for curr_id, curr in enumerate(bricks):
            if fallen := curr.fall(points - curr):
                bricks[curr_id] = fallen
                fallen_ids.add(curr_id)  # the actual fallen-object is exchanged, so we have to keep track of ids
                points.difference_update(curr)  # remove curr
                points.update(fallen)  # add fallen
                repeat = True
    return len(fallen_ids)
