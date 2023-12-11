from typing import List

import networkx as nx

from computer import Computer

MOVEMENT = {1: 1, 2: -1, 3: 1j, 4: -1j}

def test_15(data: List[int], level):
    g = nx.Graph()
    todo = [(Computer(data), 0, [0])]
    oxygen = steps_total = 0  # to avoid uninitialized variable warnings
    while todo:
        p, steps, pos = todo.pop()
        for m in MOVEMENT:
            npos = pos[-1] + MOVEMENT[m]
            if npos not in pos:
                pc = Computer(p.d, ptr=p.ptr)
                status = pc.compute([m])[0]
                if status != 0: g.add_edge(pos[-1], npos)
                if status == 1:
                    todo += [[pc, steps + 1, [*pos, npos]]]
                elif status == 2:
                    steps_total = steps + 1
                    oxygen = npos
    return (steps_total, list(nx.single_target_shortest_path_length(g, oxygen))[-1][1])[level]
