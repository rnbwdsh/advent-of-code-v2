from collections import defaultdict
from dataclasses import dataclass
from multiprocessing.dummy import Pool
from typing import List, Dict, Iterable, ClassVar, Sized

import networkx as nx
import numpy as np
import pytest

def bitmask(letters: Iterable[str], lower: bool) -> int:
    base_ord = ord('a') if lower else ord('A')
    return sum(1 << (ord(letter) - base_ord) for letter in letters if letter.islower() == lower)

class Path:
    def __init__(self, path: Sized):
        path_letters = [p for p in path[1:-1] if isinstance(p, str) and p != "@"]
        self.keys = bitmask(path_letters, True)
        self.doors = bitmask(path_letters, False)
        self.distance = len(path) - 1

@dataclass
class Walk:
    start_key: str = "@"
    keys_todo: int = 0
    doors_unlocked: int = 0
    dist: int = 0
    distances_a_b: ClassVar[Dict[str, Path]] = {}

    def advance(self) -> List["Walk"]:
        to_return = []
        for letter_bit_pos in range(self.keys_todo.bit_length()):
            letter_bit = 1 << letter_bit_pos
            if not self.keys_todo & letter_bit:
                continue
            target_key = chr(ord("a") + letter_bit_pos)
            path = Walk.distances_a_b[self.start_key + target_key]
            if not self.keys_todo & letter_bit or path.keys & self.keys_todo or path.doors & ~self.doors_unlocked:
                continue  # redundant path or path blocked
            doors_unlocked = self.doors_unlocked | letter_bit
            new_keys = self.keys_todo & ~letter_bit
            to_return.append(Walk(target_key, new_keys, doors_unlocked, self.dist + path.distance - 1))
        return to_return

def process(data: np.ndarray):
    g = nx.grid_graph(data.T.shape)
    keys_todo = set(k for k in data.flatten() if k.islower())
    for pos, val in np.ndenumerate(data):
        if val == "#":
            g.remove_node(pos)
        elif val != "." and (not val.isupper() or val.lower() in keys_todo):
            # if the door does not have a key, it's open (for case 2)
            nx.relabel_nodes(g, {pos: val}, copy=False)

    # set lookup table to all walks
    Walk.distances_a_b = {(a + b): Path(nx.shortest_path(g, source=a, target=b))
                          for a in set("@") | keys_todo
                          for b in keys_todo if a != b}
    keys_bits = bitmask(keys_todo, True)

    todo = [Walk("@", keys_bits)]
    for _ in range(len(keys_todo)):
        todo_map = defaultdict(list)
        for result in Pool(24).map(Walk.advance, todo):
            for walk in result:
                todo_map[hash((walk.start_key, walk.keys_todo, walk.doors_unlocked))].append(walk)
        todo = [min(walks, key=lambda w: w.dist) for walks in todo_map.values()]
    return min(walk.dist for walk in todo) + 2  # the 2 is start + end

@pytest.mark.notest
def test_18(data: np.ndarray, level):
    if level:
        center = np.nonzero(np.equal(data, "@"))[0][0]
        data[center - 1:center + 2, center - 1:center + 2] = np.array(
            [["@", "#", "@"], ["#", "#", "#"], ["@", "#", "@"]])
        return sum(map(process, [data[:center + 1, :center + 1],
                                 data[center:, :center + 1],
                                 data[:center + 1, center:],
                                 data[center:, center:]]))
    return process(data)
