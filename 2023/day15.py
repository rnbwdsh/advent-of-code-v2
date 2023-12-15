from collections import OrderedDict
from functools import reduce

import pytest

def hash_(s: str) -> int:
    return reduce(lambda curr, c: (curr + ord(c)) * 17 % 256, s, 0)

@pytest.mark.data("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""", 1320, 145)
def test_15(data: str, level):
    data = data.replace("\n", "").split(",")
    if level:
        boxes = [OrderedDict() for _ in range(256)]
        for part in data:
            if "=" in part:
                box, part = part.split("=")
                boxes[hash_(box)][box] = int(part)
            elif "-" in part:
                box, _ = part.split("-")
                if box in boxes[hash_(box)]:
                    del boxes[hash_(box)][box]
        return sum(box_idx * idx_slot * v
                   for box_idx, box in enumerate(boxes, 1)
                   for idx_slot, (_, v) in enumerate(box.items(), 1))
    else:
        return sum(hash_(part) for part in data)
