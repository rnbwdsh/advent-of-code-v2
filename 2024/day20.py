import networkx
import numba
import numpy as np
import pytest

DIR = ((1, 0), (0, -1), (-1, 0), (0, 1))


@pytest.mark.data("""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""", 44, 285)
def test_20(data: np.array, level):
    max_allowed = 20 if level else 2
    shortcut_1 = (50 if level else 1)
    min_shortcut =  shortcut_1 if len(data) == 15 else 100

    g = networkx.DiGraph()
    for x, y in zip(*np.nonzero(data != '#')):
        x, y = int(x), int(y)
        if data[x, y] == 'S':
            e_pos = (x, y)
        for dx, dy in DIR:
            nx, ny = x + dx, y + dy
            if 0 <= nx < data.shape[0] and 0 <= ny < data.shape[1] and data[nx, ny] != '#':
                g.add_edge((x, y), (nx, ny))
    dist2node = sorted(networkx.shortest_path_length(g, target=e_pos).items(), key=lambda x: x[1])
    dist2node = [k for k, v in dist2node]
    return find_shortcuts(dist2node, max_allowed, min_shortcut)


@numba.njit
def find_shortcuts(dist2node, max_dist, min_shortcut):
    hamming_dist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
    shortcuts = 0
    for end in range(len(dist2node)):
        for start in range(end - max_dist):
            dist = hamming_dist(dist2node[start], dist2node[end])
            if dist <= max_dist and end - start - dist >= min_shortcut:
                shortcuts += 1
    return shortcuts
