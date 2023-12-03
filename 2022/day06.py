def test_06(data: str, level):
    offset = 4 + level * 10
    for i in range(len(data) - offset):
        if len(set(data[i:i + offset])) == offset:
            return i + offset
