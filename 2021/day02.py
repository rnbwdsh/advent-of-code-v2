import numpy as np

def test_02(data, level):
    dirs = {"forward": 1j, "up": 1, "down": -1}
    pos = aim = 0
    for line in data:
        dire, dist = line.split()
        dire, dist = dirs[dire], int(dist)
        if level:
            if dire.real:
                aim += dist * dire
            else:
                pos += dist + dist * aim * dire
        else:
            pos += dire * dist
    return np.absolute([pos.real, pos.imag]).prod(dtype=int)
