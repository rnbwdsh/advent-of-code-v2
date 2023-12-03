from collections import defaultdict

import networkx as nx
import numpy as np

from level_annotations import level_ab

@level_ab(16, sep="\n\n")
def solve(data, method=0):
    allow, your, other = data  # parsing
    your = [int(x) for x in your.split("\n")[1].split(",")]
    other = np.array([[int(x)
                       for x in o.split(",")]
                      for o in other.split("\n")[1:]])

    allowed = defaultdict(set)  # build a name: allowed set
    for line in allow.split("\n"):
        name, options = line.split(": ")
        for option in options.split(" or "):
            start, end = [int(x) for x in option.split("-")]
            allowed[name].update(range(int(start), int(end) + 1))
    all_allowed = set.union(*allowed.values())

    if method:  # throw away invalid lines first
        other = np.array([line for line in other if all_allowed.issuperset(set(line))])
        g = nx.Graph()  # build name: colid graph, do bipartite matching for assignment problem
        for colid, col in enumerate(other.T):
            for name, nallowed in allowed.items():
                if nallowed.issuperset(col):
                    g.add_edge(name, colid)
        matches = nx.algorithms.bipartite.matching.minimum_weight_full_matching(g).items()
        return np.prod([your[colid] for name, colid in matches
                        if type(name) == str and name.startswith("departure")], dtype=int)
    return sum(filter(lambda o: o not in all_allowed, other.flat))  # else not needed
