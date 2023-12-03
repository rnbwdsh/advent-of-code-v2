#!/usr/bin/env python
# coding: utf-8

# In[88]:


import networkx as nx
import numpy as np

ROCK, WET, NARROW = 0, 1, 2
NEITHER, TORCH, CLIMB = 0, 1, 2

# In[90]:


depth = 3558
target = (15, 740)

# exsample numbers
# depth = 510
# target = (10,10)

t = tuple((target[0] * 2, target[1] * 2))

field = np.zeros(t, dtype=int)
erosionLevels = np.zeros(t, dtype=int)

# initialize
for x in range(t[0]):
    for y in range(t[1]):
        if x == 0 and y == 0 \
                or x == target[0] and y == target[1]:
            geoIndex = 0
        if y == 0:
            geoIndex = x * 16807
        elif x == 0:
            geoIndex = y * 48271
        else:
            geoIndex = erosionLevels[x - 1, y] * erosionLevels[x, y - 1]
        erosionLevel = (geoIndex + depth) % 20183
        typ = erosionLevel % 3
        erosionLevels[x, y] = erosionLevel
        field[x, y] = typ
        # if x < 2 and y < 2:
        #    print(x, y, "geoindex", geoIndex, "erosion", erosionLevel, "type", typ)

# The region at 0,0 (the mouth of the cave) has a geologic index of 0.
# The region at the coordinates of the target has a geologic index of 0.
field[0, 0] = 0
field[target] = 0

np.sum(field[:target[0] + 1, :target[1] + 1])

# In[97]:


g = nx.Graph()

def compatible(styp, dtyp, tool):
    # In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
    # In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
    # In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).
    if tool == NEITHER and ROCK in [dtyp, styp] \
            or tool == TORCH and WET in [dtyp, styp] \
            or tool == CLIMB and NARROW in [dtyp, styp]:
        return False
    else:
        return True

# test compatiblity
assert (not compatible(WET, ROCK, TORCH))
assert (compatible(ROCK, NARROW, TORCH))

# bidirectional graph, so we only need down + right transitions
# and tool a->b transtitions, and we get left + up and b-> a for free
for x in range(t[0]):
    for y in range(t[1]):
        # add tool transitions (bidirectional)
        g.add_edge((x, y, 0), (x, y, 1), weight=7)
        g.add_edge((x, y, 1), (x, y, 2), weight=7)
        g.add_edge((x, y, 2), (x, y, 0), weight=7)

        for xdir, ydir in [(0, 1), (1, 0)]:
            for tool in range(3):
                xtar, ytar = x + xdir, y + ydir
                if xtar < t[0] and ytar < t[1]:
                    styp, dtyp = field[(x, y)], field[(xtar, ytar)]
                    if compatible(styp, dtyp, tool):
                        srcField = (x, y, tool)
                        targetField = (xtar, ytar, tool)
                        g.add_edge(srcField, targetField, weight=1)

sfield = (0, 0, TORCH)
tfield = (target[0], target[1], TORCH)
shortest = nx.shortest_path_length(g, sfield, tfield, weight="weight")
print("shortest path length is", shortest)
