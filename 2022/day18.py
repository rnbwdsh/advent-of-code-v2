import networkx as nx
import numpy as np

def test_18(data, level):
    voxels = [tuple(int(x) + 1 for x in side.split(",")) for side in data]  # + 1 for left padding
    max_xyz = np.array(voxels, dtype=int).max(axis=0, initial=0) + 2  # +2 for right padding
    gu = nx.grid_graph(dim=tuple(max_xyz)[::-1])  # reverse because axes are flipped, directed version
    gd = gu.to_directed()  # create directed copy
    gu = gu.subgraph(set(gu) - set(voxels))  # remove centers from undirected graph, for inside-finding
    inside = set(gu) - set(nx.descendants(gu, (0, 0, 0)))  # not reachable from 0,0,0 == inside center
    # a face (directed edge) exists if source is in center and target is outside (outside center + inside if level b)
    return len({(src, dst) for src in voxels for dst in gd[src] if dst not in voxels and not (level and dst in inside)})
