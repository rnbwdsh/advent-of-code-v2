from level_annotations import level_a

MOD = 20201227

@level_a(25)
def solve(data=0, method=0):
    a, b = map(int, data.split("\n"))
    x = 1
    for i in range(1, 10000000000):
        x = (x * 7 % MOD)
        if a == x:
            break
    return pow(b, i, MOD)
