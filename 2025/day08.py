from typing import List

import networkx as nx
import pytest
from numpy.ma.core import product

from point import Point


@pytest.mark.data('''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689''', 40, 25272)
def test_08(data: List[str], level):
    g = nx.Graph()
    g.add_nodes_from(Point(tuple(map(int, line.split(",")))) for line in data)
    conn = [(n1.dist(n2), n1, n2) for i, n1 in enumerate(g) for j, n2 in enumerate(g) if i < j]
    conn = sorted(conn, key=lambda x: x[0])
    if not level:
        conn = conn[:(10 if len(g) == 20 else 1000)]
    for dist, n1, n2 in conn:
        g.add_edge(n1, n2)
        if level and nx.is_connected(g):
            return n1[0] * n2[0]

    # product of the 3 largest component sizes
    components = sorted(nx.connected_components(g), key=len, reverse=True)
    return product([len(c) for c in components[:3]])
