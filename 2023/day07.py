from collections import Counter
from typing import List

import pytest

@pytest.mark.data("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""", 6440, 5905)
def test_07(data: List[str], level):
    all_hands = [parse(line, level) for line in data]
    return sum(bid * (rank + 1) for rank, (_, _, bid) in enumerate(sorted(all_hands)))

def score_hand_0(hand: List[int]):
    nr_ctr = dict(Counter(Counter(hand).values()))
    patterns = [{1: 5}, {2: 1, 1: 3}, {2: 2, 1: 1}, {3: 1, 1: 2}, {2: 1, 3: 1}, {4: 1, 1: 1}, {5: 1}]
    for score, pattern in enumerate(patterns):
        if pattern == nr_ctr:
            return score
    raise ValueError(f"Unknown hand: {hand} {nr_ctr}")

def permuted(hand: List[int], repl: int):
    hc = hand.copy()
    hc[hand.index(0)] = repl
    return score_hand_1(hc)

def score_hand_1(hand: List[int]):
    if 0 not in hand:
        return score_hand_0(hand)
    return max(permuted(hand, card) for card in range(1, 13))

def parse(line: str, level):
    hand, bid = line.split(" ")
    hand = [("J23456789TQKA".index(card) if level else "23456789TJQKA".index(card)) for card in hand]
    score = score_hand_1(hand) if level else score_hand_0(hand)
    return score, hand, int(bid)
