import re
from typing import List

import pytest
from z3 import z3

@pytest.mark.data("""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""", '4,6,3,5,6,3,5,2,1,0', None)
def test_17(data: str, level):
    regex = r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.+)"
    a, aa, c, program = re.match(regex, data).groups()
    a, aa, c = int(a), int(aa), int(c)
    program = list(map(int, program.split(',')))
    out = simulate(program, a, aa, c)
    if not level:
        return ",".join(map(str, out))
    # only do for real data, as it breaks for testdata
    if a != 729:
        a = z3.BitVec('a', 64)
        res_sym = simulate(program, a, jmp_cnt=len(program))
        s = z3.Optimize()
        for expected, formula in zip(program, res_sym):
            s.add(formula == expected)
        s.minimize(a)
        if s.check() == z3.sat:
            m = s.model()
            return m[a].as_long()


def simulate(program: List[int], a: int, b=0, c=0, jmp_cnt=None):
    pc = 0
    out = []
    while pc < len(program):
        literal = combo = program[pc + 1]
        match combo:
            case 4: combo = a
            case 5: combo = b
            case 6: combo = c

        match program[pc]:
            case 0:
                a = a >> combo
            case 1:
                b ^= literal
            case 2:
                b = combo & 7
            case 3:
                if jmp_cnt is not None:
                    if jmp_cnt < 0:
                        return out
                    jmp_cnt -= 1
                if jmp_cnt is not None or a != 0:
                    pc = literal
                    continue
            case 4:
                b = b ^ c
            case 5:
                out.append(combo & 7)
            case 6:
                b = a >> combo
            case 7:
                c = a >> combo
        pc += 2
    return out
