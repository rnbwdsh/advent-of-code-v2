def test_02(data, level):
    data = [line.split(" ") for line in data]
    total = 0
    for a, b in data:
        a, b = ord(a) - ord('A'), ord(b) - ord('X')
        total += b * 3 + (a + b - 1) % 3 + 1 if level else ((b - a + 1) % 3) * 3 + b + 1
    return total
