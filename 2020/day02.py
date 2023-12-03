from level_annotations import level_ab

@level_ab(2)
def solve(data, level):
    cnt = 0
    for line in data:
        nr, letter, pw = line.split(" ")
        letter = letter[0]
        start, end = map(int, nr.split("-"))
        if level == 0:
            cnt += pw.count(letter[0]) in range(int(start), int(end) + 1)
        else:
            cnt += (pw[start - 1] + pw[end - 1]).count(letter) == 1
    return cnt
