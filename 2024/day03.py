import numpy as np
import pytest
import re

@pytest.mark.data(("""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""), 161, 48)
def test_03(data: str, level):
    enabled = np.array([True] * len(data))
    if level:
        for m in re.finditer(r"(do|don't)\(\)", data):
            enabled[m.start():] = m.group(1) == "do"
    return sum([int(m.group(1)) * int(m.group(2))
                for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", data)
                if enabled[m.start()]])
