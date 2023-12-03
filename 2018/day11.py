#!/usr/bin/env python
# coding: utf-8

# In[6]:


import itertools

import numpy as np

serial = 4151

w = 300
a = np.zeros((w, w))
for x, y in itertools.product(range(w), range(w)):
    cid = x + 1 + 10
    a[x, y] = (abs((cid * (y + 1) + serial) * cid) // 100) % 10 - 5

# retry for sizes
print("max\tx\ty\tsize")
for size in range(30):
    b = np.zeros((w - size, w - size))
    w2 = w - size
    for x, y in itertools.product(range(w2), range(w2)):
        b[x, y] = int(np.sum(a[x:x + size + 1, y:y + size + 1]))

    m = np.max(b)
    f = list(b.flatten())
    fi = f.index(m)
    print(int(m), fi // w2 + 1, fi % w2 + 1, size + 1, sep="\t")
