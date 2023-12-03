from copy import copy

import aocd

OUT = []
data = [int(d) for d in aocd.get_data(day=5).split(",")]

INS_SIZE = {1: 4, 2: 4, 3: 2, 4: 2, 5: 0, 6: 0, 7: 4, 8: 4, 99: 0}

def process(d, inp=[], out=OUT, ptr=0, debug=False):
    d = copy(d)  # don't modify original, return modified copy
    parse = lambda i: [i % 100] + [i // 10 ** e % 10 for e in range(2, 5)]
    while ptr < len(d):  # stop on EOF
        ins, p1m, p2m, p3m = parse(d[ptr])  # parse cmd
        if ins != 99:  # don't overread
            p1 = ptr + 1 if p1m else d[ptr + 1]
            p2 = ptr + 2 if p2m else d[ptr + 2]
            p3 = ptr + 3 if p3m else d[ptr + 3]
        if debug:    print(ptr, d[ptr:ptr + 4])  # debug
        if ins == 1:
            d[p3] = d[p1] + d[p2]  # add
        elif ins == 2:
            d[p3] = d[p1] * d[p2]  # mul
        elif ins == 3:
            d[p1] = inp[0]  # read
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
        elif ins == 99:
            return d  # ret
        else:
            print(f"invalid opcode {ins} @ {ptr}")  # err
        ptr += INS_SIZE[ins]  # move ptr

assert process([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
assert process([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
assert process([1002, 4, 3, 4, 33]) == [1002, 4, 3, 4, 99]

process(data, [1])
aocd.submit(day=5, answer=OUT[-1])  # manually picked

process(data, [5])
aocd.submit(day=5, answer=OUT[-1])
