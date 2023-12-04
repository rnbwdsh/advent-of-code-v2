import aocd

parse_line = lambda d: "".join([dd[0] * int(dd[1:]) for dd in d.split(",")])
data = [parse_line(d) for d in aocd.get_data(day=3).split("\n")]
print(data)

lookup = {"R": 1, "L": -1, "U": 1j, "D": -1j}

def trace(data):
    pos = 0
    return {(pos := pos + lookup[d]): time + 1 for time, d in enumerate(data)}

line1, line2 = trace(data[0]), trace(data[1])
intersect = line1.keys() & line2.keys()
dist = [abs(d.real) + abs(d.imag) for d in intersect]
aocd.submit(day=3, answer=int(min(dist)))

intersect_dict = {pos: line1[pos] + line2[pos] for pos in intersect}
aocd.submit(day=3, answer=min(intersect_dict.values()))
