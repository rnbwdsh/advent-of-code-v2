#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools
import re
from collections import defaultdict, Counter

import numpy as np

o = 400
grid = np.zeros((o, o), dtype=int)
d = defaultdict(list)
a = """305, 349
315, 193
154, 62
246, 310
145, 283
260, 324
342, 79
321, 353
40, 242
351, 353
337, 297
174, 194
251, 160
314, 195
114, 81
204, 246
203, 169
203, 296
60, 276
201, 47
206, 96
243, 46
295, 304
319, 80
213, 330
337, 255
40, 262
302, 150
147, 349
317, 240
96, 315
133, 305
320, 348
210, 300
266, 216
223, 319
207, 152
127, 214
312, 245
49, 329
211, 84
129, 276
247, 143
208, 235
271, 126
124, 211
144, 184
54, 88
354, 300
148, 85"""
b = a.strip().split("\n")
c = [[int(x) for x in re.findall("(\d+), (\d+)", bb)[0]] for bb in b]

# manhattan distance
def distance(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])

# for each field, calculate the distance
for i in itertools.product(range(o), range(o)):
    dist = defaultdict(list)
    for index, line in enumerate(c):
        x = line[0]
        y = line[1]
        dist[distance((x, y), i)].append(index)
    best = dist[min(dist)]
    if len(best) > 1:
        grid[i] = -1
    else:
        grid[i] = best[0]

found = Counter(grid.flatten())

# sort out all the cornering ones
for i in range(o):
    if grid[i, 0] in found:
        found.pop(grid[i, 0])
    if grid[i, o - 1] in found:
        found.pop(grid[i, o - 1])
    if grid[0, i] in found:
        found.pop(grid[0, i])
    if grid[o - 1, i] in found:
        found.pop(grid[o - 1, i])

print(grid)
max(found.values())

# In[2]:


grid = np.zeros((o, o), dtype=int)

for i in itertools.product(range(o), range(o)):
    s = 0
    for line in c:
        x = line[0]
        y = line[1]
        s += distance((x, y), i)
    if s < 10000:
        grid[i] = -2

Counter(grid.flatten())[-2]
