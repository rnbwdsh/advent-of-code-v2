from typing import List

import numpy as np

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 1000
EMPTY, WALL, BLOCK, HPAD, BALL = range(5)
CONTROLS = {"a": 1, "s": 0, "d": -1}

class Process:  # wrapper for generator
    def __init__(self, data, inp):
        self.d = data[:] + [0] * EXT_MEM  # copy + extend memory
        self.done = False
        self.pg = self.process_gen()
        self.inp = inp or []
        self.base = 0

    def calc(self, inp):
        self.inp = inp or []
        return next(self.pg)

    def proc_data(self, inp):
        self.calc(inp)
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

def play_game(data):
    p = Process([2] + data[1:], [])  # set d[0] = 2 to insert 2 coins
    pos_ball = pos_pad = 0  # just for step 0
    score = 0
    while not p.done:
        output = p.calc([np.sign(pos_ball - pos_pad)])
        # display routine: draw tile @ x/y if x/y is not -1/0 and remember pos_ball/hpad
        for i in range(0, len(output), 3):
            x, y, tile = output[i:i + 3]
            if x == -1 and y == 0:
                score = tile
            else:
                if tile == BALL:
                    pos_ball = x
                elif tile == HPAD:
                    pos_pad = x
    return score

def test_13(data: List[int], level):
    p = Process(data, [])
    prog_out = np.array(p.calc([]))
    # select every 3rd block and count how many are type block
    return play_game(data) if level else sum(np.equal(prog_out[range(2, len(prog_out), 3)], BLOCK))
