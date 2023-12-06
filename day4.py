import re
from typing import NamedTuple

with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = [l.strip() for l in f.readlines()]

Card = NamedTuple("Card", num=int, winners=set[int], pulls=set[int])


def winners(line: str) -> set[int]:
    split_re = re.compile(r'\s*[:|]\s*')
    winners_str = split_re.split(line.strip())[1]
    return {int(num) for num in winners_str.split()}


def pulls(line: str) -> set[int]:
    split_re = re.compile(r'\s*[:|]\s*')
    winners_str = split_re.split(line.strip())[2]
    return {int(num) for num in winners_str.split()}


def card_value(card: Card) -> int:
    """
    Calculates card value by counting the winning numbers present in `card.pulls`.
    First winner is worth 1 point, with each additional one doubling the value.
    So the value is equal to 2**(amount of winners - 1).
    1 winner -> 2^0 = 1, 2 winners -> 2^1 = 2, 3 winners -> 2^2 = 4, ...
    """
    winning_pulls = card.pulls.intersection(card.winners)
    return 2 ** (len(winning_pulls) - 1) if len(winning_pulls) > 0 else 0


cards = [Card(i, winners(l), pulls(l)) for i, l in enumerate(input_lines, start=1)]

# Part 1
card_values = map(card_value, cards)
print(f"Challenge 1: {sum(card_values)}")

# Part 2
# TODO
