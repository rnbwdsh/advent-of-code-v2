from typing import List

import pytest

@pytest.mark.data("""TODO""", 1337, 1337)
def test_21(data: List[str], level):
    total = 0
    for line in data:
        total += 1
    return total