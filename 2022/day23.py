from collections import Counter

def test_23(data, level):
    curr_pos = [x + y * 1j for y, line in enumerate(data) for x, c in enumerate(line) if c == "#"]
    move_dirs = [(m, 0, 1j * m, -1j * m) for m in [-1j, 1j, -1, 1]]
    around = (1, 1 + 1j, 1j, -1 + 1j, -1, -1 - 1j, -1j, 1 - 1j)
    for t in range(10_000 if level else 10):
        cps = set(curr_pos)  # way faster lookup
        next_pos = [None for _ in curr_pos]  # initialize target array
        for i, p in enumerate(curr_pos):
            if any((p + a) in cps for a in around):
                for m, c1, c2, c3 in move_dirs:  # precomputing + unrolling = performance.
                    if not ((p + m + c1) in cps or (p + m + c2) in cps or (p + m + c3) in cps):
                        next_pos[i] = p + m
                        break

        cntr = Counter(next_pos)  # fastest way to check double-allocations
        for i, p in enumerate(next_pos):
            if cntr[p] == 1 and p is not None:
                curr_pos[i] = next_pos[i]  # noqa   # weird typing error

        move_dirs = move_dirs[1:] + move_dirs[:1]  # rotate move_dirs
        if level and all(n is None for n in next_pos):
            return t + 1
    x, i = [c.real for c in curr_pos], [c.imag for c in curr_pos]
    return round((max(x) - min(x) + 1) * (max(i) - min(i) + 1) - len(curr_pos))
