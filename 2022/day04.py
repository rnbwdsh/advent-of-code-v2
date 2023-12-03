import re

def test_04(data, level):
    total = 0
    for line in data:
        a, b, c, d = map(int, re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", line)[0])
        left, right = set(range(a, b + 1)), set(range(c, d + 1))
        total += bool(left & right) if level else left.issuperset(right) or right.issuperset(left)
    return total
