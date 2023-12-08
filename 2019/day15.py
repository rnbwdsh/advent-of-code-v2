from typing import List

import networkx as nx

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 1000
MOVEMENT = {1: 1, 2: -1, 3: 1j, 4: -1j}


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
                self.done = True
                return out  # ret
            else:
                print(f"invalid opcode {ins} @ {ptr}")  # err
            ptr += IN_SIZE[ins]  # jmp is compensated with -3    # move ptr


def labyrinth(data: List[int]):
    g = nx.Graph()
    todo = [(Process(data), 0, [0])]
    oxygen = steps_total = 0  # to avoid uninitialized variable warnings
    while todo:
        p, steps, pos = todo.pop()
        for m in MOVEMENT:
            npos = pos[-1] + MOVEMENT[m]
            if npos not in pos:
                pc = Process(p.d, ptr=p.ptr)
                status = pc.process(inp=[m])[0]
                if status != 0: g.add_edge(pos[-1], npos)
                if status == 1:
                    todo += [[pc, steps + 1, [*pos, npos]]]
                elif status == 2:
                    steps_total = steps + 1
                    oxygen = npos
    return steps_total, list(nx.single_target_shortest_path_length(g, oxygen))[-1][1]

def test_15(data: List[int], level):
    return labyrinth(data)[level]
