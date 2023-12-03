import networkx as nx
import numpy as np

from level_annotations import level_ab

@level_ab(15)
def test(lines, level):
    data = np.array([[int(i) for i in line] for line in lines])
    if level:
        dx, dy = data.shape
        data = np.tile(data, (5, 5))
        for i, j in np.ndindex(5, 5):
            data[i * dx:i * dx + dx, j * dy:j * dy + dy] += i + j
        data = (data - 1) % 9 + 1  # 10 becomes 1

    g = nx.DiGraph(((a, b), (x, y), {"weight": w})
                   for (x, y), w in np.ndenumerate(data)
                   for a, b in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
                   if a in range(len(data)) and b in range(len(data[0])))
    dx, dy = data.shape
    return nx.dijkstra_path_length(g, (0, 0), (dx - 1, dy - 1))
