from dataclasses import dataclass
from typing import List, Optional
import pytest

SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1}
NAME = {1: "ADD", 2: "MUL", 3: "RED", 4: "PRT", 5: "JNZ", 6: "JZ", 7: "LT", 8: "EQ", 9: "BAS", 99: "RET"}


@dataclass
class Computer:
    """ Intcode computer for 2019/05,07,09,11,13,15,17,19,21,23,25 """
    d: List[int]
    ptr: int = 0
    base: int = 0
    done: bool = False
    yielding: bool = False
    debug: bool = False
    name: str = ""
    ext_mem: int = 10_000
    p0: Optional[int] = None
    p1: Optional[int] = None
    p2: Optional[int] = None
    size: Optional[int] = None
    ins: Optional[int] = None
    i_raw: Optional[int] = None

    def __post_init__(self):
        self.d = self.d[:] + [0] * self.ext_mem

    def parse_ins(self):
        self.i_raw = self.d[self.ptr]
        self.ins = self.i_raw % 100
        self.size = SIZE[self.ins]
        if self.size > 0 + 1:
            self.p0 = self.parse_param(0, 100)
            if self.size > 1 + 1:
                self.p1 = self.parse_param(1, 1000)
                if self.size > 2 + 1:
                    self.p2 = self.parse_param(2, 10000)

    def parse_param(self, i, e):
        p = self.ptr + 1 + i
        match self.i_raw // e % 10:
            case 0:
                return self.d[p]  # position
            case 1:
                return p  # intermediate
            case 2:
                return self.base + self.d[p]  # relative

    def compute(self, inp=None, extra_mem=0):
        self.d += [0] * extra_mem
        inp = inp or []
        out = []

        while self.ptr < len(self.d):
            self.parse_ins()
            if self.debug:
                self.debug_print()
            match self.ins:
                case 1:  # ADD
                    self.d[self.p2] = self.d[self.p0] + self.d[self.p1]
                case 2:  # MUL
                    self.d[self.p2] = self.d[self.p0] * self.d[self.p1]
                case 3:  # READ
                    if not inp:
                        return out
                    self.d[self.p0] = inp.pop(0)
                case 4:  # PRINT
                    out.append(self.d[self.p0])
                case 5:  # JNZ
                    if self.d[self.p0]:
                        self.ptr = self.d[self.p1]
                        continue
                case 6:  # JZ
                    if not self.d[self.p0]:
                        self.ptr = self.d[self.p1]
                        continue
                case 7:  # LT
                    self.d[self.p2] = int(self.d[self.p0] < self.d[self.p1])
                case 8:  # EQ
                    self.d[self.p2] = int(self.d[self.p0] == self.d[self.p1])
                case 9:  # BASE
                    self.base += self.d[self.p0]
                case 99:  # RET
                    self.done = True
                    return out
                case _:  # ERR
                    raise ValueError(f"Unknown instruction {self.ins} at {self.ptr}")
            self.ptr += self.size
        return out

    def debug_print(self):
        raw_ins = self.d[self.ptr:self.ptr + self.size]
        written = None
        if self.ins == 3:
            written = self.d[self.p0]
        elif self.ins == 4:
            written = self.p0
        elif self.ins == 5 or self.ins == 6:
            written = self.ptr
        print(self.name, self.ptr, NAME[self.ins], self.p0 or '-', self.p1 or '-', self.p2 or '-', "=", written, "raw = " + " ".join(map(str, raw_ins)), sep="\t")

    def compute_str(self, inp):
        inp = [ord(c) for c in inp]
        ret = self.compute(inp)
        return "".join([chr(i) if i < 256 else str(i) for i in ret])

    def compute_mem_after(self, inp=None):
        self.compute(inp)
        return self.d

@pytest.mark.parametrize("data", [
    # tests from 2019/day02.py
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
    # tests from 2019/day05.py - immediate mode
    ([1002,4,3,4,33], [1002,4,3,4,99])])
def test_compute_mem_after(data):
    input_data,expected_output = data
    assert Computer(input_data, ext_mem=0).compute_mem_after() == expected_output

@pytest.mark.parametrize("data", [
    # tests from 2019/day05.py - immediate mode
    ([3,9,8,9,10,9,4,9,99,-1,8], [42], [0]),
    ([3,9,8,9,10,9,4,9,99,-1,8], [8], [1]),
    ([3,9,7,9,10,9,4,9,99,-1,8], [42], [0]),
    ([3,9,7,9,10,9,4,9,99,-1,8], [7], [1]),
    ([3,3,1108,-1,8,3,4,3,99], [42], [0]),
    ([3,3,1108,-1,8,3,4,3,99], [8], [1]),
    ([3,3,1107,-1,8,3,4,3,99], [42], [0]),
    ([3,3,1107,-1,8,3,4,3,99], [7], [1])])
def test_imm(data):
    input_data,input_run,expected_output = data
    assert Computer(input_data).compute(input_run, extra_mem=1000_000) == expected_output


@pytest.mark.parametrize("data", [
    # tests from 2019/day09.py - relative mode
    ([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [], [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]),
    ([1102,34915192,34915192,7,4,7,99,0], [], [1219070632396864]),
    ([104,1125899906842624,99], [], [1125899906842624])])
def test_rel(data):
    input_data,input_run,expected_output = data
    assert Computer(input_data).compute(input_run, extra_mem=1000_000) == expected_output
