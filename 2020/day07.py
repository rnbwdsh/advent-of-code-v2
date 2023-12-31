import re
from typing import List

import networkx as nx

def test_07(data: List[str], level):
    g = nx.DiGraph()
    for line in data:
        line = re.sub("(bags?)", "", line)
        containing, contained = line[:-2].split("  contain ")
        if "no other" not in contained:
            for contain in contained.split(" , "):
                c = contain.split(" ")
                cnt = int(c[0]) if len(c) == 3 else 1
                contain = " ".join(c[-2:])
                g.add_edge(containing, contain, cnt=cnt)
    if level:
        return dfs(g, "shiny gold", 1)
    else:
        return len(nx.algorithms.dag.ancestors(g, "shiny gold"))

def dfs(g: nx.Graph, start: str, factor: int):
    return sum([dfs(g, follower, factor * val["cnt"]) + factor * val["cnt"]
                for follower, val in g[start].items()])
