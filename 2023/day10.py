from typing import List

import networkx as nx
import numpy as np
import pytest
from scipy.ndimage.measurements import label

from parsers import parse_array

L, R, U, D = ((0, -1), (0, 1), (-1, 0), (1, 0))
CONN = {"S": (U, D, L, R), "|": (U, D), "-": (L, R), "L": (R, U), "J": (L, U), "7": (L, D), "F": (R, D)}

@pytest.mark.data(("""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""",
"""..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""), 8, 4)
def test_10(data: List[str], level):
    empty_line = "\n" + " " * (len(data[0]) * 2 - 1) + "\n"  # add empty line between every line
    joined_data = empty_line.join([" ".join(line) for line in data])  # add space between every char
    data = parse_array(joined_data)

    start = tuple(np.argwhere(data == "S")[0])
    g = nx.Graph()
    for (x, y), v in np.ndenumerate(data):  # construct graph
        for dx, dy in CONN.get(v, ()):  # if v not in conn, just don't add anything
            g.add_edge((x, y), (x + dx, y + dy))

    if level:
        g = nx.subgraph(g, nx.node_connected_component(g, start))  # retain only start-reachable
        img = np.ones_like(data, dtype=int)  # convert graph back to matrix
        for node in g.nodes:
            img[node] = 0
        img = np.pad(img, pad_width=1, constant_values=1)[1:, 1:]
        img[np.equal(label(img)[0], 1)] = 0  # flood fill from 0/0 border
        img = (img[::2, ::2] + img[1::2, ::2] + img[::2, 1::2] + img[1::2, 1::2]) == 4  # sample 50% of the img
        return np.sum(img)
    return max(nx.single_source_shortest_path_length(g, start).values()) // 2
