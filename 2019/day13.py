import IPython.display
import PIL
import aocd
import numpy as np

data = list([int(d) for d in aocd.get_data().split(",")])
print(data)

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
IN_NAME = {1: "add", 2: "mul", 3: "rd", 4: "prnt", 5: "jnz", 6: "jz",
           7: "lt", 8: "eq", 9: "bas", 99: "ret"}
EXT_MEM = 1000

class Process():  # wrapper for generator
    def __init__(self, data, inp=[], dbg=False):
        self.d = data[:] + [0] * EXT_MEM  # copy + extend memory
        self.done = False
        self.pg = self.process_gen(dbg=dbg)
        self.inp = inp
        self.base = 0

    def process(self, inp=[]):
        self.inp = inp
        return next(self.pg)

    def proc_data(self, inp):
        self.process(inp)
        return self.d[:-EXT_MEM]

    def parse_ins(self, ptr, dbg):
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

    def process_gen(self, dbg):
        out = [];
        ptr = 0;
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
                self.done = True; yield out  # ret
            else:
                print(f"invalid opcode {ins} @ {ptr}")  # err
            ptr += IN_SIZE[ins]  # jmp is compensated with -3    # move ptr

# tests in other files


EMPTY, WALL, BLOCK, HPAD, BALL = range(5)

p = Process(data)
prog_out = np.array(p.process([]))
# select every 3rd block and count how many are type block
block_cnt = sum(prog_out[range(2, len(prog_out), 3)] == BLOCK)
aocd.submit(answer=block_cnt)

# In[ ]:


controls = {"a": 1, "s": 0, "d": -1}

# import matplotlib.pyplot as plt

def play_game(data, interactive=False):
    """ interactive code is commented out. control with asd """
    p = Process([2] + data[1:])  # set d[0] = 2 to insert 2 coins
    screen = np.zeros((35, 25))  # create virtual display, dimensions from part 1
    ballpos = padpos = 0  # just for step 0
    img = None
    while not p.done:
        if interactive:
            if img == None:
                output = p.process([0])  # get initial image by doing 0 for 1 frame
            else:
                output = p.process([controls[input()]])  # control with asd
                IPython.display.clear_output()
        else:  # non-interactive action: move the paddle to the ball
            output = p.process([np.sign(ballpos - padpos)])
        # display routine: draw tile @ x/y if x/y is not -1/0 and remember ballpos/hpad
        for i in range(0, len(output), 3):
            x, y, tile = output[i:i + 3]
            if x == -1 and y == 0:
                if interactive: print("score:", tile, "\r")
                score = tile
            else:
                if interactive:    screen[x, y] = tile
                if tile == BALL:
                    ballpos = x
                elif tile == HPAD:
                    padpos = x
        if interactive:
            # display 270 degree roated, brightened up x50 image, with color mode L and size 350x250
            img = PIL.Image.fromarray(np.rot90(screen, k=3) * 50).convert("L").resize((350, 250))
            IPython.display.display(img, display_id=1)
    return score

aocd.submit(answer=play_game(data))

# In[ ]:


play_game(data, interactive=True)
