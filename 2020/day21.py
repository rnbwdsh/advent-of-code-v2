import itertools
from collections import Counter

import networkx as nx

from level_annotations import level_ab

@level_ab(21)
def solve(data, method=0):
    g = nx.Graph()
    all_ing_ctr = Counter()
    for line in data:
        ing, alle = line.split(" (contains ")
        ing = set(ing.split(" "))
        alle = set(alle[:-1].split(", "))
        all_ing_ctr.update(ing)
        for a, i in itertools.product(alle, ing):
            if g.has_edge(a, i):  # the solution isn't unique so we have to use this trick
                g.get_edge_data(a, i)["weight"] -= 1
            else:
                g.add_edge(a, i, weight=0)

    all_ing = set(all_ing_ctr)
    match = nx.bipartite.minimum_weight_full_matching(g)
    unsafe = set(match)  # dict, mapping unsafe ingredients AND compounds
    if method:
        return ",".join((sorted(all_ing & unsafe, key=lambda ing: match[ing])))
    else:
        return sum([all_ing_ctr[s] for s in all_ing - unsafe])
