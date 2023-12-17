import itertools
import re
from functools import partial
from multiprocessing import Pool
from typing import Dict

import networkx as nx
import numpy as np

def test_16(data, level):
    # create base graph
    g = nx.DiGraph()
    node_flow = {}
    for line in data:
        src, rate, targets = \
            re.findall(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)", line)[0]
        for dst in targets.split(", "):
            g.add_edge(src, dst, weight=1)
        if int(rate) > 0 or src == "AA":
            node_flow[src] = int(rate)

    # trim graph to only contain nodes with flow
    fwg = nx.floyd_warshall(g, weight="weight")
    g = nx.from_edgelist(
        [(src, dst, {'weight': fwg[src][dst]}) for src, dst in itertools.product(node_flow, node_flow) if
         fwg[src][dst]], nx.DiGraph)

    # walk graph
    states = [State(pos="AA", visited={"AA"}, length=26 if level else 30, score=0)]
    i = 0
    while len(states) > i:
        i += len(ns := states[i:])
        for followup in Pool().map(partial(followup_states, g=g, node_flow=node_flow), ns):
            states.extend(followup)
    for state in states:  # create bitmap
        state.visited = sum(1 << i for i, v in enumerate(node_flow) if v in state.visited and v != "AA")
    states = sorted(states, key=lambda s: s.score, reverse=True)

    if level:
        scores = np.array(
            [[s.score for s in states]])  # speeds up computation, by trimming before quadratic computation
        vis = np.array([[s.visited for s in states]])
        mask = ~(vis.T & vis).astype(bool)  # not overlapping
        return (scores.T + scores)[mask].max()
    else:
        return max([s.score for s in states])

class State:
    def __init__(self, pos, visited, length, score):
        self.pos = pos
        self.visited = visited
        self.length = length
        self.score = score

def followup_states(s: State, g: nx.DiGraph, node_flow: Dict):
    states = []
    for n in g.neighbors(s.pos):
        new_len = s.length - g[s.pos][n]["weight"] - 1
        if n not in s.visited and new_len > 0:
            states.append(State(pos=n, visited=s.visited | {n}, length=new_len, score=s.score + node_flow[n] * new_len))
    return states