from itertools import product
from typing import List
import numpy as np
import numba
import pytest


@numba.njit
def mix_prune(secret: int, value: int) -> int:
    return secret ^ value % 16777216

@numba.njit
def process(secret: int) -> int:
    secret = mix_prune(secret, secret * 64)
    secret = mix_prune(secret, secret // 32)
    return mix_prune(secret, secret * 2048)

@numba.njit(nopython=True, parallel=True)
def simulate_inner(buy_indicator: np.array, diffs: np.array, sequences: np.array) -> int:
    total = 0
    for seq_id in numba.prange(len(sequences)):
        diff = diffs[seq_id]
        for i, v in enumerate(diff):
            if v == buy_indicator:
                total += sequences[seq_id][i + 3]
                break
    return total

@numba.njit
def to_base20(n: np.array) -> np.array:
    return sum([n[i] * 20 ** i for i in range(4)])

@numba.njit
def gen_sequence(secret: int) -> np.array:
    curr_seq = [secret]
    for _ in range(2000):
        secret = process(secret)
        curr_seq.append(secret)
    return np.array(curr_seq[1:])

@numba.njit
def gen_diff(seq):
    diff = np.diff(seq)
    return np.array([to_base20(diff[i:i + 4]) for i in range(len(diff) - 3)])

@pytest.mark.data("1\n10\n100\n2024", 37327623, 23)
def test_21(data: List[str], level):
    if level and len(data) == 4:
        data = [1, 2, 3, 2024]
    if not level:
        return sum([gen_sequence(int(line))[-1] for line in data])
    seqs = [gen_sequence(int(line)) % 10 for line in data]
    diffs = [gen_diff(seq) for seq in seqs]
    seqs = [seq[1:] for seq in seqs]
    # heuristic that it should be -, +, -, + -> reduces search space by 8x, 5x speedup
    buy_indicators = [to_base20(p) for p in product(range(-9, 10), repeat=4) if p[3] > 0 > p[2] and p[1] > 0 > p[0]]
    # type conversions + continuous array gives another 2x speedup due to memory layout
    seq = np.array(seqs, dtype=np.int8)
    diff = np.array(diffs, dtype=np.int32)
    return max([simulate_inner(buy_indicator, diff, seq) for buy_indicator in np.array(buy_indicators, dtype=np.int32)])

def test_numbers_123():
    curr = 123
    exp = [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
    for i, number in enumerate(exp):
        curr = process(curr)
        assert curr == number

def test_simulate():
    seqs = np.array([3, 0, 6, 5, 4, 4, 6, 4, 4, 2])
    assert simulate_inner(to_base20([-1, -1, 0, 2]), [(gen_diff(seqs))], [seqs[1:]]) == 6
