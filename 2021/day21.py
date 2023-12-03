from collections import defaultdict

def forward(pos0, pos1, s0, s1, t, i):
    curr = (t // 3) % 2  # current player = time / 3, as every roll advances time by 1
    curr_pos = ([pos0, pos1][curr] + i - 1) % 10 + 1
    if curr:
        pos1 = curr_pos
    else:
        pos0 = curr_pos
    if (t % 3) == 2:
        if curr:
            s1 += curr_pos
        else:
            s0 += curr_pos
    return pos0, pos1, s0, s1

def test_21(data, level):
    pos = [int(data[i][-1:]) for i in range(2)]
    die = iter(range(1, 9999))  # for part 1
    stop = 21 if level else 1000
    # inits for part 2
    worlds = {(*pos, 0, 0): 1}
    winners = [0, 0]

    for t in range(9999):
        next_worlds = defaultdict(int)
        for world, cnt in list(worlds.items()):
            for roll in range(1, 4) if level else [next(die)]:  # yields a single number for part 1:
                w = forward(*world, t, roll)
                s0, s1 = w[-2:]  # extract s0 and s1 by unpacking
                if s0 >= stop or s1 >= stop:
                    if not level:
                        return min(s0, s1) * roll
                    winners[s1 >= stop] += cnt
                else:
                    next_worlds[w] += cnt
        worlds = next_worlds
        if not worlds: break
    return max(winners)
