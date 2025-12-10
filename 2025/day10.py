from typing import List

import pytest
import z3


def solve(line: str, level) -> int:
    target, combos = line[1:].split("]")
    target = [i == "#" for i in target]
    *combos, last = combos[1:].split(" ")
    combos = [[int(i) for i in combo[1:-1].split(",")] for combo in combos]
    if level:
        target = tuple(int(i) for i in last[1:-1].split(","))

    # create a z3 optimizer that finds the minimal number of presses (multipliers)
    s = z3.Optimize()
    multiplier_vars = [z3.Int(f'mult_{i}') for i in range(len(combos))]
    for mv in multiplier_vars:
        s.add(mv >= 0)
    for i, t in enumerate(target):
        total = z3.Sum([mv for j, mv in enumerate(multiplier_vars) if i in combos[j]])
        s.add((t == total) if level else (t == total % 2))
    s.minimize(z3.Sum(multiplier_vars))
    if s.check() == z3.sat:
        return sum(s.model()[mv].as_long() for mv in multiplier_vars)
    raise ValueError("No solution found")


@pytest.mark.data('''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}''', None, 33)
def test_10(data: List[str], level):
    return sum(solve(line, level) for line in data)
