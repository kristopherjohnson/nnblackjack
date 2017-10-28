#!/usr/bin/env python3

"""
Generates basic strategy for every possible Blackjack deal.

Cards are represented by one-character symbols, where

- '2' - '9' are numbered cards
- 'T' is 10
- 'J' is Jack
- 'Q' is Queen
- 'K' is King
- 'A' is Ace

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
    'A' : 11, # or 1
}


HIT = "Hit"
STAND = "Stand"
SPLIT = "Split"
DOUBLE_OR_HIT = "DoubleH"
DOUBLE_OR_STAND = "DoubleS"
SURRENDER_OR_HIT = "Surrender"


def basic_strategy_action(card1, card2, dealer):
    """
    Return the best action for the given deal.

    Possible return values are

    - "Hit"
    - "Stand"
    - "DoubleH" (if Double not allowed, Hit)
    - "DoubleS" (if Double not allowed, Stand)
    - "Surrender" (if not allowed, Hit)
    """

    # Based on the chart at <https://en.m.wikipedia.org/wiki/Blackjack#Basic_strategy>,
    # which assumes
    #
    # - four to eight decks
    # - dealer hits on soft 17
    # - double allowed after a split
    # - only original bets are lost after dealer blackjack

    # If either player card is an Ace, make it card1.
    if card2 == 'A':
        card1, card2 = card2, card1

    card1_value = RANK_VALUE[card1]
    card2_value = RANK_VALUE[card2]
    dealer_value = RANK_VALUE[dealer]

    if card1 == card2:  # Pair

        if card1_value == 10:
            return STAND

        if card1_value == 9:
            return SPLIT if dealer_value in [2, 3, 4, 5, 6, 8, 9] else STAND

        if card1_value in [8, 11]:
            return SPLIT

        if card1_value in [2, 3, 7]:
            return SPLIT if dealer_value <= 7 else HIT

        if card1_value == 6:
            return SPLIT if dealer_value <= 6 else HIT

        if card1_value == 4:
            return SPLIT if dealer_value in [5, 6] else HIT

        # 5+5 falls through and is handled as Hard 10 below

    if card1 == 'A':  # Soft total

        if card2_value in [9, 10]:
            return STAND

        if card2_value == 8:
            return DOUBLE_OR_STAND if dealer_value == 6 else STAND

        if card2_value == 7:
            if dealer_value <= 6:
                return DOUBLE_OR_STAND
            elif dealer_value <= 8:
                return STAND
            else:
                return HIT

        if card2_value == 6:
            return DOUBLE_OR_HIT if 3 <= dealer_value <= 6 else HIT

        if card2_value in [4, 5]:
            return DOUBLE_OR_HIT if 4 <= dealer_value <= 6 else HIT

        # 2, 3
        return DOUBLE_OR_HIT if dealer_value in [5, 6] else HIT

    else:  # Hard total

        total = card1_value + card2_value

        if total >= 17:
            return STAND

        if total == 16:
            if dealer_value <= 6:
                return STAND
            elif dealer_value <= 8:
                return HIT
            else:
                return SURRENDER_OR_HIT

        if total == 15:
            if dealer_value <= 6:
                return STAND
            elif dealer_value == 10:
                return SURRENDER_OR_HIT
            else:
                return HIT

        if total in [13, 14]:
            return STAND if dealer_value <= 6 else HIT

        if total == 12:
            return STAND if 4 <= dealer_value <= 6 else HIT

        if total == 11:
            return DOUBLE_OR_HIT

        if total == 10:
            return DOUBLE_OR_HIT if dealer_value <= 9 else HIT

        if total == 9:
            return DOUBLE_OR_HIT if 3 <= dealer_value <= 6 else HIT

        # 5-8
        return HIT


def soft_total(card1, card2):
    """
    Returns the sum of the values of the two cards.

    In the case of two aces, returns 12.
    """
    if card1 == 'A' and card2 == 'A':
        return 12
    else:
        return RANK_VALUE[card1] + RANK_VALUE[card2]


def generate_basic_strategy_data():
    """
    Generates basic strategy actions for every possible Blackjack deal.

    Output is a sequence of dictionaries with keys
    "card1", "card2", "total", "hardness", "dealer", and "action".

    "card1" and "card2" are the cards dealt to the player.

    "total" is the sum of the values of player's cards.

    "hardness" is "Soft" if at least one of the cards is an Ace,
    or "Hard" otherwise.

    "dealer" is the dealer's face-up card.

    "action" is "Hit", "Stand", "Split", "DoubleH", "DoubleS" or "Surrender".
    """
    return ({ "card1"    : card1,
              "card2"    : card2,
              "total"    : soft_total(card1, card2),
              "hardness" : "Soft" if card1 == 'A' or card2 == 'A' else "Hard",
              "dealer"   : dealer,
              "action"   : basic_strategy_action(card1, card2, dealer)
            } for card1 in RANKS for card2 in RANKS for dealer in RANKS) 


if __name__ == "__main__":
    for deal in generate_basic_strategy_data():
        print("{card1}-{card2} ({hardness} {total}) {dealer} {action}".format(**deal))


