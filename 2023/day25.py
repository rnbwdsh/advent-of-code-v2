from typing import List

import networkx as nx
import pytest


@pytest.mark.data("""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""", 54, None)
def test_25(data: List[str], level_a):
    g = nx.Graph()
    for line in data:
        left, right = line.split(": ")
        for right in right.split(" "):
            g.add_edge(left, right)
    cc = list(nx.connected_components(g))
    return len(cc[0]) * len(cc[1])
