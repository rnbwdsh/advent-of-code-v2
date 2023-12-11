from typing import List

import numpy as np

from computer import Computer
from parsers import parse_array

RNG = np.random.default_rng(42)


def frame(field):  # draw a "." frame around view
    nf = np.full((field.shape[0] + 2, field.shape[1] + 2), ".")
    nf[1:-1, 1:-1] = field
    return nf

def path(field, curr_dir=-1):
    field = frame(field)
    pos = np.nonzero(np.equal(field, "^"))
    pos = int(pos[0]) + int(pos[1]) * 1j
    movement = ""
    dist = 0  # avoid uninitialized variable warning
    for _ in range(100):
        for dire in [1, 3]:
            ndir = curr_dir * 1j ** dire
            if field[t2c(pos + ndir)] == '#':
                movement += " L R"[dire]
            else:
                continue
            for dist in range(100):
                if field[t2c(pos + ndir * (dist + 1))] == ".":
                    break
            movement += str(dist) + ","
            pos += ndir * dist
            curr_dir = ndir
    return movement[:-1]

def compress(orig):
    line = orig.split(",")
    while True:
        ol = orig  # reset replacement
        sl = []  # reset substitution list
        splits = sorted(RNG.integers(0, len(line), 6))
        for i in range(0, 6, 2):
            pattern = ",".join(line[splits[i]: splits[i + 1]])  # get subpattern
            if len(pattern) > 20: break  # exit if it's too long
            sign = "ABC"[i // 2]  # pick A for 0, B for 1...
            ol = ol.replace(pattern, sign)  # build sign
            sl.append(pattern)  # append to output arrays
        if len(set(ol)) == 4:  # must be [ABC,]
            return [ol] + sl

t2c = lambda pos: tuple([int(pos.real), int(pos.imag)])  # tuple 2 complex

C, L, R, U, D = (0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)

def test_17(data: List[int], level):
    field = Computer(data, ext_mem=100_000).compute([1])
    field = parse_array("".join([chr(i) for i in field]).strip())
    if level:
        inp = [ord(c) for c in "\n".join(compress(path(field)) + ["n\n"]).replace("R", "R,").replace("L", "L,")]
        res = (Computer([2] + data[1:]).compute(inp))
        return res[-1]

    total = 0
    for pos, val in np.ndenumerate(field):
        try:
            cmp = np.array([field[tuple(np.array(pos) + p)] for p in [C, L, R, U, D]])
            if all(np.not_equal(cmp, ".")):
                total += pos[0] * pos[1]
                field[pos] = "O"
        except IndexError:
            pass
    return total
