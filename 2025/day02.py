import pytest

def check_num_str(s: str, i: int) -> bool:
    return all(s[0:i] == s[j:j+i] for j in range(i, len(s), i))

@pytest.mark.data(("11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"), 1227775554, 4174379265)
def test_02(data: str, level):
    sum_invalid = 0
    for r in data.split(","):
        start, end = map(int, r.split("-"))
        for i in range(start, end + 1):
            si = str(i)
            if (not level and not len(si) % 2 != 0 and si[:(len(si) // 2)] == si[(len(si) // 2):] or
                    level and any(check_num_str(si, i) for i in range(1, len(si)))):
                sum_invalid += i
    return sum_invalid

