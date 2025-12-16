"""
check_card_location.py

Checks if the content of a `helper.card_location` is accurate.
"""

from typing import Callable

from Dinosaur_Venture import helper as h
from tests.test_utils.list_utilities import are_lists_exactly_equal


def check_card_locations_unordered(
    card_location_1: h.cardLocation, 
    card_location_2: h.cardLocation, 
    comparison_parameter: Callable[[any], any]=None
) -> bool:
    def sort_function(card):
        return card.name

    list_1 = card_location_1.getArray()
    list_2 = card_location_2.getArray()

    list_1.sort(key=sort_function)
    list_2.sort(key=sort_function)

    return are_lists_exactly_equal(list_1, list_2, comparison_parameter=comparison_parameter)