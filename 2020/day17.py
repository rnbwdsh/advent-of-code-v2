import numpy as np
from scipy.signal import convolve

from level_annotations import level_ab

@level_ab(17)
def solve(data, method=0, it=6):  # run with 6 iterations by default
    field = np.array([[list(line) for line in data]]) == "#"
    if method: field = np.expand_dims(field, 0)
    is_alive = np.vectorize(lambda x: x in [3, 1002, 1003])
    conv_filt = np.ones((3,) * (method + 3), dtype=int)
    conv_filt[(1,) * (method + 3)] = 1000  # set center 0
    for _ in range(it):
        field = is_alive(convolve(field.astype(int), conv_filt, "full"))
    return field.sum()
