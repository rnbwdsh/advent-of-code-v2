import re
from collections import Counter
from math import floor

import pytest
from scipy import optimize

class Inventory(Counter):
    def __init__(self, data, fuel):
        super().__init__()
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

    def replace(self, add_typ, amount):
        if add_typ != "ORE":
            add_num, typ_cnt = self.lookup[add_typ]
            self.update({add_typ: -add_num * amount})
            self.update(Counter({k: v * amount for k, v in typ_cnt.items()}))

@pytest.mark.notest
def test_14(data: str, level):
    if level:
        metric = lambda i: abs(Inventory(data, i).loop() - 1000000000000)
        return floor(optimize.minimize_scalar(metric).x)
    return Inventory(data, 1).loop()
