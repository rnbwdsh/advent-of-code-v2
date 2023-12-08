def test_05(data: str, level):
    d = [int(d) for d in data.replace("\n", "").split(",")]  # don't modify original, return modified copy
    ptr, out, debug = 0, [], False
    while ptr < len(d):  # stop on EOF
        ins, p1m, p2m, p3m = [d[ptr] % 100] + [d[ptr] // 10 ** e % 10 for e in range(2, 5)]
        if ins == 99:
            break
        ins_size = {1: 4, 2: 4, 3: 2, 4: 2, 5: 0, 6: 0, 7: 4, 8: 4, 99: 0}
        size = ins_size[ins]
        p1 = ptr + 1 if p1m else d[ptr + 1]
        p2 = p3 = 0  # default
        if size > 1:
            p2 = ptr + 2 if p2m else d[ptr + 2]
        if size > 2:
            p3 = ptr + 3 if p3m else d[ptr + 3]
        if debug:    print(ptr, d[ptr:ptr + 4])  # debug
        if ins == 1:
            d[p3] = d[p1] + d[p2]  # add
        elif ins == 2:
            d[p3] = d[p1] * d[p2]  # mul
        elif ins == 3:
            d[p1] = 5 if level else 1  # read
        elif ins == 4:
            out.append(d[p1])  # print
        elif ins == 5:
            ptr = d[p2] if d[p1] else ptr + 3  # je
        elif ins == 6:
            ptr = d[p2] if not d[p1] else ptr + 3  # jne
        elif ins == 7:
            d[p3] = int(d[p1] < d[p2])  # lt
        elif ins == 8:
            d[p3] = int(d[p1] == d[p2])  # eq
        else:
            raise ValueError(f"Unknown instruction {ins} at {ptr}")
        ptr += ins_size[ins]  # move ptr
    return out[-1]
