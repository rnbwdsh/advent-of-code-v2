import re
from typing import List

import numpy as np

PATTERN = r"""Monkey (\d+):
 +Starting items: (\d+(?:, \d+)*)
 +Operation: new = old (.) (.+)
 +Test: divisible by (\d+)
 +If true: throw to monkey (\d+)
 +If false: throw to monkey (\d+)"""

class Monkey:
    def __init__(self, chunk: str):
        self.residue = 0  # equivalence class for numbers
        self.cnt = 0
        self.next_items = []

        self.id, self.items, self.op, self.num, self.divisor, self.if_true, self.if_false = re.match(PATTERN, chunk).groups()  # noqa spaces in regex
        self.id, self.divisor, self.if_true, self.if_false = int(self.id), int(self.divisor), int(self.if_true), int(
            self.if_false)
        self.items = [int(i) for i in self.items.split(", ")]

        if self.num == "old":
            self.op = lambda x: x ** 2
        else:
            self.num = int(self.num)
            if "*" in self.op:
                self.op = lambda x: x * self.num
            elif "+" in self.op:
                self.op = lambda x: x + self.num

    def process(self, monkeys):
        self.cnt += len(self.items)
        for i in self.items:
            i = self.op(i)
            if self.residue:
                i = i % self.residue
            else:
                i //= 3
            target = self.if_true if i % self.divisor == 0 else self.if_false
            monkeys[target].items.append(i)
        self.items = []

def test_11(data: List[List[str]], level):
    monkeys = [Monkey("\n".join(chunk)) for chunk in data]
    if level:
        divisors = np.lcm.reduce([m.divisor for m in monkeys])  # noqa
        for m in monkeys:
            m.residue = divisors
    for _ in range(10000 if level else 20):
        for m in monkeys:
            m.process(monkeys)
    return np.prod(sorted([m.cnt for m in monkeys])[-2:])
