import pytest

@pytest.mark.notest
def test_08(data, level):
    total = 0
    len2num = {2: 1, 3: 7, 4: 4, 7: 8}
    for line in data:
        inp, out = (part.split(" ") for part in line.split(" | "))
        d = {len2num.get(len(k), k): frozenset(k) for k in set(inp + out)}  # mapping: digit to set
        set2num = {v: (3 if d[7] < v else 5 if d[4] - d[7] < v else 2) if len(v) == 5 else  # case: len5
        (9 if d[4] < v else 0 if d[1] < v else 6) if len(v) == 6 else k  # case: len6 and others
                   for k, v in d.items()}  # set2digit
        total += int("".join(str(set2num[frozenset(letter)]) for letter in out)) if level else \
            len([s for s in out if len(s) in len2num.keys()])  # digits 1, 4, 7, 8
    return total
