import networkx as nx
import numpy as np
import pytest

from point import U, D, L, R, Point, PointList

CONN = {"S": (U, D, L, R), "|": (U, D), "-": (L, R), "L": (R, U), "J": (L, U), "7": (L, D), "F": (R, D)}

@pytest.mark.data(("""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""", """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""), 8, 4)
def test_10(data: np.ndarray, level):
    start = Point(tuple(np.argwhere(data == "S")[0]))
    g = nx.DiGraph([(Point(src), Point(src) + d)
                    for src, val in np.ndenumerate(data)
                    for d in CONN.get(val, ())])
    g = g.to_undirected(reciprocal=True)  # remove all non-reciprocal edges
    if level:
        return PointList([u for u, _ in nx.find_cycle(g, start)]).area
    return max(nx.single_source_shortest_path_length(g, start).values())
