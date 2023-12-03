import itertools

import numpy as np

from level_annotations import level_ab

ROTATORS = [(mul, channels) for channels in itertools.permutations([0, 1, 2]) for mul in
            itertools.product([1, -1], repeat=3)]

class Scanner:
    def __init__(self, lines):
        hdr, *beacons = lines.split("\n")
        self.id = int(hdr.split()[2])
        self.beacons = np.array([[int(i) for i in b.split(",")] for b in beacons])
        rel_lines = np.array(
            [b - self.beacons for b in self.beacons])  # calculate relative distances between beacons in scanner range
        self.perm = [[frozenset([tuple(list(row)) for row in line])
                      # create List(frozenset(tuples(positions)), to cross-check list with others
                      for line in rel_lines[:, :, channels] * mul]
                     for (mul, channels) in ROTATORS]  # precompute all possible rotations
        self.heuristic = set(np.absolute((rel_lines ** 2).sum(axis=-1).flatten()))
        if self.id == 0:
            self.perm = self.perm[0]
            self.aligned = True

    pos = np.array([0, 0, 0])
    aligned = False

    def align(self, other: "Scanner"):
        if self.aligned or not other.aligned or len(self.heuristic & other.heuristic) < 10: return
        for i_other, perm_other in enumerate(other.perm):
            for rot_id, perms in enumerate(self.perm):
                for i, perm in enumerate(perms):
                    if len(perm & perm_other) >= 12:  # the relative to self dist = 0 is missing
                        mul, channels = ROTATORS[rot_id]
                        self.beacons = self.beacons[:, channels] * mul
                        self.pos = other.beacons[i_other] - self.beacons[i]
                        self.perm = self.perm[rot_id]
                        self.beacons += self.pos
                        self.aligned = True
                        # print(f"Rotation {rot_id} scanner {self.id} of {other.id}\t\tItems: {len(perm & perm_other)} / {len(self.perm[0])}\t\tPos {other.id}: {other.pos} with heuristic {len(self.heuristic & other.heuristic)}")
                        return

@level_ab(19, sep="\n\n")
def test(data, level):
    scanners = [Scanner(chunk) for chunk in data]
    while not all(s.aligned for s in scanners):
        for a, b in itertools.permutations(scanners, 2):
            a.align(b)
    return max(np.abs(a.pos - b.pos).sum() for a, b in itertools.combinations(scanners, 2)) if level else \
        len({tuple(pos) for s in scanners for pos in s.beacons})  # number of unique points in a set
