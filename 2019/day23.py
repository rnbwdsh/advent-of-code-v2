from collections import Counter
from typing import List

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 1000

class Process:  # wrapper for generator
    def __init__(self, data, ptr=0, dbg=False):
        self.d = data[:] + [0] * EXT_MEM  # copy + extend memory
        self.done = False
        self.base = 0
        self.ptr = ptr

    def parse_ins(self, ptr, dbg=False):
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
        if dbg: print(ptr, IN_NAME[ins], param[:size],
                      self.d[ptr:ptr + 4], sep="\t")  # debug print
        return [ins] + param

    def compute(self, inp, dbg=False):
        out = []
        ptr = self.ptr
        d = self.d  # initializations
        while ptr < len(d):  # stop on EOF
            ins, p1, p2, p3 = self.parse_ins(ptr, dbg=dbg)
            if ins == 1:
                d[p3] = d[p1] + d[p2]  # add
            elif ins == 2:
                d[p3] = d[p1] * d[p2]  # mul
            elif ins == 3:  # read
                if not inp: self.ptr = ptr; return out;  # wait/flush
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

    def process_str(self, inp):
        out = self.compute([ord(c) for c in inp])
        return "".join([chr(i) if i in range(256) else str(i) for i in out])


def test_23(data: List[int], level):
    proc, packets, nat = [], [], []
    a = b = 0  # avoid unreferenced variable error
    ctr = Counter()

    # init processors and send -1 package
    for i in range(50):
        proc.append(Process(data))
        packets += proc[i].compute([i, -1])

    # network loop: send and collect packets
    for i in range(100):  # repeat arbitrary amount of times
        while packets:  # false if empty
            dest, x, y = packets.pop(0), packets.pop(0), packets.pop(0)
            if dest == 255:  # 255 package goes to nat
                if i == 0: a = y  # save first nat package for later
                nat = [x, y]  # overwrite nat package
            else:  # normal case: process package
                packets += proc[dest].compute([x, y])

        # after all packets have been sent, send nat package to proc0
        packets += proc[0].compute(nat[:])

        # check if a message was sent twice
        ctr.update({nat[1]: 1})  # increase counter for current y by 1
        mc = ctr.most_common()[0]  # tuple (most_common_element, cnt)
        if mc[1] == 2: b = mc[0]; break
    return b if level else a
