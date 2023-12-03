import re

import networkx as nx

from level_annotations import level_ab

@level_ab(7)
def solve(data, level):
    def dfs(G, start, factor):
        return sum([dfs(G, follower, factor * val["cnt"]) + factor * val["cnt"]
                    for follower, val in G[start].items()])

    G = nx.DiGraph()
    for line in data.split("\n"):
        line = re.sub("(bags?)", "", line)
        containing, contained = line[:-2].split("  contain ")
        if "no other" not in contained:
            for contain in contained.split(" , "):
                cspl = contain.split(" ")
                cnt = int(cspl[0]) if len(cspl) == 3 else 1
                contain = " ".join(cspl[-2:])
                G.add_edge(containing, contain, cnt=cnt)
    if level:
        return dfs(G, "shiny gold", 1)
    else:
        return len(nx.algorithms.dag.ancestors(G, "shiny gold"))
