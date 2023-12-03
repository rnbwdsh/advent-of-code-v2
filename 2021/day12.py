import networkx as nx

def all_paths(g, curr, visited, all_visited, can_twice=True):
    visited += tuple([curr])
    if curr == "end":
        all_visited.addd(visited)
        return
    for n in nx.neighbors(g, curr):
        if n.isupper() or n not in visited:
            all_paths(g, n, visited, all_visited, can_twice)
        elif can_twice and n != "start":
            all_paths(g, n, visited, all_visited, False)
    return all_visited

def test_12(data, level):
    g = nx.Graph([line.split("-") for line in data])
    res = all_paths(g, "start", tuple(), set(), can_twice=level)
    return len(res)
