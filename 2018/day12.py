#!/usr/bin/env python
# coding: utf-8

# In[29]:


a = """...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""
"""#.#.# => #
.##.. => .
#.#.. => .
..### => #
.#..# => #
..#.. => .
####. => #
###.. => #
#.... => .
.#.#. => #
....# => .
#...# => #
..#.# => #
#..#. => #
.#... => #
##..# => .
##... => .
#..## => .
.#.## => #
.##.# => .
#.##. => #
.#### => .
.###. => .
..##. => .
##.#. => .
...## => #
...#. => .
..... => .
##.## => .
###.# => #
##### => #
#.### => ."""
startState = "#..#.#..##......###...###"
# startState = "##.###.......#..#.##..#####...#...#######....##.##.##.##..#.#.##########...##.##..##.##...####..####"
b = a.split("\n")
c = [bb.split(" => ") for bb in b]
d = {cc[0]: cc[1] for cc in c}

prefix = 20
state = "." * prefix + startState + "." * prefix
total = 0
totalWidth = 0

for i in range(20):
    hc = state.count("#")
    lc = state.index("#") - prefix
    rc = state.rfind("#") - prefix

    total += hc
    totalWidth += lc + rc
    state = ".." + state + ".."

    print(i, "\t", state, "\t", state.count("#"), "\t", lc, "\t", rc)
    nstate = ""
    for i in range(len(state) - 4):
        try:
            substr = state[i:i + 5]
            nstate += d[substr]
        except KeyError:
            nstate += "."
    state = nstate
print(20, "\t", state, "\t", state.count("#"), "\t", lc, "\t", rc)
print("Total number of #:", total)
print("Sum of lc+rc:", totalWidth)
potScore = 0
for i in range(len(state)):
    if state[i] == "#":
        potScore += i - prefix
print("Pot score", potScore)

# In[133]:


from IPython.core.display import display, HTML

display(HTML("<style>.container { width:100% !important; }</style>"))

a = """#.#.# => #
.##.. => .
#.#.. => .
..### => #
.#..# => #
..#.. => .
####. => #
###.. => #
#.... => .
.#.#. => #
....# => .
#...# => #
..#.# => #
#..#. => #
.#... => #
##..# => .
##... => .
#..## => .
.#.## => #
.##.# => .
#.##. => #
.#### => .
.###. => .
..##. => .
##.#. => .
...## => #
...#. => .
..... => .
##.## => .
###.# => #
##### => #
#.### => ."""
# a =
"""...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

startState = "##.###.......#..#.##..#####...#...#######....##.##.##.##..#.#.##########...##.##..##.##...####..####"
# startState = "#..#.#..##......###...###"
b = a.split("\n")
c = [bb.split(" => ") for bb in b]
d = {cc[0]: cc[1] for cc in c}

prefix = 1200
state = "." * prefix + startState + "." * prefix

def score(state):
    potScore = 0
    for j in range(len(state)):
        if state[j] == "#":
            potScore += j - prefix - 2
    return potScore

for i in range(1010):
    state = ".." + state + ".."
    nstate = ""
    for j in range(len(state) - 4):
        try:
            substr = state[j:j + 5]
            nstate += d[substr]
        except KeyError:
            nstate += "."
    print("iteration", i, "score", score(state), "diff", score(state) - score(nstate))
    state = nstate
potScore = 0

# In[135]:


547 + 23 * 50000000000

# In[ ]:
