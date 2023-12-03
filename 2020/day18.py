import re

from more_itertools import pairwise

from level_annotations import level_ab

P_PAR = r"\([ \d+*]+\)"  # parenthesis regex
P_ADD = r"\d+ \+ \d+"  # addition regex

def subproblem(line, method):
    while (sub := re.search(P_PAR, line)):
        line = line.replace(sub.group(), subproblem(sub.group()[1:-1], method))
    if method:  # do add after brackets if method
        while (sub := re.search(P_ADD, line)) and sub.group() != line:
            line = line.replace(sub.group(), subproblem(sub.group(), method))
    spl = line.split(" ")
    acc = int(spl[0])
    for op, num in pairwise(spl[1:]):  # offset from 0th element, in 2-steps
        if op == "+":
            acc += int(num)
        elif op == "*":
            acc *= int(num)
    return str(acc)

@level_ab(18)
def solve(data, method=0):  # run with 6 iterations by default
    return sum([int(subproblem(line, method)) for line in data.split("\n")])
