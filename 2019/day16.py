import numpy as np
import pytest

@pytest.mark.notest
def test_16(data: str, level):
    data = np.array(list(data) * 10000, dtype=int)
    offset = int("".join([str(i) for i in data[:7]])) % len(data)
    for _ in range(100):
        data = data[::-1].cumsum()[::-1] % 10  # calculate cumsum from back to front
    # this works because newdata[-1] = data[-1]; data[-2] = data[-2]+newdata[-1]
    # because repeat(0,1,0,-1) for high i produces a diagonal matrix
    return "".join(data[offset:offset + 8].astype(str))  # take 8 at offset as str
