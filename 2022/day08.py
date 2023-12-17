import numpy as np

def test_08(data, level):
    f = np.array([[int(c) for c in line] for line in data])
    vis, score = np.zeros_like(f), np.ones_like(f, dtype=int)
    for _ in range(4):  # repeat with 4 rotations
        inner(f, level, score, vis)
        f, vis, score = np.rot90(f), np.rot90(vis), np.rot90(score)
    return score.max() if level else vis.sum()

def inner(f, level, score, vis):
    for (i, j), val in np.ndenumerate(f):
        if level:  # walk down 1, 2, 3... steps
            for d in range(0, len(f) - j):
                if d == 0:
                    continue
                if f[i, j + d] >= f[i, j]:
                    break
            score[i, j] *= d  # noqa
        else:
            if j == 0 or max(f[i, :j]) < f[i, j]:
                vis[i, j] = True