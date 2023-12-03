from typing import Tuple, Any

import networkx as nx
import numpy as np

dir_lookup = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

def coord_in_arr(coord: Tuple[int, int], arr: np.ndarray) -> bool:
    return all(0 <= pos < dim_len for pos, dim_len in zip(coord, arr.shape))

def pos_of_value(arr: np.ndarray, value: Any):
    return next(zip(*np.where(arr == value)))

def test_12(data, level):
    f = np.array([[ord(c) for c in line] for line in data])
    start = pos_of_value(f, ord("S"))
    end = pos_of_value(f, ord("E"))
    f[start], f[end] = ord('a'), ord('z')

    g = nx.DiGraph()
    for pos, curr in np.ndenumerate(f):
        for x, y in dir_lookup.values():
            e = pos[0] + x, pos[1] + y
            if coord_in_arr(e, f) and curr <= f[e] + 1:
                g.add_edge(e, pos)
    if level:
        apos = zip(*np.where(f == ord('a')))
        return min(nx.shortest_path_length(g, start, end) for start in apos if nx.has_path(g, start, end))
    else:
        return nx.shortest_path_length(g, start, end)
