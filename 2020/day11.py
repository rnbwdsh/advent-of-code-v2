import numpy as np

from level_annotations import level_ab

FLOOR, EMPTY, OCCUPIED = [0, 1, 2]
DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

def neighbors(dc, i, j, dist):
    im, jm = dc.shape
    cnt = 0
    for ip, jp in DIRECTIONS:
        for d in range(1, dist):
            ipos, jpos = i + ip * d, j + jp * d
            if 0 <= ipos < im and 0 <= jpos < jm:
                if (dcp := dc[ipos][jpos]) == EMPTY:
                    break
                elif dcp == OCCUPIED:
                    cnt += 1;
                    break
            else:
                break
    return cnt

def solve10(data, method):
    im, jm = data.shape
    dc = np.zeros_like(data, dtype=data.dtype)
    while not (dc == data).all():
        dc, data = data, dc  # swap without extra allocations
        for i in range(im):
            for j in range(jm):
                if (curr := dc[i][j]) != FLOOR:
                    neigh = neighbors(dc, i, j, 11 if method else 2)
                    if curr == OCCUPIED and neigh >= 4 + method:
                        curr = EMPTY
                    elif curr == EMPTY and not neigh:
                        curr = OCCUPIED
                    data[i][j] = curr
    print((dc == OCCUPIED).sum())
    return (dc == OCCUPIED).sum()

@level_ab(11)
def solve(data, level):  # numba can't optimize parsing, so we'll do it non-jitted
    data = np.array([[".L#".index(line[i]) for i in range(len(line))] for line in data])
    return solve10(data, level)
