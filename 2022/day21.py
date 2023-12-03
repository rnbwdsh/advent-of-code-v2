from operator import add, sub, mul

import z3

def test_21(data, level):
    s = z3.Solver()
    for line in data:
        a, b = line.split(": ")
        if b.isdigit():
            if not (a == "humn" and level):
                s.add(z3.Int(a) == int(b))
        else:
            b, op, c = b.split(" ")
            if level and a == "root":
                s.add(z3.Int(b) == z3.Int(c))
            else:
                opdict = {"+": add, "-": sub, "*": mul}
                if op == "/":
                    s.add(z3.Int(a) * z3.Int(c) == z3.Int(b))  # division must exactly match up
                else:
                    s.add(z3.Int(a) == opdict[op](z3.Int(b), z3.Int(c)))
    s.check()
    return s.model()[z3.Int("humn" if level else "root")].as_long()
