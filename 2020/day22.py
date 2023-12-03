from level_annotations import level_ab

def play_rec(p1, p2, rec_lvl=1):
    history = set()
    while p1 and p2:
        h = hash((tuple(p1), tuple(p2)))
        if h in history:
            return 1, 0
        history.add(h)

        c1, c2 = p1.pop(0), p2.pop(0)
        if rec_lvl and len(p1) >= c1 and len(p2) >= c2:
            winner, _ = play_rec(p1[:c1], p2[:c2], rec_lvl + 1)
        else:
            winner = c1 > c2
        if winner:
            p1 += [c1, c2]
        else:
            p2 += [c2, c1]
    return p1, p2

@level_ab(22, sep="\n\n")
def solve(data, method=0):
    p1, p2 = [list(map(int, d.split("\n")[1:]))
              for d in data]
    p1, p2 = play_rec(p1, p2, method)  # method = 0 means never recurse
    p = reversed(p1 + p2)
    return sum([card * (i + 1) for i, card in enumerate(p)])
