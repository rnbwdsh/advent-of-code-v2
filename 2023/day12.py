import re
from functools import cache
from typing import List, Tuple

import pytest


@cache
def calc_repl(s: str, repl: Tuple[int], in_string=False) -> int:
    """ Example: #?# -> #.#, ###
    replaces the first ? with . and then with #, and if there are any more ? in there, it calls itself again """
    if not s and (not repl or repl == (0,)):
        return 1
    if (not repl and "#" in s) or sum(repl) > (s.count("#") + s.count("?")):
        return 0

    sn = s[1:]
    r0 = repl[0] if repl else 0
    repl_next = tuple([r0 - 1]) + repl[1:] if repl else (0,)

    if s[0] == ".":
        if in_string and r0:        return 0
        elif in_string and not r0:  return calc_repl(sn, repl[1:], False)
        elif not in_string:         return calc_repl(sn, repl if r0 else repl[1:], False)
    elif s[0] == "#":
        if in_string and r0:        return calc_repl(sn, repl_next, True)
        elif in_string and not r0:  return 0
        elif not in_string:         return calc_repl(sn, repl_next if r0 else repl[1:], True)
    elif s[0] == "?":
        if in_string and r0:        return calc_repl(sn, repl_next, True)
        elif in_string and not r0:  return calc_repl(sn, repl[1:], False)
        elif not in_string and r0:  return calc_repl(sn, repl, False) + calc_repl(sn, repl_next, True)
        else:                       return calc_repl(sn, repl, False)

def count_continous_hashtags(l):
    """ Example: ###...#.# -> 3,1,1"""
    return [len(group) for group in re.findall(r"(#+)", l)]

@pytest.mark.data("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 21, 525152)
def test_12(data: List[str], level):
    total = 0
    for line_id, line in enumerate(data):
        line, replacements = line.split(" ")
        replacements = [int(r) for r in replacements.split(",")]
        if level:
            line = "?".join([line] * 5)
            replacements = [r for r in replacements]*5
        score = calc_repl(line, tuple(replacements), False)
        total += score
    return total
