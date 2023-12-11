from computer import Computer

def test_05(data: str, level):
    data = [int(d) for d in data.replace("\n", "").split(",")]  # don't modify original, return modified copy
    if level:
        return Computer(data).compute([5])[-1]
    return Computer(data).compute([1])[-1]
