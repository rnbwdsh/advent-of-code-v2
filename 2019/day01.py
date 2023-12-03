import aocd

data = [int(i) for i in aocd.get_data(day=1).split("\n")]
print(data)

def req_0(mass):
    return mass // 3 - 2

def req(mass: int):
    fl = [req_0(mass)]
    while req_0(fl[-1]) > 0:
        fl.append(req_0(fl[-1]))
    return sum(fl)

assert req(12) == 2
assert req(100756) == 50346

aocd.submit(day=1, answer=sum(map(req_0, data)))
aocd.submit(day=1, answer=sum(map(req, data)))
