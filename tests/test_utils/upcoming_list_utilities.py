"""
upcoming_list_utilities.py

Test utilities for checking state of attributes like entity.plusUpcomingActions.
"""

def are_upcoming_lists_equal(list_1: list, list_2: list):
    """
    Tests if list_1 and list_2 have equal values. 
    
    If lists are not of the same length, populates the shorter list with additional 0 entries.
    """
    if len(list_1) == 0 and len(list_2) == 0:
        return True
    
    if len(list_1) == 0:
        list_1.append(0)
    
    if len(list_2) == 0:
        list_2.append(0)

    if list_1[0] != list_2[0]:
        return False
    
    return are_upcoming_lists_equal(list_1[1:], list_2[2:])