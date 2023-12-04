from collections import defaultdict
from typing import List

import networkx as nx
import numpy as np

def test_16(data: List[List[str]], level):
    allow, your, other = data  # parsing
    your = [int(x) for x in your[1].split(",")]
    other = np.array([[int(x)
                       for x in o.split(",")]
                      for o in other[1:]])

    allowed = defaultdict(set)  # build a name: allowed set
    for line in allow:
        name, options = line.split(": ")
        for option in options.split(" or "):
            start, end = [int(x) for x in option.split("-")]
            allowed[name].update(range(int(start), int(end) + 1))
    all_allowed = set.union(*allowed.values())

    if level:  # throw away invalid lines first
        other = np.array([line for line in other if all_allowed.issuperset(set(line))])
        g = nx.Graph()  # build name: colid graph, do bipartite matching for assignment problem
        for col_id, col in enumerate(other.T):
            for name, n_allowed in allowed.items():
                if n_allowed.issuperset(col):
                    g.add_edge(name, col_id)
        matches = nx.algorithms.bipartite.matching.minimum_weight_full_matching(g).items()
        return np.prod([your[col_id] for name, col_id in matches
                        if isinstance(name, str) and name.startswith("departure")], dtype=int)  # noqa typing
    return sum(filter(lambda o: o not in all_allowed, other.flat))  # else not needed
