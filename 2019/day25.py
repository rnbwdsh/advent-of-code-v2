import re
from itertools import combinations

import aocd

data = list([int(d) for d in aocd.get_data(day=25).split(",")])
print(data)

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

    def process(self, inp, dbg=False):
        out = [];
        ptr = self.ptr;
        d = self.d  # initializations
        parse = lambda i: [i % 100] + [i // 10 ** e % 10 for e in range(2, 5)]
        while ptr < len(d):  # stop on EOF
            ins, p1, p2, p3 = self.parse_ins(ptr, dbg=dbg)
            # if dbg:print(ptr, d)                              # debug print
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
        out = self.process([ord(c) for c in inp], dbg=dbg)
        return "".join([chr(i) if i in range(256) else str(i) for i in out])

# ignored items: escape pod, giant electromagnet, photons, molten lava, infinite loop
# manually explored maze and took all the items
# TODO: auto-explorer with timeout for inf. loop and avoidance of death states
start = """east
take manifold
south
take whirled peas
north
west
south
take space heater
south
take dark matter
north
east
north
west
south
take antenna
north
east
south
east
take bowl of rice
north
take klein bottle
north
take spool of cat6
west
"""

# enter inv to get list of all items
p = Process(data);
p.process_str(start)
# trim away "Items in sour inventory" before and "\nCommand?\n" after and generate drop commands
items = p.process_str("inv\n").replace("-", "drop").split("\n")[2:-3]

# try to drop any amount of items until you are allowed to pass the door
for i in range(len(items)):
    for ic in combinations(items, i):
        out = Process(data).process_str(start + "\n".join(ic) + "\nnorth\n")
        if not "ship are lighter than the detected" in out \
                and not "ship are heavier than the detected" in out:
            print(ic, out)
            code = int(re.findall("\d+", out)[0])
            aocd.submit(code, day=25)
