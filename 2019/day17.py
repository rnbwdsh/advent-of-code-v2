from typing import List

import numpy as np

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 10000
RNG = np.random.default_rng(42)

class Process:  # wrapper for generator
    def __init__(self, data, ptr=0):
        self.d = data[:] + [0] * EXT_MEM  # copy + extend memory
        self.done = False
        self.base = 0
        self.ptr = ptr

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

    def process(self, inp):
        out = []
        ptr = self.ptr
        d = self.d  # initializations
        while ptr < len(d):  # stop on EOF
            ins, p1, p2, p3 = self.parse_ins(ptr)
            if ins == 1:
                d[p3] = d[p1] + d[p2]  # add
            elif ins == 2:
                d[p3] = d[p1] * d[p2]  # mul
            elif ins == 3:  # read
                if not inp:
                    self.ptr = ptr
                    return out  # wait/flush
                d[p1] = inp.pop(0)  # read
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
                self.done = True; return out  # ret
            else:
                print(f"invalid opcode {ins} @ {ptr}")  # err
            ptr += IN_SIZE[ins]  # jmp is compensated with -3    # move ptr

def parse(text):
    return np.array([list(c) for c in text.strip().split("\n")])

def il2str(il):
    return "".join([chr(i) for i in il])

def calc(field):
    s = 0
    for pos, val in np.ndenumerate(field):
        try:
            cmp = np.array([field[tuple(np.array(pos) + p)]
                            for p in [[0, 0], [0, 1], [1, 0], [-1, 0], [0, -1]]])
            if all(np.not_equal(cmp, ".")):
                s += pos[0] * pos[1]
                field[pos] = "O"
        except IndexError:
            pass
    return s

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


def test_17(data: List[int], level):
    field = parse(il2str(Process(data).process(inp=[1])))
    if not level:
        return calc(field)
    inp = [ord(c) for c in "\n".join(compress(path(field)) + ["n\n"]).replace("R", "R,").replace("L", "L,")]
    res = (Process([2] + data[1:]).process(inp))
    return res[-1]
