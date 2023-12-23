import networkx as nx
import numpy as np
import pytest
from tqdm import tqdm

import point

LOOKUP = {">": point.R, "<": point.L, "^": point.U, "v": point.D}

@pytest.mark.data("""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""", 94, 154)
def test_22(data: np.ndarray, level):
    start = (0, list(data[0]).index("."))
    target = (data.shape[0] - 1, list(data[-1]).index("."))
    g = nx.grid_graph(data.T.shape)
    if not level:
        g = nx.DiGraph(g)
    nx.set_edge_attributes(g, 1, "weight")
    for p, v in np.ndenumerate(data):
        if v == "#":
            g.remove_node(p)
        if v in LOOKUP and not level:
            opp = point.OPPOSITE[LOOKUP[v]]
            target_forbidden = opp + p
            g.remove_edge(p, target_forbidden)
    if level:
        prune_graph(g, start, target)
    return max(nx.path_weight(g, p, weight="weight") for p in tqdm(nx.all_simple_paths(g, start, target)))

def prune_graph(g, start, target):  # all dead ends and all points with exactly two neighbors
    cont = True
    while cont:
        cont = False
        for n in g.nodes:
            neigh = list(g.neighbors(n))
            if len(neigh) == 2:
                g.add_edge(*neigh, weight=sum(g.get_edge_data(a, n)["weight"] for a in neigh))
                g.remove_node(n)
                cont = True
                break
            if len(neigh) == 1 and n != start and n != target:
                g.remove_node(n)
                cont = True
                break
            if len(neigh) == 0:
                g.remove_node(n)