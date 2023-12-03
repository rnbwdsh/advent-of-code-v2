import aocd
import networkx as nx

parse = lambda data: [d.split(")") for d in data.split("\n")]
data = parse(aocd.get_data(day=6))
print(data)

def process(data):
    g = nx.DiGraph(data)
    return sum([len(nx.descendants(g, n)) for n in g.nodes])

assert process(parse("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L")) == 42
aocd.submit(day=6, answer=process(data))

def process2(data):
    g = nx.Graph(data)
    return nx.shortest_path_length(g, source='YOU', target='SAN') - 2  # don't count first and last

assert process2(parse('COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN')) == 4
aocd.submit(day=6, answer=process2(data))
