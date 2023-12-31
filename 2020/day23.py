from typing import List

import numpy as np

def get_followers(g, node, nr) -> List[int]:
    for _ in range(nr):
        node = g[node]
        yield node

def solve_(data, method):
    g = {}
    for i in range(len(data) - 1):
        g[data[i]] = data[i + 1]
    g[data[-1]] = data[0]

    current_cup = data[0]
    for i in range(10_000_000 if method else 100):
        n1, n2, n3, n4 = get_followers(g, current_cup, 4)
        g[current_cup] = g[n3]  # unlink 3 selected cups
        dst_cup = current_cup - 1  # set dst to current-1
        while (dst_cup in [n1, n2, n3]) or (dst_cup <= 0):
            dst_cup -= 1  # if dst_cup in picked-up, decrement
            if dst_cup <= 0:  # cycling around negatively
                dst_cup = len(g)
        dst_follower = list(get_followers(g, dst_cup, 1))[0]
        g[dst_cup] = n1  # link dest to first picked up
        g[n3] = dst_follower  # link last picked up to 
        current_cup = n4
    return get_followers(g, 1, 2 if method else len(g) - 1)

def test_23(data: str, level):
    data = [int(d) for d in data]
    data += range(len(data) + 1, 1_000_000 + 1) if level else []
    followers = solve_(data, level)
    if level:
        return np.prod(list(followers))
    else:
        return "".join([str(x) for x in followers])
