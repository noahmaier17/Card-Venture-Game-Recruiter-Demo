"""
upcoming_list_utilities.py

Test utilities for checking state of attributes like entity.plusUpcomingActions.
"""
from typing import Callable


def are_upcoming_lists_equal(list_1: list, list_2: list, comparison_parameter: Callable[[any], any]=None):
    """
    Tests if list_1 and list_2 have equal values. 
    
    If lists are not of the same length, populates the shorter list with additional 0 entries.

    comparison_paramter (function) is a function to call on each element of the list to test if they are equal.
    For instance, if we have comparison_paramter(card): return card.name, we will test equality based on card name.
    If None, tests based on if two objects are equal.
    """
    if len(list_1) == 0 and len(list_2) == 0:
        return True
    
    if len(list_1) == 0:
        list_1.append(0)
    
    if len(list_2) == 0:
        list_2.append(0)

    if comparison_parameter and comparison_parameter(list_1[0]) != comparison_parameter(list_2[0]):
        return False
    elif list_1[0] != list_2[0]:
        return False
    
    return are_upcoming_lists_equal(list_1[1:], list_2[2:], comparison_parameter=comparison_parameter)

def default_name_comparison_parameter(card):
    """Possible default parameter for `are_lists_exactly_equal` to compare cards by name."""
    return card.name

def are_lists_exactly_equal(list_1: list, list_2: list, comparison_parameter: Callable[[any], any]=None):
    """
    Tests if list_1 and list_2 are exactly equal. 

    comparison_paramter (function) is a function to call on each element of the list to test if they are equal.
    For instance, if we have comparison_paramter(card): return card.name, we will test equality based on card name.
    If None, tests based on if two objects are equal.    
    """
    if len(list_1) == 0 and len(list_2) == 0:
        return True
    
    if len(list_1) != len(list_2):
        return False
    
    if comparison_parameter and comparison_parameter(list_1[0]) != comparison_parameter(list_2[0]):
        return False
    elif not comparison_parameter and list_1[0] != list_2[0]:
        return False
    
    return are_lists_exactly_equal(list_1[1:], list_2[1:], comparison_parameter=comparison_parameter)
