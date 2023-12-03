import re
from dataclasses import dataclass, field

import numpy as np

from level_annotations import level_ab

def overlap(a: range, b: range):
    return range(max(a.start, b.start), min(a.stop, b.stop))

@dataclass
class Cube:
    x: range
    y: range
    z: range
    state: bool
    sub: list = field(default_factory=list)

    def overlap(self, other: "Cube"):
        self.add(Cube(overlap(self.x, other.x), overlap(self.y, other.y), overlap(self.z, other.z), False))

    def add(self, other):
        if other.x and other.y and other.z:
            for sub in self.sub:
                sub.overlap(other)  # so we don't count overlapping sub-cubes
            self.sub.append(other)

    def size(self):
        return np.prod([len(d) for d in [self.x, self.y, self.z]]) - sum(sub.size() for sub in self.sub)

@level_ab(22)
def test(lines, level):
    root = Cube(range(0), range(0), range(0), False)  # container for sub-cubes with add-logic
    for line in lines:
        state = line.startswith("on")
        x0, x1, y0, y1, z0, z1 = map(int, re.findall("-?\\d+", line))
        if level or (x0 >= -50 and x1 <= 50 and y0 >= -50 and y1 <= 50 and z0 >= -50 and z1 <= 50):
            root.add(Cube(range(x0, x1 + 1), range(y0, y1 + 1), range(z0, z1 + 1), state))
    return sum(c.size() for c in root.sub if c.state)
