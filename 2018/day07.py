import re
from collections import defaultdict

a = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
aa = """Step A must be finished before step L can begin.
Step B must be finished before step U can begin.
Step S must be finished before step K can begin.
Step L must be finished before step R can begin.
Step C must be finished before step I can begin.
Step F must be finished before step N can begin.
Step X must be finished before step H can begin.
Step Z must be finished before step U can begin.
Step P must be finished before step T can begin.
Step R must be finished before step U can begin.
Step H must be finished before step T can begin.
Step V must be finished before step G can begin.
Step E must be finished before step D can begin.
Step G must be finished before step W can begin.
Step N must be finished before step J can begin.
Step U must be finished before step D can begin.
Step Y must be finished before step K can begin.
Step K must be finished before step J can begin.
Step D must be finished before step M can begin.
Step I must be finished before step O can begin.
Step M must be finished before step Q can begin.
Step Q must be finished before step J can begin.
Step T must be finished before step J can begin.
Step W must be finished before step O can begin.
Step J must be finished before step O can begin.
Step C must be finished before step F can begin.
Step C must be finished before step J can begin.
Step Z must be finished before step I can begin.
Step K must be finished before step I can begin.
Step L must be finished before step W can begin.
Step I must be finished before step W can begin.
Step N must be finished before step O can begin.
Step B must be finished before step G can begin.
Step S must be finished before step O can begin.
Step P must be finished before step H can begin.
Step R must be finished before step J can begin.
Step N must be finished before step U can begin.
Step U must be finished before step J can begin.
Step E must be finished before step T can begin.
Step T must be finished before step O can begin.
Step L must be finished before step T can begin.
Step P must be finished before step Y can begin.
Step L must be finished before step C can begin.
Step D must be finished before step O can begin.
Step H must be finished before step Y can begin.
Step Q must be finished before step T can begin.
Step P must be finished before step G can begin.
Step G must be finished before step D can begin.
Step F must be finished before step H can begin.
Step G must be finished before step M can begin.
Step F must be finished before step V can begin.
Step X must be finished before step O can begin.
Step V must be finished before step Y can begin.
Step Y must be finished before step D can begin.
Step H must be finished before step G can begin.
Step A must be finished before step S can begin.
Step E must be finished before step U can begin.
Step Y must be finished before step O can begin.
Step C must be finished before step K can begin.
Step R must be finished before step W can begin.
Step G must be finished before step I can begin.
Step V must be finished before step E can begin.
Step V must be finished before step T can begin.
Step E must be finished before step K can begin.
Step X must be finished before step R can begin.
Step Q must be finished before step W can begin.
Step X must be finished before step P can begin.
Step K must be finished before step T can begin.
Step I must be finished before step T can begin.
Step P must be finished before step R can begin.
Step T must be finished before step W can begin.
Step X must be finished before step I can begin.
Step N must be finished before step Q can begin.
Step G must be finished before step Y can begin.
Step Y must be finished before step W can begin.
Step L must be finished before step D can begin.
Step F must be finished before step D can begin.
Step A must be finished before step T can begin.
Step R must be finished before step H can begin.
Step E must be finished before step I can begin.
Step W must be finished before step J can begin.
Step F must be finished before step M can begin.
Step V must be finished before step W can begin.
Step I must be finished before step J can begin.
Step Z must be finished before step P can begin.
Step H must be finished before step U can begin.
Step R must be finished before step V can begin.
Step V must be finished before step M can begin.
Step Y must be finished before step M can begin.
Step P must be finished before step M can begin.
Step K must be finished before step D can begin.
Step C must be finished before step T can begin.
Step Y must be finished before step T can begin.
Step U must be finished before step I can begin.
Step A must be finished before step O can begin.
Step E must be finished before step J can begin.
Step H must be finished before step V can begin.
Step F must be finished before step W can begin.
Step M must be finished before step T can begin.
Step S must be finished before step H can begin.
Step S must be finished before step G can begin."""

b = aa.strip().split("\n")
c = [re.findall("Step (\w) must be finished before step (\w) can begin", bb)[0] for bb in b]

print(c)

graph = defaultdict(list)
letters = set()
for line in c:
    graph[line[1]] += (line[0])
    letters.add(line[0])
    letters.add(line[1])

print(graph)
print()
print("Solution")

while len(letters) > 0:
    for x in sorted(list(letters)):
        if len(graph[x]) == 0:
            letters.remove(x)
            for k, v in graph.items():
                if x in v:
                    v.remove(x)
            print(x, end="")
            break
print()

graph = defaultdict(list)
free_time = defaultdict(list)
letters = set()
number_working = 0
max_working = 5
time = 0

for line in c:
    graph[line[1]] += (line[0])
    letters.add(line[0])
    letters.add(line[1])

print(graph)
print()
print("Solution")

# 1157
def time_for_letter(x):
    return ord(x) - 4
    # return ord(x)-64

while len(letters) > 0 or free_time:
    if time in free_time:
        for x in free_time[time]:
            # remove dependencies for letter once it's done
            for k, v in graph.items():
                if x in v:
                    v.remove(x)
            print("done working at", time, "on", x)
            free_time[time].remove(x)
            number_working -= 1
        del free_time[time]

    for x in sorted(list(letters)):
        if len(graph[x]) == 0 and number_working < max_working:
            number_working += 1
            letters.remove(x)
            # print(x,end="")
            print("started working at", time, "for", time_for_letter(x), "on", x)
            free_time[time + time_for_letter(x)] += x

    time += 1
print(time - 1)
