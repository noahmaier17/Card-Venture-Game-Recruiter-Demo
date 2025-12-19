"""
check_card_location.py

Utilities for `helper.card_location`.
"""

from typing import Callable

from Dinosaur_Venture import card as c
from Dinosaur_Venture import card_tokens as tk
from Dinosaur_Venture import helper as h
from tests.test_utils.list_utilities import are_lists_exactly_equal

"""
Constants useful for checking ordering of cards.
"""
UPPERCASE_ALHPABET = [letter.upper() for letter in h.ALPHABET]
LOWERCASE_ALHPABET = [letter.lower() for letter in h.ALPHABET]
NUMBERS = [number for number in list(range(0, 24))]
NUMBERS_AS_STRINGS = [str(number) for number in NUMBERS]

def populate_card_location(count: int, card_location: "h.cardLocation", names_array: list, feathery_list_by_index=None):
    """
    Appends count-number of cards to the given card location, where the i-th card is named the i-th element of names_array.
    Does so in order.
    If feathery_list_by_index is present, entokens the i-th card with feathery if feathery_list_by_index[i] == true.
    """
    for i in range(count):
        new_card = c.Card()
        new_card.name = names_array[i]

        if feathery_list_by_index and feathery_list_by_index[i]:
            new_card.publishToken(tk.feathery())

        card_location.append(new_card)

def check_card_locations_unordered(
    card_location_1: h.cardLocation, 
    card_location_2: h.cardLocation, 
    comparison_parameter: Callable[[any], any]=None
) -> bool:
    """
    Checks if both input card locations have the same cards irregardless of order,
    essentially checking if the two sets are equal.
    """
    def sort_function(card):
        return card.name

    list_1 = card_location_1.getArray()
    list_2 = card_location_2.getArray()

    list_1.sort(key=sort_function)
    list_2.sort(key=sort_function)

    return are_lists_exactly_equal(list_1, list_2, comparison_parameter=comparison_parameter)