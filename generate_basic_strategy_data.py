#!/usr/bin/env python3

"""
Generates comma-separated values for every possible Blackjack deal.

First two values are cards dealt to the player.

Third value is the dealier's up card.

Fourth value is "Hit", "Stand", "Split", or "Double".

Cards are represented by one-character symbols, where

- 'T' is 10
- 'J' is Jack
- 'Q' is Queen
- 'K' is King
- 'A' is Ace
- '2' - '9' are numbered cards

"""


RANKS = [ '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A' ]

RANK_VALUE = {
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    'T' : 10,
    'J' : 10,
    'Q' : 10,
    'K' : 10,
    'A' : 11,
}


HIT = "Hit"
STAND = "Stand"
SPLIT = "Split"
DOUBLE = "Double"


def basic_strategy_action(deal):
    """
    Return the best action ("Hit", "Stand", "Split", or "Double") for the given deal.
    """

    # See <https://www.cs.bu.edu/~hwxi/academic/courses/CS320/Spring02/assignments/06/basic-strategy.html>

    card1 = deal[0]
    card2 = deal[1]
    dealer = deal[2]

    # If either card is an Ace, make it card1.
    if card2 == 'A':
        card1, card2 = card2, card1

    card1_value = RANK_VALUE[card1]
    card2_value = RANK_VALUE[card2]
    dealer_value = RANK_VALUE[dealer]

    if card1 == card2:  # Split?

        if card1_value == 10:
            return STAND

        if card1 == 'A' or card1_value == 8:
            return SPLIT

        if card1_value == 2 or card1_value == 3 or card1_value == 7:
            if 2 <= dealer_value <= 7:
                return SPLIT
            else:
                return HIT

        if card1_value == 4:
            if dealer_value == 5 or dealer_value == 6:
                return SPLIT
            else:
                return HIT

        if card1_value == 6:
            if 2 <= dealer_value <= 6:
                return SPLIT
            else:
                return HIT

        if card1_value == 9:
            if 2 <= dealer_value <= 6 or dealer_value == 8 or dealer_value == 9:
                return SPLIT
            else:
                return HIT

        # Note: 5,5 will be handled as 10 below

    if card1 == 'A':  # One ace

        if card2_value == 2 or card2_value == 3:
            if dealer_value == 5 or dealer_value == 6:
                return DOUBLE
            else:
                return HIT

        if card2_value == 4 or card2_value == 5:
            if 4 <= dealer_value <= 6:
                return DOUBLE
            else:
                return HIT

        if card2_value == 6:
            if 3 <= dealer_value <= 6:
                return DOUBLE
            else:
                return HIT

        if card2_value == 7:
            if 3 <= dealer_value <= 6:
                return DOUBLE
            elif 9 <= dealer_value:
                return HIT
            else:
                return STAND

        return STAND

    else: # No ace

        total = card1_value + card2_value

        if total <= 8:
            return HIT

        if total == 9:
            if 3 <= dealer_value <= 6:
                return DOUBLE
            else:
                return HIT

        if total == 10:
            if dealer_value <= 9:
                return DOUBLE
            else:
                return HIT

        if total == 11:
            if dealer_value <= 10:
                return DOUBLE
            else:
                return HIT

        if total == 12:
            if 4 <= dealer_value <= 6:
                return STAND
            else:
                return HIT

        if 13 <= total <= 16:
            if 2 <= dealer_value <= 6:
                return STAND
            else:
                return HIT

        return STAND


def generate_basic_strategy_data():
    """
    Generates CSV records of basic strategy for every possible Blackjack deal.

    First two values are cards dealt to the player.

    Third value is the dealer's up card.

    Fourth value is "Hit", "Stand", "Split", or "Double".
    """
    for deal in [(card1, card2, dealer) for card1 in RANKS for card2 in RANKS for dealer in RANKS]:
        action = basic_strategy_action(deal)
        print(f"{deal[0]},{deal[1]},{deal[2]},{action}")


if __name__ == "__main__":
    generate_basic_strategy_data()


