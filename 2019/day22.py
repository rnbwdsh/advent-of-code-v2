from typing import List

def deal_with_increment(d, amount):
    nd = [0] * len(d)
    for i in range(len(d)):
        nd[(i * int(amount)) % len(d)] = d[i]
    return nd

def run(data, deck_size=10):
    d = list(range(0, deck_size))
    for line in data:
        words = line.split(" ")
        if words[-2] == "new": d = d[::-1]
        if words[-2] == "cut": d = d[int(words[-1]):] + d[:int(words[-1])]
        if words[-2] == "increment": d = deal_with_increment(d, words[-1])
    return d

def test_22(data: List[str], level):
    if level:
        # values found via manual inspection
        position, deck_size, rep = 2020, 119315717514047, 101741582076661

        lines = [line.split(" ") for line in data]

        add, mul = 0, 1
        # we iterate over the input and accumulate the actions
        for op in lines:
            # cut shifts the card into -n * past_multipliers        -> save inverse, forward shift
            if op[-2] == "cut":
                add += int(op[-1]) * mul
            # shuffle_into_new_deck reverses the deck               _> save inverse, which is normal
            elif op[-2] == "new":
                mul *= -1
                add += mul
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
    else:
        return run(data, 10007).index(2019)
