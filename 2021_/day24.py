import math

from z3 import BitVec, BitVecVal, Optimize, If

from level_annotations import level_ab

@level_ab(24, sep="\n")
def test(lines, level):
    s = Optimize()
    size = int(math.log2(10 ** 14)) + 1  # 47
    digits = [BitVec(f'd_{i}', size) for i in range(14)]
    var = {r: 0 for r in 'xyzw'}

    pos = 0
    for i, inst in enumerate(lines):
        instr, a_name, *b = inst.split()
        a = var[a_name]
        if b:
            b = var[b[0]] if b[0] in var else int(b[0])
        c = BitVec(f'v_{i}', size)

        match instr:  # py3.10 ftw
            case 'inp':
                c = digits[pos];
                pos += 1
            case 'add':
                s.add(c == a + b)
            case 'mul':
                s.add(c == a * b)
            case 'mod':
                s.add(c == a % b)
            case 'div':
                s.add(c == a / b)
            case 'eql':
                s.add(c == If(a == b, BitVecVal(0, size), BitVecVal(1, size)))  # this is the secret for performance
        var[a_name] = c  # overwrite register

    # extra contrains: digits in 1 - 9
    s.add([0 < d for d in digits])
    s.add([d < 10 for d in digits])
    s.add(var['z'] == 0)

    # start solver
    optimizer = [s.maximize, s.minimize][level]
    optimizer(sum((10 ** i) * d for i, d in enumerate(digits[::-1])))
    s.check()
    m = s.model()
    return ''.join([str(m[d]) for d in digits])
