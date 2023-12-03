from collections import defaultdict

def test_05(data, level):
    stacks = defaultdict(list)
    data = iter(data)
    for line in data:
        if line.startswith(" 1 "):
            next(data)  # forward iterator by 1
            break
        for pos, dst in enumerate(line):
            if dst.isalpha():  # skip "[", "]", " "
                stacks[1 + pos // 4].insert(0, dst)
    for line in data:
        _, amount, _, src, _, dst = line.split(" ")
        amount, src, dst = int(amount), int(src), int(dst)
        picked = [stacks[src].pop() for _ in range(amount)]
        stacks[dst].extend(reversed(picked) if level else picked)
    return "".join([stacks[i][-1] for i in sorted(stacks.keys())])
