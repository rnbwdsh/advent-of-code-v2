from string import ascii_uppercase as tp

import networkx as nx
import numpy as np

def create(data: str) -> nx.Graph:
    d = np.array(list(map(list, data.split("\n"))))
    g = nx.Graph()
    portals = {}
    for spos, src in np.ndenumerate(d):
        for p in [[1, 0], [0, 1]]:
            pos_d = tuple(np.array(spos) + p)
            if pos_d[0] in range(d.shape[0]) and pos_d[1] in range(d.shape[1]):
                dest = d[pos_d]
                if src not in "# " and dest not in "# ":
                    if src in tp and dest in tp:
                        name = src + dest
                        g.add_edge(spos, pos_d, weight=0)
                        g.nodes[spos]["name"] = name
                        if name in portals:
                            g.add_edge(spos, portals[name], teleport=True)
                        else:
                            portals[name] = spos
                    else:
                        entering_tp = src in tp or dest in tp
                        g.add_edge(spos, pos_d, weight=not entering_tp)
                    g.nodes[spos]["typ"] = "tp" if src in tp else src
    return g

def portal(g, name):
    return min([pos for pos, posname in nx.get_node_attributes(g, "name").items() if name == posname])

def expand(g, height, width, rec_dep):
    inner = []
    outer = []
    for node in nx.get_node_attributes(g, "name"):
        if 2 < node[0] < width - 2 and 2 < node[1] < height - 2:
            inner.append(node)
        else:
            outer.append(node)

    g.remove_edges_from(nx.get_edge_attributes(g, "teleport"))
    gc = nx.Graph()
    for i in range(rec_dep):
        for n1 in nx.get_node_attributes(g, "name"):
            for n2 in nx.get_node_attributes(g, "name"):
                if n1 != n2 and nx.has_path(g, n1, n2) and n1 < n2:
                    n_start = "AA" not in [g.nodes[n1]["name"], g.nodes[n2]["name"]]
                    l = nx.shortest_path_length(g, n1, n2, weight="weight") + n_start

                    if n1 in outer and n2 in outer or n1 in inner and n2 in inner:
                        gc.add_edge(g.nodes[n1]["name"] + str(i), g.nodes[n2]["name"] + str(i), weight=l)
                    elif n1 in outer and n2 in inner:
                        gc.add_edge(g.nodes[n1]["name"] + str(i), g.nodes[n2]["name"] + str(i + 1), weight=l)
                    else:
                        gc.add_edge(g.nodes[n1]["name"] + str(i + 1), g.nodes[n2]["name"] + str(i), weight=l)

    return gc

def test_20(data: str, level):
    g = create(data)
    if level:
        g = expand(g, len(data.split("\n")[0]), len(data.split("\n")), 50)
        start, end = "AA0", "ZZ0"
    else:
        start, end = portal(g, "AA"), portal(g, "ZZ")
    return nx.shortest_path_length(g, start, end, weight="weight")
