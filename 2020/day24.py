from collections import defaultdict

DIR6 = {1 + 1j: "ne", 1 - 1j: "se", -1 + 1j: "nw", -1 - 1j: "sw", 2: "e", -2: "w"}

def parse(s, tok=()):
    if not s: return tok
    for dv, dn in DIR6.items():
        if s.startswith(dn):
            # print(dn, len(dn), s[len(dn)+1:])
            rv = parse(s[len(dn):], (*tok, dv))
            if rv: return rv
    return False

assert sum(parse("nwwswee")) == 0

def test_24(data, level):
    field = defaultdict(bool)
    for line in data:
        pos = sum(parse(line))
        field[pos] = not field[pos]

    if level:  # part 2: game of life in a sparse hex field
        for _ in range(100):
            fc = field.copy()
            for pos, pv in field.items():
                if pv:  # only add white fields to black neighbors
                    for nd in DIR6:
                        fc.update({pos + nd: fc[pos + nd]})
            for pos, pv in fc.items():
                nr_neigh = sum([field[pos + nd] for nd in DIR6])
                if (pv and (nr_neigh == 0 or nr_neigh > 2)) or (not pv and nr_neigh == 2):
                    fc[pos] = not fc[pos]  # flip
            field = fc
    return sum(field.values())  # sum(bool) = count of true
