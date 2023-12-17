import re
from math import lcm
from typing import Dict, Tuple

import pytest

@pytest.mark.data(("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""",
                   """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""), 2, 6)
def test_08(data: str, level):
    instructions, _, *conn = data.split("\n")
    conn = [re.match(r"(\w+) = \(([\w, ]+), ([\w, ]+)\)", c_line).groups() for c_line in conn]
    conn = {a: (b, c) for a, b, c in conn}
    if level:
        starts = [pos for pos in conn if pos.endswith("A")]
        return lcm(*[run_sim(instructions, conn, pos) for pos in starts])
    return run_sim(instructions, conn, "AAA")

def run_sim(instructions: str, conn: Dict[str, Tuple[str, str]], pos: str):
    for time in range(1000000):
        step = instructions[time % len(instructions)]
        choice = conn[pos]
        pos = choice[step == "R"]
        if pos.endswith("Z"):
            return time + 1
