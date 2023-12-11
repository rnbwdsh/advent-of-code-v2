import pytest

def check_num(n: int, level: int):
    n_str = str(n)
    if sorted(n_str) != list(n_str):
        return False
    doubles = {i for i in range(10) if str(i) * 2 in n_str}
    if level:
        doubles -= {i for i in doubles if str(i) * 3 in n_str}
    return bool(doubles)

@pytest.mark.notest
def test_04(data: str, level):
    return sum([check_num(n, level) for n in range(*map(int, data.split("-")))])
