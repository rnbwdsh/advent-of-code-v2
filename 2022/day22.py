import re
from dataclasses import dataclass
from typing import Tuple, List, Dict, NamedTuple

import numpy as np

# based on https://github.com/blubber-rubber/AdventOfCode2022/blob/main/Day22/part2.py
ROTATIONS = ['^', '>', 'v', '<']
DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def test_22(data, level):
    # Pad lines to make them all the same length (required for numpy)
    line_len = max(len(line) for line in data[:-2])
    world = np.array([list(line + " " * (line_len - len(line))) for line in data[:-2]])
    block_size = int((np.sum(world != " ") / 6) ** 0.5)
    d, face, faces = 0, None, []  # to avoid warnings
    if level:
        faces = create_faces(world, block_size)
        face = faces["U"]
        y = x = 0
    else:
        world = np.pad(world, 1, constant_values=" ")
        y, x = list(zip(*np.nonzero("." == world)))[0]  # noqa  # numpy typing error

    for token in re.findall(r"(\d+|[RL])", data[-1]):
        if not token.isnumeric():  # Rotation direction
            d += [-1, 1][token == "R"]
            d %= 4
            continue
        for _ in range(int(token)):  # stepping instruction
            xn, yn = x + DIR[d][0], y + DIR[d][1]
            if level:  # move on face
                if 0 <= xn < block_size and 0 <= yn < block_size:  # Check if we are crossing an edge
                    face_next = face  # no edge crossed, face stays same
                else:  # An edge was crossed
                    face_name, direction = stamps[face.no.name].rotate_until(face.no)[d]
                    face_next = faces[face_name]
                    while face_next.no.orientation != direction:  # Align the neighbouring face with stamp
                        face_next.rotate()
                    xn %= block_size
                    yn %= block_size
                if face_next.world[yn][xn] == "#":
                    break
                face = face_next
            else:
                if world[yn, xn] == " ":
                    while world[yn - DIR[d][1], xn - DIR[d][0]] != " ":
                        xn -= DIR[d][0]
                        yn -= DIR[d][1]
                if world[yn, xn] == "#":
                    break
            x, y = xn, yn

    if level:
        x, y, d = face.rotate_to_original(x, y, d, block_size)

    return y * 1000 + x * 4 + d

class NameOrientation(NamedTuple):  # allows indexing and regular property accesss
    name: str
    orientation: str

    @property
    def next_rotation(self) -> 'NameOrientation':
        r_index = ROTATIONS.index(self.orientation)
        return NameOrientation(self.name, ROTATIONS[(r_index + 1) % 4])

@dataclass
class Stamp:
    _name_orientation: NameOrientation | Tuple[str, str]
    _neighbors: List[NameOrientation | Tuple[str, str]]

    def __post_init__(self):  # map to Symbol
        self._name_orientation = NameOrientation(*self._name_orientation)
        self._neighbors = [NameOrientation(*n) for n in self._neighbors]

    def rotate_until(self, name_orientation: NameOrientation):
        while self._name_orientation != name_orientation:
            self._name_orientation = self._name_orientation.next_rotation
            self._neighbors = [n.next_rotation for n in self._neighbors]
            self._neighbors = self._neighbors[-1:] + self._neighbors[:-1]
        return self._neighbors

stamps = {'U': Stamp(('U', '^'), [('L', '>'), ('B', 'v'), ('R', '<'), ('F', '^')]),  # noqa
          'D': Stamp(('D', '^'), [('R', '<'), ('B', '^'), ('L', '>'), ('F', 'v')]),  # noqa
          'F': Stamp(('F', '^'), [('L', '^'), ('U', '^'), ('R', '^'), ('D', 'v')]),  # noqa
          'B': Stamp(('B', '^'), [('R', '^'), ('U', 'v'), ('L', '^'), ('D', '^')]),  # noqa
          'L': Stamp(('L', '^'), [('B', '^'), ('U', '<'), ('F', '^'), ('D', '<')]),  # noqa
          'R': Stamp(('R', '^'), [('F', '^'), ('U', '>'), ('B', '^'), ('D', '>')])}  # noqa

@dataclass
class Face:
    no: NameOrientation
    world: np.ndarray
    pos_abs: Tuple[int, int]

    def __post_init__(self):
        self.no = NameOrientation(*self.no)
        self.orientation_original = self.no.orientation

    def rotate(self):
        self.no = self.no.next_rotation
        self.world = np.rot90(self.world, k=-1)

    def rotate_to_original(self, x: int, y: int, d: int, side_length: int) -> Tuple[int, int, int]:
        while self.no.orientation != self.orientation_original:
            self.rotate()
            x, y = side_length - 1 - y, x
            d = (d + 1) % len(DIR)
        return x + self.pos_abs[0] + 1, y + self.pos_abs[1] + 1, d

def create_faces(grid: np.ndarray, block_size: int) -> Dict[str, Face]:
    """ Generates a dictionary that maps a face to the mini-square it corresponds to in the grid
    and its orientation in the grid. It then """
    w, h = grid.shape
    pos_square = {(y, x): grid[x:x + block_size, y:y + block_size]
                  for x in range(0, w, block_size)
                  for y in range(0, h, block_size)
                  if np.all(grid[x:x + block_size, y:y + block_size] != " ")}

    # positions of squares in the grid
    p0 = min(pos_square, key=lambda x: (x[1], x[0]))
    position_queue = [p0]  # positions to be stamped
    mappings = {p0: NameOrientation("U", "^")}  # Mini-square to face and orientation
    faces = {"U": Face(("U", "^"), pos_square[p0], p0)}  # noqa E203

    seen = set()  # positions already stamped
    while position_queue:  # Still positions to be stamped
        pos = x, y = position_queue.pop(0)
        seen.add(pos)
        face = mappings[pos][0]
        neighbour_faces = stamps[face].rotate_until(mappings[pos])
        for i, name_orientation in enumerate(neighbour_faces):
            pos = (x + DIR[i][0] * block_size, y + DIR[i][1] * block_size)
            if pos in pos_square and pos not in seen:  # Check if we need to stamp the neighbours
                position_queue.append(pos)
                mappings[pos] = name_orientation
                faces[name_orientation[0]] = Face(name_orientation, pos_square[pos], pos)  # noqa E203
    return faces