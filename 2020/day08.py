from typing import List

def interpret(lines: List[str], level: int):
    seen = set()
    acc = ptr = 0
    for _ in range(10000):
        if (ptr in seen and level == 0) or ptr >= len(lines): return acc

        instr, arg = lines[ptr]
        if instr == "acc":
            acc += int(arg)
        elif instr == "jmp":
            ptr += int(arg) - 1

        seen.add(ptr)
        ptr += 1
    return False

def test_08(data, level):
    lines = [line.split(" ") for line in data]
    if level:
        for i in range(len(lines)):
            lc = [l[:] for l in lines]
            swap = {"nop": "jmp", "jmp": "nop", "acc": "acc"}
            lc[i][0] = swap[lc[i][0]]
            if lc[i][0] != "acc":
                res = interpret(lc, level)
                if res is not False:
                    return res
    return interpret(lines, level)
