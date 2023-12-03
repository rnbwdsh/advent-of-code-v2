from level_annotations import level_ab

@level_ab(8)
def solve(data, method=0):
    def interpret(lines):
        seen = set()
        acc = ptr = 0
        for icnt in range(10000):
            if (ptr in seen and method == 0) or ptr >= len(lines): return acc

            instr, arg = lines[ptr]
            if instr == "acc":
                acc += int(arg)
            elif instr == "jmp":
                ptr += int(arg) - 1

            seen.add(ptr)
            ptr += 1
        return False

    lines = [line.split(" ") for line in data.split("\n")]
    if method:
        for i in range(len(lines)):
            lc = [l[:] for l in lines]
            swap = {"nop": "jmp", "jmp": "nop", "acc": "acc"}
            lc[i][0] = swap[lc[i][0]]
            if lc[i][0] != "acc":
                res = interpret(lc)
                if res is not False:
                    return res
    return interpret(lines)
