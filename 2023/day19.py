import operator
from dataclasses import dataclass
from typing import List, Optional, Dict
from numpy import prod

import pytest

OP_LOOKUP = {"<": operator.lt, ">": operator.gt}

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
    wf = {name: [Rule(*p.split(":")) if ":" in p else Rule(None, p) for p in rest.split(",")]
          for name, rest in (w.split("{") for w in workflows.split("\n"))}
    if level:
        return work_b(Parts({k: range(1, 4001) for k in "xmas"}, "in", 0), wf)
    else:
        items = [{name: int(val) for part in line[1:-1].split(",") for name, val in [part.split("=")]}
                 for line in items.split("\n")]
        return sum(work_a(item, wf) for item in items)

def work_b(parts, wf):
    if parts.rule in "RA":
        return parts.score()
    check = wf[parts.rule][parts.step]
    return sum(work_b(p, wf) for p in parts.split(check))

def work_a(item, workflow, rule="in"):
    if rule == "A":
        return sum(item.values())
    elif rule == "R":
        return 0
    for check in workflow[rule]:
        rule = check.perform_check(item)
        if rule is not None:
            return work_a(item, workflow, rule)

class Rule:
    def __init__(self, var_to_check_op: Optional[str], target: str):
        self.target = target.replace("}", "")
        self.var = None
        if var_to_check_op:
            self.var, self.op, *val = var_to_check_op
            self.op = OP_LOOKUP[var_to_check_op[1]]
            self.val = int("".join(val))

    def perform_check(self, i: Dict[str, int]) -> Optional[str]:
        if self.var is None:
            return self.target
        return self.perform_check_val(i[self.var])

    def perform_check_val(self, val: int) -> Optional[str]:
        if self.op(val, self.val):
            return self.target

@dataclass
class Parts:
    val: Dict[str, range]
    rule: str
    step: int

    def score(self):
        return prod([len(self.val[i]) for i in "xmas"]) if self.rule == "A" else 0

    def split(self, check: Rule) -> List["Parts"]:
        if check.var is None:
            return [Parts(self.val, check.target, 0)]

        # check start and stop values
        cond_start = check.perform_check_val(self.val[check.var].start)
        cond_stop = check.perform_check_val(self.val[check.var].stop - 1)

        # if both match, go to next rule
        if cond_start and cond_stop:
            return [Parts(self.val, check.target, 0)]
        # if none match, go to next step
        elif not cond_start and not cond_stop:
            return [Parts(self.val, self.rule, self.step + 1)]

        # the border of left/right is shifted by 1 in case of lt
        cutoff = check.val if check.op == operator.lt else check.val + 1
        # the check.var: statement overwrites the one field in the copied self.val dict
        v0 = {**self.val, check.var: range(self.val[check.var].start, cutoff)}
        v1 = {**self.val, check.var: range(cutoff, self.val[check.var].stop)}
        # if the case only matches for the stop-value, swap the two
        if cond_stop:
            v0, v1 = v1, v0
        return [Parts(v0, check.target, 0), Parts(v1, self.rule, self.step + 1)]
