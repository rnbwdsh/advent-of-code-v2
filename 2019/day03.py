from typing import List, Dict, Union

lookup = {"R": 1, "L": -1, "U": 1j, "D": -1j}

def parse_line(d: str) -> str:
    return "".join([dd[0] * int(dd[1:]) for dd in d.split(",")])

def trace(data: str) -> Dict[complex, int]:
    pos = 0
    result = {}
    for time, d in enumerate(data):
        pos = pos + lookup[d]
        result[pos] = time + 1
    return result

def test_03(data: List[str], level):
    data = [parse_line(d) for d in data]
    line1, line2 = trace(data[0]), trace(data[1])
    intersect = line1.keys() & line2.keys()

    if level:
        return min({pos: line1[pos] + line2[pos] for pos in intersect}.values())
    return int(min([abs(d.real) + abs(d.imag) for d in intersect]))
