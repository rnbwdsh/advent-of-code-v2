from collections import defaultdict
from string import ascii_lowercase as keys
from string import ascii_uppercase as doors

import aocd
import networkx as nx
import numpy as np

def create(d) -> nx.Graph:
    if type(d) == str:  # support string and numpy input
        d = np.array(list(map(list, d.split("\n"))))
    g = nx.Graph()
    for spos, src in np.ndenumerate(d):
        for p in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            dpos = tuple(np.array(spos) + p)
            if dpos[0] in range(d.shape[0]) and dpos[1] in range(d.shape[1]):
                dest = d[dpos]
                if src != "#" and dest != "#":
                    g.add_edge(spos, dpos, weight=1)
                    if src in keys:
                        g.nodes[spos]["key"] = src
                    elif src in doors:
                        g.nodes[spos]["door"] = src.lower()
                    g.nodes[spos]["typ"] = src

    # trim graph
    for node in g.copy().nodes:
        neigh = list(g.neighbors(node))
        if len(neigh) == 2 and g.nodes[node]["typ"] == ".":
            weight = sum([g.edges[(node, n)]["weight"] for n in neigh])
            g.remove_node(node)
            g.add_edge(*neigh, weight=weight)

    return g

def bfs(data):
    # init data
    g = create(data)
    startpos = [pos for pos, typ in nx.get_node_attributes(g, "typ").items() if typ == "@"][0]
    pos_door = nx.get_node_attributes(g, "door")
    pos_key = nx.get_node_attributes(g, "key")

    # build dict (src) -> (dest, doors_in_way, keys_in_way)
    key_dist = defaultdict(list)
    for p1, k1 in list(pos_key.items()) + [[startpos, "@"]]:
        for p2, k2 in pos_key.items():
            if k1 != k2:
                # calculate shortest path between any points and if any any keys/doors are on the way
                sp = nx.shortest_path(g, p1, p2, weight="weight")
                blocked_by = set(sp) & (set(pos_door))
                blocked_by = set([pos_door[bb] for bb in blocked_by])

                blocking = set(sp) & set(pos_key) - set([p1, p2])
                blocking = set([pos_key[bb] for bb in blocking])

                dist = nx.shortest_path_length(g, p1, p2, weight="weight")
                key_dist[k1].append([k2, dist, blocked_by, blocking])

    # assumption: we can't "walk around doors"
    # and the shortest_path(shortest_path(keys)) is shorter 
    jobs = {(0, "@", frozenset())}
    for _ in range(len(pos_key)):  # iterate bfs for number of keys, as we need that many steps
        jobs = list(set(  # unique
            [(steps + dist, target, keys_hold | set([target]))  # add new dist-target-visited tuples
             for steps, start, keys_hold in jobs  # for all current start-tuples
             for target, dist, blocked_by, blocking in key_dist[start]  # for all target-tuples
             if target not in keys_hold  # if target is not already reached
             and not blocked_by - keys_hold  # not blocked by a door without a key
             and not blocking - keys_hold]))  # and not blocked by a key on the
    return min([j[0] for j in jobs])

assert bfs("""#########
#b.A.@.a#
#########""")

assert bfs("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""") == 81

# part 1
aocd.submit(bfs(aocd.get_data(day=18)), day=18)

get_ipython().run_cell_magic('time', '',
                             '# optimized variant with bitmasks and encoding that\'s 10x faster\ndef encode(a):  # "a" = 2^0, @=2^27\n    if a == "@":       return 0\n    if type(a) == str: return 2**(ord(a)-ord("a"))\n    else:              return sum([encode(aa) for aa in a])\n\ndef bfs(data):\n    # init data\n    g = create(data)\n    startpos = [pos for pos, typ in nx.get_node_attributes(g, "typ").items() if typ=="@"][0]\n    pos_door = nx.get_node_attributes(g, "door")\n    pos_key =  nx.get_node_attributes(g, "key")\n    \n    # needed for part 2: just ignore doors that don\'t have keys in this sub-maze. doesn\'t affect part 1\n    for p, d in list(pos_door.items()):\n        if d not in pos_key.values():\n            pos_door.pop(p)\n    \n    # build dict (src) -> (dest, doors_in_way, keys_in_way)\n    key_dist = defaultdict(list)\n    for p1, k1 in list(pos_key.items())+[[startpos, "@"]]:\n        for p2, k2 in pos_key.items():\n            if k1 != k2:\n                # calculate shortest path between any points and if any any keys/doors are on the way\n                sp = nx.shortest_path(g, p1, p2, weight="weight")\n                blocked_by = set(sp) & (set(pos_door))\n                blocked_by = set([pos_door[bb] for bb in blocked_by])\n                \n                blocking = set(sp) & set(pos_key) - set([p1,p2])\n                blocking = set([pos_key[bb] for bb in blocking])\n                \n                dist = nx.shortest_path_length(g, p1, p2, weight="weight")\n                key_dist[encode(k1)].append([encode(k2), dist, encode(blocked_by), encode(blocking)])\n    \n    # assumption: we can\'t "walk around doors"\n    # and the shortest_path(shortest_path(keys)) is shorter \n    jobs = {(0, encode("@"), 0)}\n    for _ in range(len(pos_key)):  # iterate bfs for number of keys, as we need that many steps\n        jobs = list(set(  # unique, deduplicate for performance\n            [(steps+dist, target, keys_hold|target)            # add new dist-target-visited tuples\n                for steps, start, keys_hold in jobs            # for all current start-tuples\n                    for target, dist, blocked_by, blocking in key_dist[start]  # for all target-tuples\n                        if  not target     &  keys_hold        # if target is not already reached\n                        and not blocked_by & ~keys_hold        # not blocked by a door without a key\n                        and not blocking   & ~keys_hold]))     # and not blocked by a key on the \n    return min([j[0] for j in jobs])\n\nassert bfs("""#########\n#b.A.@.a#\n#########""")\n\nassert bfs("""########################\n#@..............ac.GI.b#\n###d#e#f################\n###A#B#C################\n###g#h#i################\n########################""") == 81\n\n# part 1\naocd.submit(bfs(aocd.get_data(day=18)), day=18)\n')

# part 2 assumption: we can act as if all doors that don't have keys in this maze don't exist
# as we can just use another robot and wait in this maze, as we can only move one at a time anyways
data = aocd.get_data(day=18)
d = np.array(list(map(list, data.split("\n"))))  # parse data
center = np.where(d == "@")[0][0]  # square maze -> only the x-coord is enough
# set the center to @#@ ### @#@
d[center - 1:center + 2, center - 1:center + 2] = np.array([["@", "#", "@"], ["#", "#", "#"], ["@", "#", "@"]])

# create the 4 sub-mazes
d1 = d[:center + 1, :center + 1]
d2 = d[center:, :center + 1]
d3 = d[:center + 1, center:]
d4 = d[center:, center:]

# sum of sub-mazes = sum of steps
res = sum(map(bfs, [d1, d2, d3, d4]))
aocd.submit(res, day=18)
