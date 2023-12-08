from collections import Counter, defaultdict


class Hand:
    # `hand` can be assumed to always be of length 5 (per puzzle description.
    hand: list[str]
    # `original hand` stores the hand before replacing J-cards. Required for breaking ties in part 2
    original_hand: list[str]
    hand_count: defaultdict[str, int]
    bid: int
    card_order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def __init__(self, hand: str, bid: int, j_are_joker: bool = False):
        """
        Builds a Hand instance from the Hand-string and a bidding value.

        :param hand: 5-character string consisting of characters in `self.card_order`.
        :param bid:
        :param j_are_joker:
        """
        self.bid = int(bid)

        self.hand = [char for char in hand.strip().upper()]
        self.original_hand = [char for char in hand.strip().upper()]
        if len(self.hand) != 5 or any((char not in self.card_order) for char in self.hand):
            raise ValueError("Length of `hand` must be exactly 5 and consist of valid card abbreviations!")

        # This is for part 2, which changes the meaning of J-cards to Jokers. They can be optimized right away.
        if j_are_joker:
            self.card_order = ["J"] + [c for c in self.card_order if c != "J"]
            self.optimize_jokers()

        # After possible modifications for part 2, create the hand_count
        self.hand_count = defaultdict(int)
        self.hand_count.update(Counter(self.hand))

    def __str__(self) -> str:
        return f"{self.hand} ({self.bid})"

    @property
    def is_5oak(self) -> bool:
        return set(self.hand_count.values()) == {5}

    @property
    def is_4oak(self) -> bool:
        return set(self.hand_count.values()) == {1, 4}

    @property
    def is_full_house(self) -> bool:
        return set(self.hand_count.values()) == {2, 3}

    @property
    def is_3oak(self) -> bool:
        return sorted(self.hand_count.values()) == [1, 1, 3]

    @property
    def is_two_pair(self) -> bool:
        return sorted(self.hand_count.values()) == [1, 2, 2]

    @property
    def is_one_pair(self) -> bool:
        return sorted(self.hand_count.values()) == [1, 1, 1, 2]

    @property
    def high_cards(self) -> tuple[int, ...]:
        # For part 2 it is important to get the cards from `self.original_hand` (before replacing J-cards),
        # as J-cards are not treated as their replacement when breaking ties.
        return tuple(self.card_order.index(card) for card in self.original_hand)

    @property
    def rank(self) -> tuple:
        return (
            self.is_5oak,
            self.is_4oak,
            self.is_full_house,
            self.is_3oak,
            self.is_two_pair,
            self.is_one_pair,
            self.high_cards
        )

    def optimize_jokers(self) -> None:
        """ Finds the most common cards or most valuable single card and changes Jokers to that card. """
        counter_no_j = {card: count for card, count in Counter(self.hand).items() if card != "J"}
        # In the special case of all cards being Jokers, replace them with the best card 5 times
        if len(counter_no_j) == 0:
            self.hand = [self.card_order[-1]] * 5
            return
        # In all other cases it's optimal to convert to the most common card (higher rank, if tied).
        card, _ = max(counter_no_j.items(),
                      key=lambda count_tuple: (count_tuple[1], self.card_order.index(count_tuple[0])))
        self.hand = [(card if char == "J" else char) for char in self.hand]


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Part 1
    hands = [Hand(*line.strip().split()) for line in input_lines]
    ordered_hands = sorted(hands, key=lambda hand: hand.rank)
    wins_per_hand = (hand.bid * rank for rank, hand in enumerate(ordered_hands, start=1))
    print(f"Challenge 1: {sum(wins_per_hand)}")

    # Part 2
    hands = [Hand(*line.strip().split(), j_are_joker=True) for line in input_lines]
    ordered_hands = sorted(hands, key=lambda hand: hand.rank)
    wins_per_hand = (hand.bid * rank for rank, hand in enumerate(ordered_hands, start=1))
    print(f"Challenge 2: {sum(wins_per_hand)}")


if __name__ == '__main__':
    main()
