import pytest

@pytest.mark.notest
def test_04(data: str, level):
    return sum(sorted(n_str := str(n)) == list(n_str)
               and any(str(i) * 2 in n_str for i in range(10))
               and (not level or not any(str(i) * 3 in n_str for i in range(10)))
               for n in range(*map(int, data.split("-"))))
