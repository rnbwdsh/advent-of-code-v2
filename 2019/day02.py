import aocd

data = [int(d) for d in aocd.get_data(day=2).split(",")]
print(data)

def process(d):
    d = d[:]
    for ptr in range(0, len(d), 4):
        # print(d[ptr:ptr+4]) # debug
        if d[ptr] == 1:
            d[d[ptr + 3]] = d[d[ptr + 1]] + d[d[ptr + 2]]
        elif d[ptr] == 2:
            d[d[ptr + 3]] = d[d[ptr + 1]] * d[d[ptr + 2]]
        elif d[ptr] == 99:
            return d
        else:
            print(f"invalid opcode {d[ptr]} @ {ptr}")

assert process([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
assert process([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]

data[1:3] = 12, 2
out = process(data)

aocd.submit(day=2, answer=out[0])

for i in range(100):
    for j in range(100):
        d[1:3] = i, j
        out = process(d)
        if out[0] == 19690720:
            aocd.submit(day=2, answer=i * 100 + j)
