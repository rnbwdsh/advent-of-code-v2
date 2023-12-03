import re
from collections import Counter
from math import floor

import aocd
from scipy import optimize

class Inventory(Counter):
    def __init__(self, data, fuel):
        self["FUEL"] = -fuel
        # create lookup table for chemical -> (needed, {traded, given})
        lines = [list(reversed(re.split(",? =?>? ?", line))) for line in data.split("\n")]
        self.lookup = {parts[0]: (int(parts[1]), Counter(
            {parts[i]: int(parts[i + 1]) for i in range(2, len(parts), 2)})) for parts in lines}

    def loop(self):
        while True:
            # find first negative-count-non-ore
            for name, stored in self.items():
                if name != "ORE" and stored < 0: break
            else:
                return -self["ORE"]
            self.replace(name, stored // self.lookup[name][0])

    def replace(self, addtyp, amount):
        if addtyp != "ORE":
            addnum, typ_cnt = self.lookup[addtyp]
            self.update({addtyp: -addnum * amount})
            self.update(Counter({k: v * amount for k, v in typ_cnt.items()}))

assert Inventory(
    """9 ORE => 2 A\n8 ORE => 3 B\n7 ORE => 5 C\n3 A, 4 B => 1 AB\n5 B, 7 C => 1 BC\n4 C, 1 A => 1 CA\n2 AB, 3 BC, 4 CA => 1 FUEL""",
    1).loop() == 165

aocd.submit(day=14, answer=Inventory(aocd.get_data(), 1).loop())

metric = lambda i: abs(Inventory(aocd.get_data(), i).loop() - 1000000000000)
aocd.submit(floor(optimize.minimize_scalar(metric).x), day=14)
