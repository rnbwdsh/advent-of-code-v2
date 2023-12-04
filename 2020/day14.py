import itertools
import re
from typing import List

def write_positions(masked, memory, val):
    for p in itertools.product(*[["0", "1"] if letter == "X" else [letter] for letter in masked]):
        memory[int("".join(p), 2)] = int(val)  # write multiple memory positions

def test_14(data: List[str], level):
    memory = {}
    mask = "X0"[level]
    for line in data:
        if line.startswith("mask = "):
            bitmask = line[7:]
        elif line.startswith("mem"):
            addr, val = re.findall("\d+", line)
            to_use = addr if level else val
            padded = bin(int(to_use))[2:].rjust(36, "0")
            masked = [(a if b == mask else b) for a, b in zip(padded, bitmask)]  # noqa maybe unused
            if level:  # mask to list of lists with len(inner_list) == 0 or 1
                write_positions(masked, memory, val)
            else:
                memory[int(addr)] = int("".join(masked), 2)
    return sum(memory.values())
