from collections import Counter

from level_annotations import level_ab

@level_ab(6)
def solve(data, level):
    cnt = 0
    for section in data.split("\n\n"):
        nr_lines = section.count("\n") + 1
        if level:
            cnt += sum([lcnt == nr_lines and l != "\n" for l, lcnt in Counter(section).items()])
        else:
            cnt += len(set(section).difference({"\n"}))
    return cnt
