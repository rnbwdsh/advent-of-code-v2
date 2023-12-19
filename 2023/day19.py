import operator
from dataclasses import dataclass
from typing import List, Dict

import pytest
from numpy import prod

@pytest.mark.data("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""", 19114, 167409079868000)
def test_19(data: List[str], level):
    workflows, items = data
    wf = {name: [Rule(p) for p in rest.split(",")] for name, rest in (w.split("{") for w in workflows.split("\n"))}
    if level:
        return work_b(PartRange({k: range(1, 4001) for k in "xmas"}, "in", 0), wf)
    else:
        items = [dict(part.split("=") for part in line[1:-1].split(",")) for line in items.split("\n")]
        return sum(work_a(item, wf) for item in items)

class Rule:
    def __init__(self, line: str):
        if ":" in line:
            (self.var, self.op, *val), self.target = line.split(":")
            self.op = operator.lt if self.op == "<" else operator.gt
            self.val = int("".join(val))
            self.check_val = lambda v: self.target if self.op(int(v), self.val) else None
            self.check = lambda p: self.check_val(p[self.var])
        else:
            self.var = None
            self.target = line[:-1]
            self.check = lambda _: self.target

@dataclass
class PartRange:
    val: Dict[str, range]
    rule: str
    step: int

    def score(self):
        return prod([len(self.val[i]) for i in "xmas"]) if self.rule == "A" else 0

    def split(self, check: Rule) -> List["PartRange"]:
        if check.var is None:
            return [PartRange(self.val, check.target, 0)]

        # check start and stop values
        cond_start = check.check_val(self.val[check.var].start)
        cond_stop = check.check_val(self.val[check.var].stop - 1)

        # if both match, go to next rule
        if cond_start and cond_stop:
            return [PartRange(self.val, check.target, 0)]
        # if none match, go to next step
        elif not cond_start and not cond_stop:
            return [PartRange(self.val, self.rule, self.step + 1)]

        # the border of left/right is shifted by 1 in case of lt
        cutoff = check.val if check.op == operator.lt else check.val + 1
        # the check.var: statement overwrites the one field in the copied self.val dict
        v0 = {**self.val, check.var: range(self.val[check.var].start, cutoff)}
        v1 = {**self.val, check.var: range(cutoff, self.val[check.var].stop)}
        # if the case only matches for the stop-value, swap the two
        if cond_stop:
            v0, v1 = v1, v0
        return [PartRange(v0, check.target, 0), PartRange(v1, self.rule, self.step + 1)]

def work_b(part: PartRange, workflow: Dict[str, List[Rule]]):
    if part.rule in "RA":
        return part.score()
    rule = workflow[part.rule][part.step]
    return sum(work_b(p, workflow) for p in part.split(rule))

def work_a(part: Dict[str, str], workflow: Dict[str, List[Rule]], rule_name="in"):
    if rule_name == "A":
        return sum(map(int, part.values()))
    elif rule_name == "R":
        return 0
    for rule in workflow[rule_name]:
        rule_name = rule.check(part)
        if rule_name is not None:
            return work_a(part, workflow, rule_name)
