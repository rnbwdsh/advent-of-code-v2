import re

from level_annotations import level_ab

def match(key: str, val: str):
    match key:
        case "byr":
            return 1920 <= int(val) <= 2002
        case "iyr":
            return 2010 <= int(val) <= 2020
        case "eyr":
            return 2020 <= int(val) <= 2030
        case "hgt":
            return (val[-2:] == "cm" and 150 <= int(val[:-2]) <= 193) or (
                        val[-2:] == "in" and 59 <= int(val[:-2]) <= 76)
        case "hcl":
            return len(val) == 7 and val[0] == "#" and set(val[1:]).issubset(set("0123456789abcdef"))
        case "ecl":
            return val in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        case "pid":
            return len(val) == 9 and set(val).issubset(set("0123456789"))
        case "cid":
            return True
        case _:
            return False

@level_ab(4, sep="\n\n")
def solve(data, level):
    ctr = 0
    allowed = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    for line in data:
        ut = dict([token.split(":") for token in re.split("[ \n]+", line)])
        if level:  # part b
            stats = [k in ut and match(k, ut[k]) for k in allowed]
            ctr += all(stats)
        else:  # part a
            ctr += allowed.issubset(set(ut))
    return ctr
