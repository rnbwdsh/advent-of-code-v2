import re
from collections import Counter
from typing import List

import pytest

@pytest.mark.data("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""", 13, 30)
def test_05(data: List[str], level):
    total = 0
    ctr = Counter()
    for line in data:
        num, left, right = re.search( r'Card +(\d+):([\d ]+)\|([\d ]+)', line.replace("  ", " ")).groups()
        left  = set([int(l) for l in  left.strip().split(" ")])
        right = set([int(r) for r in right.strip().split(" ")])
        nr_match = len(left & right)
        if nr_match:
            total += 1 << (nr_match - 1)
        ctr[int(num)] = nr_match
    if level:
        max_id = max(ctr.keys())
        ticket_num = Counter(ctr.keys())
        for src in range(max_id):
            ticket_num += {to_add+1: ticket_num[src]
                           for to_add in range(src, src + ctr[src])
                           if to_add < max_id}
        return sum(ticket_num.values())
    return total
