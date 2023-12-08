from collections import defaultdict
from typing import List

import matplotlib.pyplot as plt
import numpy as np

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 1000

class Process:  # wrapper for generator
    def __init__(self, data, inp=None):
        self.d = data[:] + [0] * EXT_MEM  # copy + extend memory
        self.done = False
        self.pg = self.process_gen()
        self.inp = inp or []
        self.base = 0

    def compute(self, inp):
        self.inp = inp
        return next(self.pg)

    def proc_data(self, inp):
        self.compute(inp)
        return self.d[:-EXT_MEM]

    def parse_ins(self, ptr):
        param = [0, 0, 0]
        ins = self.d[ptr] % 100
        modes = [self.d[ptr] // 10 ** e % 10 for e in range(2, 5)]
        for i, mode in enumerate(modes):
            size = IN_SIZE[ins] - 1
            if i < size:
                p = ptr + 1 + i
                if mode == 0:  param[i] = self.d[p]  # position
                if mode == 1:  param[i] = p  # intermediate
                if mode == 2:  param[i] = self.base + self.d[p]  # relative
        return [ins] + param

    def process_gen(self):
        out = []
        ptr = 0
        d = self.d  # initializations
        while ptr < len(d):  # stop on EOF
            ins, p1, p2, p3 = self.parse_ins(ptr)
            if ins == 1:
                d[p3] = d[p1] + d[p2]  # add
            elif ins == 2:
                d[p3] = d[p1] * d[p2]  # mul
            elif ins == 3:  # read
                if not self.inp: yield out; out = []  # wait/flush
                d[p1] = self.inp.pop(0)  # read
            elif ins == 4:
                out.append(d[p1])  # print
            elif ins == 5:
                ptr = d[p2] - 3 if d[p1] else ptr  # jnz
            elif ins == 6:
                ptr = d[p2] - 3 if not d[p1] else ptr  # jz
            elif ins == 7:
                d[p3] = int(d[p1] < d[p2])  # lt
            elif ins == 8:
                d[p3] = int(d[p1] == d[p2])  # eq
            elif ins == 9:
                self.base += d[p1]  # base
            elif ins == 99:
                self.done = True
                yield out  # ret
            else:
                print(f"invalid opcode {ins} @ {ptr}")  # err
            ptr += IN_SIZE[ins]  # jmp is compensated with -3    # move ptr

BLACK, WHITE = 0, 1

def paint_ship(data, start_col=BLACK):
    ship = defaultdict(int)
    pos = 0
    direction = 1j
    lr = {0: 1j, 1: -1j}
    ship[pos] = start_col

    p = Process(data)
    while not p.done:
        curr_col = ship[pos]
        next_col, next_dir = p.compute([curr_col])
        ship[pos] = next_col
        direction *= lr[next_dir]
        pos += direction
    return ship

def show(ship):
    real = [int(i.real) for i in ship.keys()]  # get real compontents
    imag = [int(i.imag) for i in ship.keys()]  # get imag components
    minr, maxr, mini, maxi = min(real), max(real), min(imag), max(imag)  # get ranges
    arr = np.zeros((maxr - minr + 1, maxi - mini + 1))  # create canvas with enough size
    for pos, col in ship.items():
        x, y = pos.real - minr, pos.imag - mini
        arr[int(x), int(y)] = col
    plt.imshow(np.rot90(arr), cmap="Greys")

def test_11(data: List[int], level_a):
    painted = paint_ship(data, level_a)
    if not level_a:
        return len(painted)
    else:
        show(painted)
