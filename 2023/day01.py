from typing import List

import regex

from level_annotations import level_a, level_b

LOOKUP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def parse(nums):
    return int(LOOKUP.get(nums[0], nums[0])) * 10 + int(LOOKUP.get(nums[-1], nums[-1]))

def sol(lines, level):
    to_search = "[1234656789]" + ("|" + "|".join(LOOKUP.keys()) if level else "")
    return sum([parse(list(regex.findall(to_search, line, overlapped=True))) for line in lines])

@level_a(1, test=("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""", 142))
def solve(lines: List[str], level):
    return sol(lines, level)

# def level_ab(day: int, test: Tuple | bool = None, levels=(0, 1), quiet=False, sep="\n", apply=lambda a: a):
@level_b(1, test=("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""", 142, 281))
def solve(lines: List[str], level):
    return sol(lines, level)
