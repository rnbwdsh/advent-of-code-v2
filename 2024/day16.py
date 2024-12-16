import networkx
import numpy as np
import pytest

DIR = ((1, 0), (0, -1), (-1, 0), (0, 1))

@pytest.mark.data("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""", 7036, 45)
def test_16(data: np.array, level):
    e_pos = list(zip(*np.where(data == 'E')))[0]
    s_pos = list(zip(*np.where(data == 'S')))[0]
    # Starting facing east (index 3 in DIR)
    g = networkx.DiGraph()
    # we start facing to the right
    g.add_edge("START", (s_pos[0], s_pos[1], DIR.index((0, 1))), weight=0)
    # we can end facing any direction
    for fi in range(len(DIR)):
        g.add_edge((e_pos[0], e_pos[1], fi), "END", weight=0)

    for x, y in zip(*np.where(data != '#')):
        for fi, (dx, dy) in enumerate(DIR):
            nx, ny = x + dx, y + dy
            if 0 <= nx < data.shape[0] and 0 <= ny < data.shape[1] and data[nx, ny] != '#':
                g.add_edge((x, y, fi), (nx, ny, fi), weight=1)
            g.add_edge((x, y, fi), (x, y, (fi+1) % 4), weight=1000)
            g.add_edge((x, y, fi), (x, y, (fi-1) % 4), weight=1000)

    spl = networkx.shortest_path_length(g, source="START", target="END", weight='weight')
    if not level:
        return spl
    else:
        dist_start = dict(networkx.shortest_path_length(g, source="START", weight='weight'))
        dist_end = dict(networkx.shortest_path_length(g, target="END", weight='weight'))
        return len({node[:2] for node in g.nodes if (dist_start[node] + dist_end[node]) == spl})-2
