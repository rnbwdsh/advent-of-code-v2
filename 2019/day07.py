from itertools import permutations
from typing import List

class Process:  # wrapper for generator
    def __init__(self, data):
        self.d = data[:]  # copy
        self.done = False
        self.pg = self.process_gen()
        self.inp = []

    def compute(self, inp):
        self.inp = inp
        return next(self.pg)

    def proc_data(self, inp):
        self.compute(inp)
        return self.d

    def process_gen(self):
        out = []
        ptr = 0
        d = self.d  # initializations
        in_size = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 0}
        while ptr < len(d):  # stop on EOF
            ins, m1, m2, m3 = [d[ptr] % 100] + [d[ptr] // 10 ** e % 10 for e in range(2, 5)]
            p1 = p2 = p3 = 0  # default
            if in_size[ins] > 0: p1 = ptr + 1 if m1 else d[ptr + 1]  # load p1-p3
            if in_size[ins] > 1: p2 = ptr + 2 if m2 else d[ptr + 2]  # if used
            if in_size[ins] > 2: p3 = ptr + 3 if m3 else d[ptr + 3]  #
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
            elif ins == 99:
                self.done = True
                yield out  # ret
            else:
                raise ValueError(f"Unknown instruction {ins} at {ptr}")
            ptr += in_size[ins]  # jmp is compensated with -3    # move ptr

def chain_process(prog, inl, out):
    proc = [Process(prog) for _ in inl]
    for epoch in range(100000):
        for i, inp in enumerate(inl):
            out = proc[i].compute(([inp] if epoch == 0 else []) + out)
            if proc[i].done and i == len(inl) - 1:  # if the last is done, get out
                return out[0]

def chain_process_loop(prog, ran):  # search all permutations
    best = {chain_process(prog, inp, [0]): inp for inp in permutations(ran)}
    best_k = max(best.keys())
    return best_k, list(best[best_k])  # return (best score, best permutation)

def test_07(data: List[int], level):
    return chain_process_loop(data, range(5, 10) if level else range(5))[0]
