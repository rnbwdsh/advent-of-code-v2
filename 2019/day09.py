from typing import List

from computer import Computer

def test_09(data: List[int], level):
    res = Computer(data).compute([1 + level])
    return res[0] if level else ",".join(map(str, res))
