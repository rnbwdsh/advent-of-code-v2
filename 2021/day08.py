def to_num(d, k, v):
    if len(v) == 5:
        if d[7] < v:
            return 3
        elif d[4] - d[7] < v:
            return 5
        else:
            return 2
    elif len(v) == 6:
        if d[4] < v:
            return 9
        elif d[1] < v:
            return 0
        else:
            return 6
    else:
        return k

def test_08(data: str, level):
    total = 0
    len2num = {2: 1, 3: 7, 4: 4, 7: 8}
    data = data.replace("|\n", "| ")  # testdata is ill-formatted
    for line in data.split("\n"):
        inp, out = (part.split(" ") for part in line.split(" | "))
        d = {len2num.get(len(k), k): frozenset(k) for k in set(inp + out)}  # mapping: digit to set
        set2num = {v: to_num(d, k, v) for k, v in d.items()}
        total += int("".join(str(set2num[frozenset(letter)]) for letter in out)) if level else \
            len([s for s in out if len(s) in len2num.keys()])  # digits 1, 4, 7, 8
    return total
