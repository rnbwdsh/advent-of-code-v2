#!/usr/bin/env python
# coding: utf-8

# In[35]:


import numpy as np
from scipy.cluster.hierarchy import fclusterdata
from scipy.spatial.distance import cityblock as manhattan

a = """ 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""
"""-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""
a = open("day25.txt").read().strip()
pointgroups = [np.array(list(map(int, aa.split(",")))) for aa in a.split("\n")]
# print(pointgroups)
clu = fclusterdata(pointgroups, t=3.0, criterion='distance', metric=manhattan)
print("Number of clusters", max(clu))
