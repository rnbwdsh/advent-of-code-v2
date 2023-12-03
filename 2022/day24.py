import itertools

import networkx as nx
import numpy as np

SIGN_MOVE = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
MOVES = list(SIGN_MOVE.values()) + [(0, 0)]
MAX_TIME = 900

def test_24(data, level):
    f = np.array([list(li) for li in data])[1:-1, 1:-1]
    w, h = f.shape

    blizzards = [(x, y, *SIGN_MOVE[f[x, y]]) for x, y in zip(*np.where(f != "."))]

    g = nx.DiGraph()
    g.add_nodes_from(itertools.product(range(MAX_TIME), range(w), range(h)))
    g.remove_nodes_from({node for t in range(MAX_TIME)
                         for x, y, xd, yd in blizzards
                         if (node := (t, (x + xd * t) % w, (y + yd * t) % h)) in g})
    g.add_edges_from([((t, x, y), node_next)
                      for t, x, y in g
                      for xd, yd in MOVES
                      if (node_next := (t + 1, x + xd, y + yd)) in g])

    t0 = 0
    p0, p1 = (0, 0), (w - 1, h - 1)
    for start_pos, end_pos in ((p0, p1), (p1, p0), (p0, p1))[:1 + level * 2]:  # level1: to + back + to
        gc = g.copy()
        for t in range(t0, MAX_TIME):
            gc.add_edge(("start", t), ("start", t + 1))  # wait in start
            gc.add_edge(("start", t), (t,) + start_pos)  #
            gc.add_edge((t,) + end_pos, "end")

        t0 += nx.shortest_path_length(gc, source=("start", t0), target="end") - 1
    return t0
