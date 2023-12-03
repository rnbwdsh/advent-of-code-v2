import aocd

ran = range(*map(int, aocd.get_data(day=4).split("-")))
print(ran)

check2 = lambda n: any([str(i) * 2 in n for i in range(10)])
ordered = lambda n: n == "".join(sorted(n))
test = lambda n: ordered(n) and check2(n)

assert test("111111")
assert not test("223450")
assert test("111122")
assert test("366666")

res = sum([test(str(r)) for r in ran])
aocd.submit(res, day=4)

check2not3 = lambda n: any([str(i) * 2 in n and not str(i) * 3 in n for i in range(10)])
test2 = lambda n: ordered(n) and check2not3(n)

assert test2("112233")
assert not test2("123444")
assert test2("111122")

res = sum([test2(str(r)) for r in ran])
aocd.submit(res, day=4)
