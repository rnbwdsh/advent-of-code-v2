import re
from itertools import combinations
from typing import List

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 1000

class Process():  # wrapper for generator
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

    def process_str(self, inp, dbg=False):
        out = self.compute([ord(c) for c in inp], dbg=dbg)
        return "".join([chr(i) if i in range(256) else str(i) for i in out])

START = 'east\ntake manifold\nsouth\ntake whirled peas\nnorth\nwest\nsouth\ntake space heater\nsouth\ntake dark matter\nnorth\neast\nnorth\nwest\nsouth\ntake antenna\nnorth\neast\nsouth\neast\ntake bowl of rice\nnorth\ntake klein bottle\nnorth\ntake spool of cat6\nwest\n'
FORBIDDEN_A = "ship are lighter than the detected"
FORBIDDEN_B = "ship are heavier than the detected"

def test_25(data: List[int], level_a):
    # enter inv to get list of all items

    # ignored items: escape pod, giant electromagnet, photons, molten lava, infinite loop
    # manually explored maze and took all the items
    p = Process(data)
    p.process_str(START)

    # trim away "Items in sour inventory" before and "\nCommand?\n" after and generate drop commands
    items = p.process_str("inv\n").replace("-", "drop").split("\n")[2:-3]

    # try to drop any amount of items until you are allowed to pass the door
    for i in range(len(items)):
        for ic in combinations(items, i):
            out = Process(data).process_str(START + "\n".join(ic) + "\nnorth\n")
            if FORBIDDEN_A not in out and FORBIDDEN_B not in out:
                return int(re.findall("\d+", out)[0])
