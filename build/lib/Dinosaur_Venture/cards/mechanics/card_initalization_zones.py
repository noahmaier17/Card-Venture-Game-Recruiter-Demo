"""
card_initalization_zones.py

Contains the key-value pairs of strings representing intialization zones
to their actual text.
"""

from enum import Enum

"""Hard-coded initialization locations."""
class CardInsertionPostion(Enum):
    BOTTOM = "Bottom"
    TOP = "Top"
    DISCARD = "Discard"
    INTO_HAND = "Into Hand"
    DRAW = "Draw"
    MUCK = "Muck"
    POCKET = "Pocket"

"""Global constant variable with no-space initialization zones (str) paired with their nicer, UI version (str)."""
INITIALIZATION_ZONES = {
    "iBottom": CardInsertionPostion.BOTTOM.value,
    "iTop": CardInsertionPostion.TOP.value,
    "iDiscard": CardInsertionPostion.DISCARD.value,
    "iInto_Hand": CardInsertionPostion.INTO_HAND.value,
    "iDraw": CardInsertionPostion.DRAW.value,
    "iMuck": CardInsertionPostion.MUCK.value,
    "iPocket": CardInsertionPostion.POCKET.value
}

"""Global constant variable which reverses the order of the INITIALIZION_ZONES key-value pairings."""
REVERSED_INITIALIZATION_ZONES = {}
for key in INITIALIZATION_ZONES.keys():
    REVERSED_INITIALIZATION_ZONES.update({INITIALIZATION_ZONES[key]: key})

assert isinstance(REVERSED_INITIALIZATION_ZONES.get("Bottom"), str)