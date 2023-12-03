import aocd

def deal_with_increment(d, amount):
    nd = [0] * len(d)
    for i in range(len(d)):
        nd[(i * int(amount)) % len(d)] = d[i]
    return nd

def run(data, deck_size=10):
    d = list(range(0, deck_size))
    for line in data.split("\n"):
        words = line.split(" ")
        if words[-2] == "new": d = d[::-1]
        if words[-2] == "cut": d = d[int(words[-1]):] + d[:int(words[-1])]
        if words[-2] == "increment": d = deal_with_increment(d, words[-1])
    return d

assert run("""deal with increment 7
deal into new stack
deal into new stack""") == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
print()
assert run("""cut 6
deal with increment 7
deal into new stack""") == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
print()
assert run("""deal with increment 7
deal with increment 9
cut -2""") == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]

assert run("""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""") == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

sol = run(aocd.get_data(day=22), 10007).index(2019)
aocd.submit(sol, day=22)

def solve(data, position, deck_size, rep):
    lines = [line.split(" ") for line in data.split("\n")]

    add, mul = 0, 1
    # we iterate over the input and accumulate the actions
    for op in lines:
        # cut shifts the card into -n * past_multipliers        -> save inverse, forward shift
        if op[-2] == "cut":
            add += int(op[-1]) * mul
        # shuffle_into_new_deck reverses the deck               _> save inverse, which is normal
        elif op[-2] == "new":
            mul *= -1; add += mul
        # deal_with_increments multiplies                       -> save the inverse of this multiplication
        else:
            mul *= pow(int(op[-1]), -1, deck_size)

    # invert the current multiplier
    mul_inv = pow(1 - mul, -1, deck_size)
    # repeate the inverse multiplication
    muls = pow(mul, rep, deck_size)
    # repeat the inverse addition
    adds = add * (1 - muls) * mul_inv

    return (position * muls + adds) % deck_size

aocd.submit(solve(aocd.get_data(day=22), position=2020, deck_size=119315717514047, rep=101741582076661), day=22)
