from collections import Counter
from typing import List

from computer import Computer

def test_23(data: List[int], level):
    proc, packets, nat = [], [], []
    a = b = 0  # avoid unreferenced variable error
    ctr = Counter()

    # init processors and send -1 package
    for i in range(50):
        proc.append(Computer(data))
        packets += proc[i].compute([i, -1])

    # network loop: send and collect packets
    for i in range(100):  # repeat arbitrary amount of times
        while packets:  # false if empty
            dest, x, y = packets.pop(0), packets.pop(0), packets.pop(0)
            if dest == 255:  # 255 package goes to nat
                if i == 0: a = y  # save first nat package for later
                nat = [x, y]  # overwrite nat package
            else:  # normal case: process package
                packets += proc[dest].compute([x, y])

        # after all packets have been sent, send nat package to proc0
        packets += proc[0].compute(nat[:])

        # check if a message was sent twice
        ctr.update({nat[1]: 1})  # increase counter for current y by 1
        mc = ctr.most_common()[0]  # tuple (most_common_element, cnt)
        if mc[1] == 2: b = mc[0]; break
    return b if level else a
