from collections import defaultdict

from level_annotations import level_ab

DIR6 = {1 + 1j: "ne", 1 - 1j: "se", -1 + 1j: "nw", -1 - 1j: "sw", 2: "e", -2: "w"}

def parse(s, tok=()):
    if not s: return tok
    for dv, dn in DIR6.items():
        if s.startswith(dn):
            # print(dn, len(dn), s[len(dn)+1:])
            rv = parse(s[len(dn):], (*tok, dv))
            if rv: return rv
    else:
        return False

assert sum(parse("nwwswee")) == 0

@level_ab(24)
def solve(data, method=0):
    field = defaultdict(bool)
    for line in data.split("\n"):
        pos = sum(parse(line))
        field[pos] = not field[pos]

    if method:  # part 2: game of life in a sparse hex field
        for i in range(100):
            fc = field.copy()
            for pos, pv in field.items():
                if pv:  # only add white fields to black neighbors
                    for nd in DIR6:
                        fc[pos + nd] = fc[pos + nd]
            for pos, pv in fc.items():
                nr_neigh = sum([field[pos + nd] for nd in DIR6])
                if (pv and (nr_neigh == 0 or nr_neigh > 2)) or (not pv and nr_neigh == 2):
                    fc[pos] = not fc[pos]  # flip
            field = fc
    return sum(field.values())  # sum(bool) = count of true
