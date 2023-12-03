def test_25(data, level_a):
    total = 0
    lookup = "012=-"
    for s in data:
        subtotal = 0  # for each number, left to right, convert
        for c in s:
            subtotal = subtotal * 5 + (lookup.index(c) + 2) % 5 - 2
        total += subtotal

    res = ""  # convert back, lsb to msb, convert
    while total:
        res = lookup[r := total % 5] + res
        total = total // 5 + (1 if r > 2 else 0)  # if =-, add 1 to next digit
    return res
