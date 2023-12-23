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
    bricks = [Brick.create(line) for line in data]
    bricks.sort(key=lambda brick: list(brick)[0][2])  # sort by mean z
    simulate_falling(bricks, False)  # make all fall to bottom
    return sum(simulate_falling([b for b in bricks if b != curr], not level)
               for curr in tqdm(bricks))

class Brick(frozenset[Point]):
    @staticmethod
    def create(line: str):
        start, end = line.split('~')
        start, end = start.split(','), end.split(',')
        coordinates = product(*[range(int(start[i]), int(end[i]) + 1) for i in range(3)])
        return Brick(Point(*c) for c in coordinates)

    @cache  # falling is expensive, so we cache it
    def _fallen(self):
        b = Brick({p + Point(0, 0, -1) for p in self})
        return b if all(p[2] >= 0 for p in b) else None

    def fall(self, collision: Set[Point]) -> Optional['Brick']:
        fallen = self._fallen()
        if not fallen or bool(fallen & collision):
            return None
        return fallen.fall(collision) or fallen  # try to fall further, but return None if you fell 0

def simulate_falling(bricks: List[Brick], single_round: bool):
    fallen_ids = set()
    points = set().union(*bricks)
    while True:
        repeat = False
        for curr_id, curr in enumerate(bricks):
            points.difference_update(curr)
            if fallen := curr.fall(points):
                bricks[curr_id] = fallen
                fallen_ids.add(curr_id)
                repeat = True
                if single_round:
                    return False
            points.update(fallen or curr)
        if not repeat or single_round:
            break
    return single_round or len(fallen_ids)
