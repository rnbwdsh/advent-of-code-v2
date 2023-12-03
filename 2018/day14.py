#!/usr/bin/env python
# coding: utf-8

# In[44]:


def solve(until, full=False):
    r = [3, 7]
    p1 = 0
    p2 = 1
    while len(r) < (until + 12):
        new_score = r[p1] + r[p2]
        for score in list(str(new_score)):
            r.append(int(score))
        # print("moved forward", r[p1] + 1, r[p2] + 1)
        p1 = (p1 + r[p1] + 1) % (len(r))
        p2 = (p2 + r[p2] + 1) % (len(r))
        # print(p1,p2,"\t",r)
    if not full:
        return "".join(str(i) for i in r[until:until + 10])
    else:
        return "".join(str(i) for i in r)

print(solve(9))
print(solve(5))
print(solve(18))
print(solve(2018))
print(solve(327901))

# In[51]:


def solve2(subsequence, toSearch=10000):
    seq = solve(toSearch, True)
    return seq.index(str(subsequence))

print(solve2(51589))
print(solve2("01245"))
print(solve2("327901", 100000000))
