import functools

import matplotlib.pyplot as plt
import numpy as np
import pytest

@pytest.mark.notest
def test_08(data: str, level):
    data = np.array([int(d) for d in list(data)]).reshape((-1, 6, 25))
    if level:
        plt.imshow(functools.reduce(lambda a, b: np.where(a != 2, a, b), data))
        return "ZLBJF"
    layer = min(data, key=lambda l: (l == 0).sum())
    return (layer == 1).sum() * (layer == 2).sum()
