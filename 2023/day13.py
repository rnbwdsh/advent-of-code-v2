from typing import List

import numpy as np
import pytest

import parsers

def score_reflection(chunk: np.ndarray, not_allowed=0):
    for field, mul in ((chunk, 100), (chunk.T, 1)):
        for i in range(1, len(field)):
            right = field[i:i*2]
            left = field[i-len(right):i]
            if np.equal(left, right[::-1]).all():
                score = mul * i
                if score != not_allowed:
                    return score

def score_smudge(field: np.ndarray, score_orig: int):
    for (y, x), val in np.ndenumerate(field):
        fc = field.copy()
        fc[y, x] = ~ val
        score = score_reflection(fc, score_orig)
        if score:
            return score

@pytest.mark.data("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""", 405, 400)
def test_13(data: List[List[str]], level):
    chunks = (np.equal(parsers.parse_array("\n".join(chunk)), "#") for chunk in data)
    return sum(score_smudge(field, score_reflection(field, 0)) if level else
               score_reflection(field, 0)
               for field in chunks)
