from typing import List

import networkx as nx

def test_06(data: List[str], level):
    data = [d.split(")") for d in data]
    g = nx.Graph(data) if level else nx.DiGraph(data)
    if level:
        return nx.shortest_path_length(g, source='YOU', target='SAN') - 2  # don't count first and last
    return sum([len(nx.descendants(g, n)) for n in g.nodes])
