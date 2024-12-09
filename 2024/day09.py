import numba
import numpy as np
import pytest

FREE = -1
BUF_SIZE = 100_000

@numba.jit
def defrag1(a, lpos, pos):
    while pos >= lpos:
        # "".join(map(str, a)).replace("-1", ".")
        while a[pos] == FREE:
            pos -= 1
            if pos < 0:
                break
            continue
        while a[lpos] != FREE:
            lpos += 1
            continue
        if pos >= lpos:
            a[pos], a[lpos] = a[lpos], a[pos]
        pos -= 1
        lpos += 1

@numba.jit
def defrag2(a, curr, file_size, file_start):
    for file_id in range(curr // 2, 0, -1):
        start = file_start[file_id]
        size = file_size[file_id]
        # find leftmost spot to place a file of size, that's left of start
        offset = 0
        found = False
        while offset < start:
            pos = 0
            while pos < size and offset + pos < start and a[offset + pos] == FREE:
                pos += 1
            if pos == size:
                found = True
                break
            offset += pos + 1
        if found:
            a[offset:offset + size] = [file_id] * size
            a[start:start + size] = [FREE] * size
        # print("".join(map(str, a[:60])).replace("-1", "."))

@numba.jit
def checksum(a):
    total = 0
    for i in range(BUF_SIZE):
        if a[i] == FREE:
            continue
        total += i * a[i]
    return total

@pytest.mark.data(("""2333133121414131402"""), 1928, 2858)
def test_09(data: str, level):
    # read logic
    a = np.array([FREE for _ in range(BUF_SIZE)])
    curr = 0
    pos = 0
    file_size = []
    file_start = []
    for c in data:
        c = int(c)
        for i in range(c):
            a[pos+i] = curr // 2 if curr %2 == 0 else -1
        if curr %2 == 0:
            file_size.append(c)
            file_start.append(pos)
        pos += c
        curr += 1

    # reorder stuff
    if not level:
        defrag1(a, int(data[0]), pos)
    else:
        defrag2(a, curr, file_size, file_start)
    return checksum(a)
