import itertools
import operator
from typing import List, Optional

import pytest

TIMEOUT = 50

@pytest.mark.data('x00: 1\nx01: 1\nx02: 1\ny00: 0\ny01: 1\ny02: 0\n\nx00 AND y00 -> z00\nx01 XOR y01 -> z01\nx02 OR y02 -> z02', 4, None)
def test_24(data: List[List[str]], level):
    init = {name: int(val) for line in data[0] for name, val in [line.split(": ")]}
    tasks = {b: a.split(" ") for line in data[1] for a, b in [line.split(" -> ")]}
    if level:
        best_swaps = []
        for _ in range(4):
            best_swap = None
            best_score = 0
            for a, b in list(itertools.combinations(tasks.keys(), 2)):
                tn = simulate_rep(init, swap_tasks(tasks, a, b))
                if tn is not None and best_score < tn < TIMEOUT:
                    best_score = tn
                    best_swap = (a, b)
            best_swaps.extend(best_swap)
            tasks = swap_tasks(tasks, *best_swap)
        return ",".join(sorted(best_swaps))
    else:
        return simulate(init, tasks)

def swap_tasks(tasks, a, b):
    tc = tasks.copy()
    tc[a], tc[b] = tc[b], tc[a]
    return tc

def simulate(init, tasks):
    while tasks:
        for k, (left, op, right) in list(tasks.items()):
            if left in init and right in init:
                o = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}[op]
                init[k] = o(init[left], init[right])
                del tasks[k]
    r = [str(v) for k, v in sorted(init.items()) if k.startswith("z")]
    return int("".join(r)[::-1], 2)

def get_label(l: str, r: str, op: str):
    # special cases: carry and half 0
    if l == "&00" and r == "^01":
        return "r00" if op == "^" else "c00"

    # case: x00 ^ y00 -> ^00, x01 & y01 -> &01
    l_id, r_id = l[-2:], r[-2:]
    if l_id == r_id:
        return op + l_id

    # r..esult, c..arry, i..ntermediate
    if l_id.isnumeric() and r_id.isnumeric() and int(l_id) - int(r_id) == 1:
        match (op, l[0], r[0]):
            case ("|", "&", "c"):
                return "i" + l_id
            case ("&", "^", "i"):
                return "c" + r_id
            case ("^", "^", "i"):
                return "r" + l_id
    return None

def simulate_rep(init, tasks) -> Optional[int]:
    init = init.copy()
    for rep in range(TIMEOUT+1):
        for k, (l, op, r) in list(tasks.items()):
            if l in init and r in init:
                if not isinstance(init[l], int):
                    l = init[l]
                if not isinstance(init[r], int):
                    r = init[r]
                if l > r:
                    l, r = r, l
                init[k] = get_label(l, r, {"AND": "&", "OR": "|", "XOR": "^"}[op])
                del tasks[k]
                if init[k] is None or not tasks:
                    return rep
