from itertools import product
from typing import Tuple

import networkx as nx
import numpy as np
import pytest

from util import add_pos, in_bounds, DIR, OPPOSITE

@pytest.mark.data("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""", 102, 94)
def test_17(data: np.ndarray, level):
    data = data.astype(int)
    target = data.shape[0] - 1, data.shape[1] - 1
    return shortest_path(data, (0, 0), target, level)

def shortest_path(data: np.ndarray, start: Tuple[int, int], target: Tuple[int, int], level: int) -> int:
    depth_max = 10 if level else 3
    depth_min = 3 if level else 0
    g = nx.DiGraph()

    for dir in DIR:  # add start and end nodes
        g.add_edge("start", (start, dir, 0), weight=0)
        for r in range(depth_min, depth_max):
            g.add_edge((target, dir, r), "end", weight=0)

    for pos_a in np.ndindex(data.shape):
        for dir_a, dir_b in product(DIR, repeat=2):
            pos_b = add_pos(pos_a, dir_b)
            if not in_bounds(pos_b, data) or dir_b == OPPOSITE[dir_a]:
                continue  # going oob or back is not allowed
            for r in range(0 if dir_a == dir_b else depth_min, depth_max):
                g.add_edge((pos_a, dir_a, r), (pos_b, dir_b, r+1 if dir_a == dir_b else 0), weight=data[*pos_b])
    return nx.shortest_path_length(g, "start", "end", weight="weight")
