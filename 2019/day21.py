from typing import List

from computer import Computer

PROG_0 = 'NOT A T\nNOT B J\nOR J T\nNOT C J\nOR T J\nAND D J\nWALK\n'
PROG_1 = 'NOT I T\nNOT T J\nOR F J\nAND E J\nOR H J\nAND D J\nNOT A T\nNOT T T\nAND B T\nAND C T\nNOT T T\nAND T J\nRUN\n'

def test_21(data: List[int], level):
    return Computer(data).compute_str(PROG_1 if level else PROG_0).split("\n")[-1]
