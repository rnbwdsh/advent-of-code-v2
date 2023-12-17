from functools import cache
from typing import List, Tuple

import pytest

@pytest.mark.data("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 21, 525152)
def test_12(data: List[str], level):
    total = 0
    for line in data:
        line, replacements = line.split(" ")
        replacements = [int(r) for r in replacements.split(",")]
        if level:
            line = "?".join([line] * 5)
            replacements = [r for r in replacements] * 5
        score = calc_repl(line, tuple(replacements), False)
        total += score
    return total

@cache
def calc_repl(s: str, r: Tuple[int], in_string=False) -> int:
    """ Recursively calculate the number of replacements for a given string and a pattern of replacements """
    if not s and (not r or r == (0,)):
        return 1
    if (not r and "#" in s) or sum(r) > (s.count("#") + s.count("?")):
        return 0

    s, sn = s[0], s[1:]  # can't use deconstruct, because that would result in an tuple (un-cache-able)
    r0 = r[0] if r else 0

    if s == "." and in_string and r0 or s == "#" and not r0:
        return 0  # recursion root: can't continue with ? or .
    if s == "?" and not in_string and r0:
        return calc_repl("." + sn, r, False) + calc_repl("#" + sn, r, False)  # call self but with # and . instead of ?
    if (s == "#" or s == "?" and in_string) and r0:
        r = tuple([r0 - 1]) + r[1:]  # reduce the repl[ß] by 1
    if (s == "." or s == "?" and in_string) and not r0:
        r = r[1:]  # remove the repl[0] if it's 0
    in_string = s == "#" or s == "?" and r0  # the next in-string depends on the current char and the repl[0]
    return calc_repl(sn, r, in_string)
