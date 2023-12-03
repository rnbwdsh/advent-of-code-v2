import numpy as np

from level_annotations import level_a

@level_a(25, sep="\n")
def test(lines, level):
    d = np.array([list(line) for line in lines])
    w, h = d.shape

    for t in range(1, 1000):
        move_east = [(i, j) for (i, j), c in np.ndenumerate(d) if c == ">" and d[i, (j + 1) % h] == "."]
        for i, j in move_east:
            d[i, j] = "."
            d[i, (j + 1) % h] = ">"

        move_south = [(i, j) for (i, j), c in np.ndenumerate(d) if c == "v" and d[(i + 1) % w, j] == "."]
        for i, j in move_south:
            d[i, j] = "."
            d[(i + 1) % w, j] = "v"

        if not move_south and not move_east:
            return t
