from typing import List

import pytest

def check_at_pos(data, x, y):
    total = 0
    for stepx, stepy in [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
        for i, letter in enumerate("XMAS"):
            xn = x + stepx * i
            yn = y + stepy * i
            if not (0 <= xn < len(data) and 0 <= yn < len(data[0])):
                break
            if data[xn][yn] != letter:
                break
        # If we didn't break, we found a match
        else:
            total += 1
    return total


def check_2_at_pos(data, i, j):
    return {(data[i - 1][j - 1]), (data[i + 1][j + 1])} == {(data[i - 1][j + 1]), (data[i + 1][j - 1])} == set("MS")


@pytest.mark.data(("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""), 18, 9)
def test_04(data: List[str], level):
    total = 0
    for i in range(level, len(data)-level):
        for j in range(level, len(data[0])-level):
            if data[i][j] == "X" and not level:
                total += check_at_pos(data, i, j)
            elif data[i][j] == "A" and level:
                total += check_2_at_pos(data, i, j)
    return total