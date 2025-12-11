from functools import cache
from typing import List

import networkx as nx
import pytest


def count_paths_passing_through(g: nx.DiGraph, source: str, target: str, via: frozenset) -> int:
    @cache
    def dfs(node: str, r: frozenset) -> int:
        if node == target:
            return 1 if not r else 0
        return sum(dfs(n, r - {n} if n in r else r) for n in g.neighbors(node))

    return dfs(source, via)

@pytest.mark.data(('''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out''', '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out'''), 5, 2)
def test_11(data: List[str], level):
    g = nx.DiGraph()
    for line in data:
        name, parts = line.split(": ")
        g.add_edges_from((name, part) for part in parts.split())
    if not level:
        return count_paths_passing_through(g, source="you", target="out", via=frozenset())
    return count_paths_passing_through(g, source="svr", target="out", via=frozenset(["dac", "fft"]))