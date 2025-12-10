"""
card_initalization_zones.py

Contains the key-value pairs of strings representing intialization zones
to their actual text.
"""

"""Global constant variable with no-space initialization zones paired with their nicer, UI version."""
INITIALIZATION_ZONES = {
    "iBottom": "Bottom",
    "iTop": "Top",
    "iDiscard": "Discard",
    "iInto_Hand": "Into Hand",
    "iDraw": "Draw",
    "iMuck": "Muck",
    "iPocket": "Pocket"
}

"""Global constant variable which reverses the order of the INITIALIZION_ZONES key-value pairings."""
REVERSED_INITIALIZATION_ZONES = {}
for key in INITIALIZATION_ZONES.keys():
    REVERSED_INITIALIZATION_ZONES.update({INITIALIZATION_ZONES[key]: key})