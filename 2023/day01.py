import pytest
import regex

LOOKUP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def parse(nums):
    return int(LOOKUP.get(nums[0], nums[0])) * 10 + int(LOOKUP.get(nums[-1], nums[-1]))

@pytest.mark.data(("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""", """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""), 142, 281)
def test_01(data, level):
    to_search = "[1234656789]" + ("|" + "|".join(LOOKUP.keys()) if level else "")
    return sum([parse(list(regex.findall(to_search, line, overlapped=True))) for line in data])
