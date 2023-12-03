import networkx as nx

from level_annotations import level_ab

def all_paths(g, curr, visited, all_visited, can_twice=True):
    visited += tuple([curr])
    if curr == "end":
        all_visited.add(visited)
        return
    for n in nx.neighbors(g, curr):
        if n.isupper() or n not in visited:
            all_paths(g, n, visited, all_visited, can_twice)
        elif can_twice and n != "start":
            all_paths(g, n, visited, all_visited, False)
    return all_visited

@level_ab(12)
def test(lines, level):
    g = nx.Graph([line.split("-") for line in lines])
    res = all_paths(g, "start", tuple(), set(), can_twice=level)
    return len(res)
