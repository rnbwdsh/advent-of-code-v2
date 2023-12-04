from collections import Counter

def test_06(data: str, level):
    cnt = 0
    for section in data.split("\n\n"):
        nr_lines = section.count("\n") + 1
        if level:
            cnt += sum([lcnt == nr_lines and l != "\n" for l, lcnt in Counter(section).items()])
        else:
            cnt += len(set(section).difference({"\n"}))
    return cnt
