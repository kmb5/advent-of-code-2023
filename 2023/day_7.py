from __future__ import annotations

from enum import Enum
from collections import Counter
from functools import cmp_to_key

sample = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

CARD_STRENGTHS = {c: i for i, c in enumerate("23456789TJQKA")}
CARD_STRENGTHS_P2 = {c: i for i, c in enumerate("J23456789TQKA")}


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    def __init__(self, cards, p="p1"):
        self.cards = cards
        self.part = p
        if p == "p1":
            self.type_ = self.get_type()
        else:
            self.type_ = self.get_type_p2()

    def __str__(self):
        return self.cards

    def __repr__(self):
        return self.cards

    def get_type(self, cntr=None) -> HandType:
        if cntr is None:
            cntr = Counter(self.cards)
        if len(cntr) == 1:
            return HandType.FIVE_OF_A_KIND
        if len(cntr) == 2:
            if 4 in cntr.values():
                return HandType.FOUR_OF_A_KIND
            return HandType.FULL_HOUSE
        if len(cntr) == 3:
            if 3 in cntr.values():
                return HandType.THREE_OF_A_KIND
            return HandType.TWO_PAIR
        if len(cntr) == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def get_type_p2(self) -> HandType:
        cntr = Counter(self.cards)
        if "J" not in cntr:
            return self.get_type()
        if "J" in cntr and len(cntr) == 1:
            return self.get_type()

        # we need to make a copy first without "J"
        # to find the card with the highest occurrence that isn't J
        _cntr = {i: cntr[i] for i in cntr if i != "J"}
        max_key = max(_cntr, key=_cntr.get)

        _cntr[max_key] += cntr["J"]
        return self.get_type(cntr=_cntr)

    def compare(self, a, b) -> bool:
        """True if a > b, False if a < b, None if they are equal"""
        strengths = CARD_STRENGTHS_P2 if self.part == "p2" else CARD_STRENGTHS
        if a == b:
            return None
        return strengths[a] > strengths[b]


def define_order(h1: Hand, h2: Hand) -> int:
    if h1.type_.value == h2.type_.value:
        for i, card in enumerate(h1.cards):
            other = h2.cards[i]
            if h1.compare(card, other) is True:
                return -1
            if h1.compare(card, other) is False:
                return 1
        # both cards are exactly the same
        return 0
    if h1.type_.value > h2.type_.value:
        return -1
    return 1


def parse(inp, p="p1"):
    hands = []
    bids = {}
    for row in inp.splitlines():
        hand, bid = row.split()
        hand = Hand(hand, p)
        hands.append(hand)
        bids[hand] = int(bid)
    return hands, bids


def solve(inp, p="p1"):
    total_winnings = 0
    hands, bids = parse(inp, p)
    s = sorted(hands, key=cmp_to_key(define_order), reverse=True)
    for i, hand in enumerate(s):
        rank = i + 1
        total_winnings += rank * bids[hand]

    return total_winnings


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_7_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = solve(inp)
    print("Part 1: ", part1_sol)

    part2_sol = solve(inp, "p2")
    print("Part 2: ", part2_sol)


def test_hands():
    assert Hand("AAAAA").type_ == HandType.FIVE_OF_A_KIND
    assert Hand("AA8AA").type_ == HandType.FOUR_OF_A_KIND
    assert Hand("23332").type_ == HandType.FULL_HOUSE
    assert Hand("TTT98").type_ == HandType.THREE_OF_A_KIND
    assert Hand("23432").type_ == HandType.TWO_PAIR
    assert Hand("A23A4").type_ == HandType.ONE_PAIR
    assert Hand("23456").type_ == HandType.HIGH_CARD

    h1, h2 = Hand("33332"), Hand("2AAAA")
    assert define_order(h1, h2) == -1

    h1, h2 = Hand("77888"), Hand("77788")
    assert define_order(h1, h2) == -1


def test_p2():
    assert Hand("T55J5", "p2").type_ == HandType.FOUR_OF_A_KIND
    assert Hand("KTJJT", "p2").type_ == HandType.FOUR_OF_A_KIND
    assert Hand("QQQJA", "p2").type_ == HandType.FOUR_OF_A_KIND
    assert Hand("QJJQ2", "p2").type_ == HandType.FOUR_OF_A_KIND
    assert Hand("JJJAJ", "p2").type_ == HandType.FIVE_OF_A_KIND
    assert Hand("JAAJK", "p2").type_ == HandType.FOUR_OF_A_KIND

    h1, h2 = Hand("AJAAA", "p2"), Hand("AAJAJ", "p2")
    assert define_order(h1, h2) == 1

    h1, h2 = Hand("JKKK2", "p2"), Hand("QQQQ2", "p2")
    assert define_order(h1, h2) == 1

    assert define_order(Hand("JJJJJ", "p2"), Hand("AAAAA", "p2")) == 1
    assert define_order(Hand("JJJAJ", "p2"), Hand("AAAAA", "p2")) == 1


if __name__ == "__main__":
    test_hands()
    test_p2()
    main()
