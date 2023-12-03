# In[11]:


import functools

import aocd
import matplotlib.pyplot as plt
import numpy as np

data = np.array([int(d) for d in list(aocd.get_data(day=8))]).reshape((-1, 6, 25))

# In[12]:


def compute(data):
    layer = min(data, key=lambda layer: (layer == 0).sum())
    return (layer == 1).sum() * (layer == 2).sum()

assert compute(np.array([int(i) for i in "123456789012"]).reshape(-1, 2, 3)) == 1
aocd.submit(day=8, answer=compute(data))

# In[13]:


draw = lambda img: functools.reduce(lambda a, b: np.where(a != 2, a, b), img)

tmp = np.array([int(i) for i in "0222112222120000"]).reshape(-1, 2, 2)
assert np.array_equal(draw(tmp), np.array([[0, 1], [1, 0]]))
plt.imshow(draw(data))
aocd.submit("ZLBJF", day=8)
