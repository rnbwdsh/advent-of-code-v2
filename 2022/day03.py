def prio(c: str) -> int:
    return ord(c.lower()) - ord('a') + 1 + c.isupper() * 26

def test_03(data, level):
    total = 0
    if level:
        for i in range(0, len(data) - 1, 3):
            a, b, c = map(set, data[i: i + 3])
            total += prio(next(iter(a & b & c)))
    else:
        for line in data:
            offset = len(line) // 2
            a, b = set(line[:offset]), set(line[offset:])
            total += sum([prio(c) for c in a & b])
    return total
