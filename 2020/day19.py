import re

from lark import Lark

from level_annotations import level_ab

@level_ab(19, test=False, sep="\n\n")
def solve(data, method=0):
    rules, examples = data
    if method:
        rules = re.sub(r"\n8:.+", "\n8: 42 | 42 8", rules)
        rules = re.sub(r"\n11:.+", "\n11: 42 31 | 42 11 31", rules)
    rules = re.sub(r"\d+", lambda d: "start" if d.group() == "0" else "w" + d.group(), rules)
    parser = Lark('%ignore " "\n' + rules)

    cnt = 0
    for example in examples.split("\n"):
        try:
            parser.parse(example);
            cnt += 1
        except:
            pass
    return cnt
