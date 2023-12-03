from collections import Counter

from level_annotations import level_ab

def substitute_step(cp, rules):
    nc = Counter()
    for (a, b), cnt in cp.items():
        m = rules.get(a + b, "")  # if not found, get empty -> new keys will be len(1), case for letter-count
        nc[a + m] += cnt
        nc[m + b] += cnt
    return nc

@level_ab(14)
def test(lines, level):
    d = lines[0]
    rules = dict([rule.split(" -> ") for rule in lines[2:]])  # lookup dict: first, second -> insert
    pair_cnt = Counter([d[i:i + 2] for i in range(len(d) - 1)])  # count pairs
    for j in range(40 if level else 10):
        pair_cnt = substitute_step(pair_cnt, rules)
    letter_cnt = substitute_step(pair_cnt, {})
    letter_cnt[d[0]] += 1  # corner case: first and last char stay const and appear 1x more
    letter_cnt[d[-1]] += 1
    return (max(letter_cnt.values()) - min(letter_cnt.values())) // 2
