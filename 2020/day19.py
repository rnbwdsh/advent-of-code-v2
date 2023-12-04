import re
from typing import List

import lark
from lark import Lark

def test_19(data: List[str], level):
    rules, examples = data
    if level:
        rules = re.sub(r"\n8:.+", "\n8: 42 | 42 8", rules)
        rules = re.sub(r"\n11:.+", "\n11: 42 31 | 42 11 31", rules)
    rules = re.sub(r"\d+", lambda d: "start" if d.group() == "0" else "w" + d.group(), rules)
    parser = Lark('%ignore " "\n' + rules)

    cnt = 0
    for example in examples.split("\n"):
        try:
            parser.parse(example)
            cnt += 1
        except lark.LarkError:
            pass
    return cnt
