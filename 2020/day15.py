from level_annotations import level_ab

@level_ab(15, apply=int, sep=",")
def solve(data, method=0):
    # numba doesn't support int(), so parsing must be done outside optimized code
    seen = dict()  # can't init as a 1-liner due to numba
    for i, nr in enumerate(data):
        seen[nr] = i + 1
    number = 0
    for i in range(len(data) + 1, 30_000_000 if method else 2020):
        # same time assignment: use old number to set, then set number, using old number
        seen[number], number = i, (i - seen[number]) if number in seen else 0
    return number
