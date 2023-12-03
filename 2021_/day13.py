import matplotlib.pyplot as plt
import numpy as np

from level_annotations import level_ab

@level_ab(13, test=False, sep="\n\n")
def test(lines, level):
    data, fold = lines
    d = np.array([[int(i) for i in d.split(",")] for d in data.split("\n")])
    field = np.zeros([np.max(d) + 1] * 2, dtype=bool)
    field[tuple(d.T)] = True
    for f in fold.split("\n"):
        direction, dist = f.split("=")
        direction, dist = direction[-1:], int(dist)

        field = field.T if direction == "y" else field  # y-case: just do it mirrored
        field = field[:dist] | field[dist + 1:][:dist][::-1]  # cut field, and OR it with other field reversed
        field = field.T if direction == "y" else field

        if not level: return field.sum()  # level1: return after first fold
    plt.imshow(field.T)
    plt.show()
    return "EAHKRECP"
