import re
from itertools import combinations
from typing import List

from computer import Computer

START = 'east\ntake manifold\nsouth\ntake whirled peas\nnorth\nwest\nsouth\ntake space heater\nsouth\ntake dark matter\nnorth\neast\nnorth\nwest\nsouth\ntake antenna\nnorth\neast\nsouth\neast\ntake bowl of rice\nnorth\ntake klein bottle\nnorth\ntake spool of cat6\nwest\n'
FORBIDDEN_A = "ship are lighter than the detected"
FORBIDDEN_B = "ship are heavier than the detected"

def test_25(data: List[int], level_a):
    # ignored items: escape pod, giant electromagnet, photons, molten lava, infinite loop
    # manually explored maze and took all the items
    p = Computer(data)
    p.compute_str(START)

    # trim away "Items in sour inventory" before and "\nCommand?\n" after and generate drop commands
    items = p.compute_str("inv\n").replace("-", "drop").split("\n")[2:-3]

    # try to drop any amount of items until you are allowed to pass the door
    for i in range(len(items)):
        for ic in combinations(items, i):
            out = Computer(data).compute_str(START + "\n".join(ic) + "\nnorth\n")
            if FORBIDDEN_A not in out and FORBIDDEN_B not in out:
                return int(re.findall("\d+", out)[0])
