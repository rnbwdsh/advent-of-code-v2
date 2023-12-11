import functools
import itertools
from dataclasses import dataclass
from typing import ClassVar

import networkx as nx
import numpy as np
import pytest
from frozendict import frozendict

# performance of this is really bad :(
ALLOWED_TARGETS = tuple([0, 1, 3, 5, 7, 9, 10])
COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

def build_graph(level):
    g = nx.Graph()
    final = {}
    for i in range(0, 10):
        g.add_edge(i, i + 1)
    for i, letter in zip(range(2, 9, 2), COST):
        final[letter] = tuple(reversed(range(len(g), len(g) + 2 + 2 * level)))
        g.add_edge(i, len(g))
        for i in range(1 + 2 * level):
            g.add_edge(len(g) - 1, len(g))
    GameState.final = frozendict(final)
    GameState.gr = g

@functools.lru_cache(maxsize=10000)
def calc_path(pos, target):
    return frozenset(nx.shortest_path(GameState.gr, pos, target)[1:])

def score(pos):
    res = 0
    for letter, p_ in GameState.final.items():
        for p in p_:
            if p in pos and pos[p] == letter:
                res += 1
            else:
                break
    return res

@dataclass(frozen=True)
class GameState:
    pos: frozendict | dict
    cost: int = 0
    steps: int = 0
    score: int = 0
    final: ClassVar[frozendict] = dict()
    gr: ClassVar[nx.Graph] = nx.Graph()

    def distance(self, start, target):
        if start == target or target in self.pos:
            return None
        path = calc_path(start, target)
        if not path & set(self.pos):
            return len(path)

    def step(self):
        next_states = []
        for start, name in self.pos.items():
            targets = GameState.final[name] + ALLOWED_TARGETS if start in ALLOWED_TARGETS else ALLOWED_TARGETS
            for target in targets:
                dist = self.distance(start, target)
                if dist:
                    new_pos = {**self.pos, target: name}
                    del new_pos[start]
                    new_pos = frozendict(new_pos)
                    g = GameState(pos=new_pos,
                                  cost=self.cost + COST[name] * dist,
                                  steps=self.steps + dist,
                                  score=score(new_pos))
                    if start in ALLOWED_TARGETS and self.score == g.score or g.score < self.score:  # if you move to the final area, you must advance the score
                        continue
                    next_states.append(g)
        return next_states

    def __hash__(self):
        return hash(self.pos)

@pytest.mark.notest
def test_23(data, level_b):
    level = level_b
    if level:
        data = list(data)
        data.insert(2, "  #D#C#B#A#")
        data.insert(3, "  #D#B#A#C#")
    build_graph(level)
    calc_path.cache_clear()

    data = np.array([list("".join(line).replace("#", "").replace(" ", "")) for line in data[2:-1]]).T.flatten()
    pos = dict(zip(range(11, 11 + len(data)), data))
    game = GameState(pos)

    states = [game]
    seen = set()
    for _ in range(100):
        progress = max(g.score for g in states)
        if progress == len(pos):
            # print(min(g.cost for g in states if g.score == len(pos)))
            return min(g.cost for g in states if g.score == len(pos))
        # print(time, progress, len(states))
        states = [game for game in states if game.score >= progress - 1 - level]
        states = [state.step() for state in states]
        states = list(itertools.chain(*states))
        states = set(states).difference(seen)
        seen.update(states)
