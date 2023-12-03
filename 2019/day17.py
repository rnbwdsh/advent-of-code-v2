import aocd
import numpy as np

data = list([int(d) for d in aocd.get_data().split(",")])
print(data)

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 10000

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

# tests in other files


parse = lambda text: np.array([list(c) for c in text.strip().split("\n")])
arr2str = lambda lines: "\n".join(["".join(line) for line in lines])
il2str = lambda il: "".join([chr(i) for i in il])

def calc(field, dbg=False):
    s = 0
    for pos, val in np.ndenumerate(field):
        try:
            cmp = np.array([field[tuple(np.array(pos) + p)]
                            for p in [[0, 0], [0, 1], [1, 0], [-1, 0], [0, -1]]])
            if all(cmp != "."):
                s += pos[0] * pos[1]
                field[pos] = "O"
        except IndexError:
            pass
    if dbg: print(arr2str(field))
    return s

assert calc(parse("""
..#..........
..#..........
##O###O...###
#.#...#...#.#
##O###O###O##
..#...#...#..
..#####...^..""")) == 76

field = parse(il2str(Process(data).process(inp=[1])))
solution = calc(field, dbg=True)
aocd.submit(solution, day=17)

c2t = lambda pos: int(pos[0]) + int(pos[1]) * 1j  # complex 2 tuple
t2c = lambda pos: tuple([int(pos.real), int(pos.imag)])  # tuple 2 complex
c2o = lambda inp: [ord(c) for c in inp]
a = 2 + 3j;
assert a == c2t(t2c(a))

def frame(field):  # draw a "." frame around view
    nf = np.full((field.shape[0] + 2, field.shape[1] + 2), ".")
    nf[1:-1, 1:-1] = field
    return nf

def path(field, currdir=-1):
    field = frame(field)
    pos = c2t(np.where(field == "^"))
    movement = ""
    for _ in range(100):
        for dire in [1, 3]:
            ndir = currdir * 1j ** dire
            if field[t2c(pos + ndir)] == '#':
                movement += " L R"[dire]
            else:
                continue
            for dist in range(100):
                if field[t2c(pos + ndir * (dist + 1))] == ".":
                    break
            movement += str(dist) + ","
            pos += ndir * dist
            currdir = ndir
    return movement[:-1]

def compress(orig):
    line = orig.split(",")
    while True:
        ol = orig  # reset replacement
        sl = []  # reset substitution list
        splits = sorted(np.random.randint(0, len(line), 6))
        for i in range(0, 6, 2):
            pattern = ",".join(line[splits[i]: splits[i + 1]])  # get subpattern
            if len(pattern) > 20: break  # exit if it's too long
            sign = "ABC"[i // 2]  # pick A for 0, B for 1...
            ol = ol.replace(pattern, sign)  # build sign
            sl.append(pattern)  # append to output arrays
        if len(set(ol)) == 4:  # must be [ABC,]
            return [ol] + sl

p = path(field)
cp = compress(p)
inp = "\n".join(cp + ["n\n"])
inp = inp.replace("R", "R,").replace("L", "L,")  # correct format
rd = Process([2] + data[1:]).process(inp=c2o(inp))
print("uncompressed:", p, "compressed:", cp, "output", il2str(rd), sep="\n")
aocd.submit(rd[-1], day=17)
