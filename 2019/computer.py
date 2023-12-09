from dataclasses import dataclass
from typing import List

IN_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
SIZES = [None, 100, 1000, 10_000]


@dataclass
class Computer:
    mem: List[int]
    ptr: int = 0
    base: int = 0
    done: bool = False

    def run(self, inp=None):
        inp = inp or [] + [None] * 10
        out = []

        while self.ptr < len(self.mem):
            i_raw = self.mem[self.ptr]
            instr = i_raw % 100
            size = IN_SIZE[instr]

            p0 = p1 = p2 = None
            if size > 1:
                p0 = self.mem[self.ptr + 1]
                if (i_raw // 100) % 10 == 0 and instr != 3:
                    p0 = self.mem[p0]
            if size > 2:
                p1 = self.mem[self.ptr + 2]
                if (i_raw // 1000) % 10 == 0:
                    p1 = self.mem[p1]
            if size > 3:
                p2 = self.mem[self.ptr + 3]
                if (i_raw // 10000) % 10 == 0 and size != 4:
                    p2 = self.mem[p2]

            match instr % 100:
                case 1:  # ADD
                    self.mem[p2] = p0 + p1
                case 2:  # MUL
                    self.mem[p2] = p0 * p1
                case 3:  # READ
                    if not inp:
                        return out
                    self.mem[p0] = inp.pop(0)
                case 4:  # PRINT
                    out.append(p0)
                case 5:  # JNZ
                    self.ptr = p1 - size if p0 else self.ptr
                case 6:  # JZ
                    self.ptr = p1 - size if not p0 else self.ptr
                case 7:  # LT
                    self.mem[p2] = int(p0 < p1)
                case 8:  # EQ
                    self.mem[p2] = int(p0 == p1)
                case 9:  # BASE
                    self.base += self.mem[p0]
                case 99:  # RET
                    self.done = True
                    return out
                case _:  # ERR
                    raise ValueError(f"Unknown instruction {instr} at {self.ptr}")
            self.ptr += size
        return out

    def compute_str(self, inp):
        inp = [ord(c) for c in inp]
        ret = self.run(inp)
        return "".join([chr(i) if i < 256 else str(i) for i in ret])

    def compute_mem_after(self, inp=None):
        self.run(inp)
        return self.mem

# tests from 2019/day02.py
assert(Computer([1,0,0,0,99]).compute_mem_after() == [2,0,0,0,99])
assert(Computer([2,3,0,3,99]).compute_mem_after() == [2,3,0,6,99])
assert(Computer([2,4,4,5,99,0]).compute_mem_after() == [2,4,4,5,99,9801])
assert(Computer([1,1,1,4,99,5,6,0,99]).compute_mem_after() == [30,1,1,4,2,5,6,0,99])

# tests from 2019/day05.py - immediate mode
assert(Computer([1002,4,3,4,33]).compute_mem_after() == [1002,4,3,4,99])

# test equal to 8
assert(Computer([3,9,8,9,10,9,4,9,99,-1,8]).run([42]) == [0])
assert(Computer([3,9,8,9,10,9,4,9,99,-1,8]).run([8]) == [1])

# test less than 8
assert(Computer([3,9,7,9,10,9,4,9,99,-1,8]).run([42]) == [0])
assert(Computer([3,9,7,9,10,9,4,9,99,-1,8]).run([7]) == [1])

# test equal to 8 imm
assert(Computer([3,3,1108,-1,8,3,4,3,99]).run([42]) == [0])
assert(Computer([3,3,1108,-1,8,3,4,3,99]).run([8]) == [1])

# test less than 8 imm
assert(Computer([3,3,1107,-1,8,3,4,3,99]).run([42]) == [0])
assert(Computer([3,3,1107,-1,8,3,4,3,99]).run([7]) == [1])


