import re
from typing import List

from more_itertools import pairwise

P_PAR = r"\([ \d+*]+\)"  # parenthesis regex
P_ADD = r"\d+ \+ \d+"  # addition regex

def sub_problem(line, level):
    while sub := re.search(P_PAR, line):
        line = line.replace(sub.group(), sub_problem(sub.group()[1:-1], level))
    if level:  # do add after brackets if method
        while (sub := re.search(P_ADD, line)) and sub.group() != line:
            line = line.replace(sub.group(), sub_problem(sub.group(), level))
    spl = line.split(" ")
    acc = int(spl[0])
    for op, num in pairwise(spl[1:]):  # offset from 0th element, in 2-steps
        if op == "+":
            acc += int(num)
        elif op == "*":
            acc *= int(num)
    return str(acc)

def test_18(data: List[str], level):  # run with 6 iterations by default
    return sum([int(sub_problem(line, level)) for line in data])
