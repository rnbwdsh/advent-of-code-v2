import itertools
import re

from level_annotations import level_ab

@level_ab(14)
def solve(data, method=0):
    memory = {}
    mask = "X0"[method]
    for line in data:
        if line.startswith("mask = "):
            bitmask = line[7:]
        elif line.startswith("mem"):
            addr, val = re.findall("[0-9]+", line)
            to_use = addr if method else val
            padded = bin(int(to_use))[2:].rjust(36, "0")
            masked = [(a if b == mask else b) for a, b in zip(padded, bitmask)]
            if method:  # mask to list of lists with len(inner_list) == 0 or 1
                for p in itertools.product(*[["0", "1"] if letter == "X" else [letter] for letter in masked]):
                    memory[int("".join(p), 2)] = int(val)  # write multiple memory positions
            else:
                memory[int(addr)] = int("".join(masked), 2)
    return sum(memory.values())
