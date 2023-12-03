#!/usr/bin/env python
# coding: utf-8

# In[2]:


import copy
from collections import defaultdict
from typing import *

import numpy as np

def fieldWithUnits(field, fighters):
    fieldw = copy.deepcopy(field)
    for f in fighters:
        if f.hp > 0:
            fieldw[f.pos] = f.kind
    return fieldw

def fightersWithPosition(fighters, pos):
    for fighter in fighters:
        if fighter.pos == pos:
            return fighter

def neighbourFields(pos):
    pos = np.array(pos)
    neigh = [pos + [-1, 0], pos + [0, -1], pos + [0, 1], pos + [1, 0]]
    return [tuple(f) for f in neigh]

def freeNeighbourFields(pos, field):
    positions = neighbourFields(pos)
    positions = list(filter(lambda p: field[p] == ".", positions))
    # print([field[p] for p in positions])
    return positions

def printfield(field):
    print("\n".join(["".join(line) for line in field]))
    print()

# recursively backtrace
def backtrace(pos, prev, path=[]):
    if pos in prev:
        return backtrace(prev[pos], prev, [prev[pos]] + path)
    else:
        return path

def backtraceToField(pos, field, targetPos):
    visited = set(pos)
    queue = freeNeighbourFields(pos, field)
    prev = {q: pos for q in queue}
    while queue:
        pos = queue.pop(0)
        # print(pos)
        if pos == targetPos:
            return backtrace(pos, prev) + [pos]
        if pos not in visited:
            visited.add(pos)
            neighbours = freeNeighbourFields(pos, field)
            for nf in (set(neighbours) - visited):
                queue.append(nf)
                prev[nf] = pos  # add backward-path
    return None

class Fighter:
    hp = 200
    damage = 3
    fighting = False

    def __init__(self, pos: Tuple[float], kind: str):
        assert (kind == "E" or kind == "G")
        self.pos = tuple(pos)
        self.kind = kind
        self.enemy = "G" if self.kind == "E" else "E"

    def neighbourFields(self):
        return neighbourFields(self.pos)

    def freeNeighbourFields(self, field: np.ndarray):
        return freeNeighbourFields(self.pos, field)

    def moveAndFight(self, field, fighters):
        # dead people can't fight
        if self.hp < 0:
            return

        # first try to fight if enemy in range
        enemies = filter(lambda nf: field[nf] == self.enemy, self.neighbourFields())
        enemies = list(map(lambda enemy: fightersWithPosition(fighters, enemy), enemies))
        if len(enemies) > 0:
            enemy = list(sorted(enemies, key=lambda e: e.hp))[0]
            enemy.hp -= self.damage
            return

        # print("looking for enemies", self)
        enemies = filter(lambda f: f.kind != self.kind, fighters)
        targetPos = []
        for e in enemies:
            targetPos += e.freeNeighbourFields(field)

        if len(targetPos) == 0:
            # print("no target positions found")
            return

        # find the closest "nearest" adjecent position
        distances = defaultdict(list)
        for t in targetPos:
            backtrace = self.backtraceToField(field, t)
            if backtrace != None:
                distances[len(backtrace)].append(backtrace)
            # else:
            #    print("no backtrace")
        if len(distances) == 0:
            print("no target positions reachable")
            return
        shortest = distances[min(distances)]  # get all the minimal distant fields
        # print("shortest",shortest)
        backtrace = sorted(shortest)[0]  # as we have y-first, then x, default py sorting works for us

        backtraces = []
        for fn in self.freeNeighbourFields(field):
            bt =

        if backtrace != None:
            self.pos = backtrace[1]

        # attack after moving too
        enemies = filter(lambda nf: field[nf] == self.enemy, self.neighbourFields())
        enemies = list(map(lambda enemy: fightersWithPosition(fighters, enemy), enemies))
        if len(enemies) > 0:
            enemy = list(sorted(enemies, key=lambda e: e.hp))[0]
            enemy.hp -= self.damage
            return

    def backtraceToField(self, field, targetPos):
        return backtraceToField(self.pos, field, targetPos)

    # string representation for printing
    def __repr__(self):
        return "%s: x: %d y: %d HP: %d\n" % (self.kind, self.pos[1], self.pos[0], self.hp)

    # for sorting the fighers
    def __lt__(self, other):
        if self.pos[0] == other.pos[0]:
            return self.pos[1] < other.pos[1]
        else:
            return self.pos[0] < other.pos[0]

a = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""

field = np.array([np.array(list(aa)) for aa in a.split("\n")])
print("initial field:")
printfield(field)

# extract fighters from field
fighters = []
for pos in np.argwhere(np.logical_or(field == "E", field == "G")):
    pos = tuple(pos)
    fighters.append(Fighter(pos, field[pos]))
    field[pos] = "."  # clean field
print("Fighters:")
print(sorted(fighters))

print("cleaned up field")
printfield(field)
print()

# main game loop:
cnt = 0
# while len(set(map(lambda f: f.kind, fighters))) > 1:
for j in range(3):
    for f in sorted(fighters):
        fwu = fieldWithUnits(field, fighters)
        f.moveAndFight(fwu, fighters)
        fighters = list(filter(lambda f: f.hp > 0, fighters))
    print("After", cnt, "round:")
    printfield(fieldWithUnits(field, fighters))
    # print(sorted(fighters))
    cnt += 1
cnt -= 1  # the last round "hasn't ended"
hp = list(map(lambda f: f.hp, filter(lambda f: f.hp > 0, fighters)))
print("Rounds", cnt, "Hp", sum(hp), "Score", cnt * sum(hp))

# toolow:  205410 = 82 * 2505
# nearly:  212708 / 210986 / 202905 / 202905
# correct: 207542 = 82 * 2531
# toohigh: 207915 = 83 * 2505
# toohigh: 212925 = 85 * 2505
