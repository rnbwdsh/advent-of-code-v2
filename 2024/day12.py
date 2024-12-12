import numpy as np
import pytest
import numba

DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def connected_copy(data: np.array, x: int, y: int):
    """ return a padded array of all nodes that have the same letter as data[x, y], padded by 1 """
    dc = np.zeros(data.shape, dtype=np.int8)
    letter = data[x, y]
    to_visit = [(x, y)]
    while to_visit:
        x, y = to_visit.pop()
        if dc[x, y] == 0:
            dc[x, y] = 1
            for dx, dy in DIR:
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= data.shape[0] or ny >= data.shape[1]:
                    continue
                if data[nx, ny] == letter:
                    to_visit.append((nx, ny))
                    data[nx, ny] = " "
    return dc


def perimeter(data: np.array) -> int:
    # make a copy shifted 1 to the left, right, up, down
    cnt = 0
    data = np.pad(data, 1)
    for pos in zip(*np.where(data == 1)):
        for dx, dy in DIR:
            nx, ny = pos[0] + dx, pos[1] + dy
            if data[nx, ny] != data[pos]:
                cnt += 1
    return cnt

@numba.njit
def count_continuous(data: np.array, bitmask: int) -> int:
    total = 0
    for line in data:
        inside = False
        for i in range(1, len(line)):
            if line[i] & bitmask and not inside:
                inside = True
                total += 1
            elif not (line[i] & bitmask):
                inside = False
    return total

def nr_sides(data: np.array) -> int:
    data = np.pad(data, 1)

    for pos in zip(*np.where(data == 1)):
        for dir_id, (dx, dy) in enumerate(DIR, 1):
            nx, ny = pos[0] + dx, pos[1] + dy
            if data[nx, ny] == 1:
                continue
            data[nx, ny] |= 1 << dir_id

    return count_continuous(data.T, 2) + count_continuous(data.T, 4) + count_continuous(data, 8) + count_continuous(data, 16)

def test_sides():
    a = np.array([[0, 1], [1, 1], [1, 0]])
    assert nr_sides(a) == 8

def test_sides_E():
    a = np.array([[1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1]])
    assert nr_sides(a) == 12


@pytest.mark.data("""AAAA
BBCD
BBCC
EEEC""", 140, 80)
def test_12(data: np.array, level):
    total = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] == " ":
                continue
            cc = connected_copy(data, i, j)
            area = int(np.sum(cc == cc[i, j]))
            total += area * (nr_sides(cc) if level else perimeter(cc))
    return total
