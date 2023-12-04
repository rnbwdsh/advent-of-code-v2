def test_05(data: str, level):
    data = data.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")
    data = [int(d, 2) for d in data.split("\n")]
    if level:
        return (set(range(min(data), max(data))) - set(data)).pop()
    else:
        return max(data)
