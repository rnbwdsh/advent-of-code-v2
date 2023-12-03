from string import ascii_uppercase as tp

import aocd
import networkx as nx
import numpy as np

def create(data: str) -> nx.Graph:
    d = np.array(list(map(list, data.split("\n"))))
    g = nx.Graph()
    portals = {}
    for spos, src in np.ndenumerate(d):
        for p in [[1, 0], [0, 1]]:
            dpos = tuple(np.array(spos) + p)
            if dpos[0] in range(d.shape[0]) and dpos[1] in range(d.shape[1]):
                dest = d[dpos]
                if src not in "# " and dest not in "# ":
                    if src in tp and dest in tp:
                        name = src + dest
                        g.add_edge(spos, dpos, weight=0)
                        g.nodes[spos]["name"] = name
                        if name in portals:
                            g.add_edge(spos, portals[name], teleport=True)
                        else:
                            portals[name] = spos
                    else:
                        entering_tp = src in tp or dest in tp
                        g.add_edge(spos, dpos, weight=not entering_tp)

                    g.nodes[spos]["typ"] = "tp" if src in tp else src

    return g

def portal(g, name):
    return min([pos for pos, posname in nx.get_node_attributes(g, "name").items() if name == posname])

def expand(g, height, width, rec_dep=2):
    inner = []
    outer = []
    for node in nx.get_node_attributes(g, "name"):
        if 2 < node[0] < width - 2 and 2 < node[1] < height - 2:
            inner.append(node)
        else:
            outer.append(node)
    print("inner/outer", len(inner), len(outer))

    g.remove_edges_from(nx.get_edge_attributes(g, "teleport"))
    gc = nx.Graph()
    for i in range(rec_dep):
        for n1 in nx.get_node_attributes(g, "name"):
            for n2 in nx.get_node_attributes(g, "name"):
                if n1 != n2 and nx.has_path(g, n1, n2) and n1 < n2:
                    startnode = "AA" not in [g.nodes[n1]["name"], g.nodes[n2]["name"]]
                    l = nx.shortest_path_length(g, n1, n2, weight="weight") + startnode
                    # print(g.nodes[n1]["name"], g.nodes[n2]["name"], l)
                    if n1 in outer and n2 in outer or n1 in inner and n2 in inner:
                        gc.add_edge(g.nodes[n1]["name"] + str(i), g.nodes[n2]["name"] + str(i), weight=l)
                    elif n1 in outer and n2 in inner:
                        gc.add_edge(g.nodes[n1]["name"] + str(i), g.nodes[n2]["name"] + str(i + 1), weight=l)
                    else:
                        gc.add_edge(g.nodes[n1]["name"] + str(i + 1), g.nodes[n2]["name"] + str(i), weight=l)

    return gc

def solve(data, start="AA", end="ZZ", exp=0, dbg=False):
    g = create(data)
    if exp:
        g = expand(g, len(data.split("\n")[0]), len(data.split("\n")), exp)
    if dbg:
        print(*g.edges, sep="\n")

    if exp:
        start, end = "AA0", "ZZ0"
    else:
        start, end = portal(g, start), portal(g, end)

    if dbg:
        for node in nx.shortest_path(g, start, end, weight="weight"):
            print(node)

    return nx.shortest_path_length(g, start, end, weight="weight")

aocd.submit(solve(aocd.get_data(day=20)), day=20)

aocd.submit(solve(aocd.get_data(day=20), exp=50), day=20)

assert solve("""         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """) == 23

assert solve("""                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """) == 58

assert solve("""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """, exp=20) == 396
