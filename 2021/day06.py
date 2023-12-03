from collections import Counter

from level_annotations import level_ab

def test_06(data: str, level):
    cnt = Counter(map(int, data.split(",")))
    for i in range(256 if level else 80):
        cnt = Counter({k - 1: v for k, v in cnt.items()})
        cnt[6] += cnt.get(-1, 0)
        cnt[8] += cnt.get(-1, 0)
        cnt[-1] = 0
    return sum(cnt.values())
