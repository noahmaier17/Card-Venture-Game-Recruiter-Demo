from Dinosaur_Venture import helper as h
from Dinosaur_Venture.cards.mechanics.card_location import CardLocation
from Dinosaur_Venture.dinosaur_venture import code

## ----- Debugging Values ----
## For all booleans, the non-debugging value is False

# For debugging, if we want to increase/decrease the difficulty
# Non-debugging value: 0
DIFFICULTY_DEBUG_BONUS = 0

# For debugging, if we want to loot more cards at a Rest Stop
# Non-debugging value: 4
NUMBER_OF_CARDS_TO_LOOT = 4

## If we will loot round 1; useful for faster testing speed
## BUGGY; needs to also override the `clearing` parameter in order to work
DO_ROUND_1_LOOTING = False

# To replace all of dino's deck with nothing
NUKE_DINO_DECK = False

# To replace dino's deck with the special debugging deck
# See dinosaur_venture.py file to determine the contents of this debug deck (line ~140)
DEBUG_DINO_DECK = True

# Skips every shop for the purpose of debugging; useful for faster testing speed
SKIP_SHOP_DEBUG = True

# Only loot shells
LOOT_SHELLS_ONLY = False

# Skip picking clearings; useful for faster testing speed
SKIP_PICKING_CLEARINGS = True

# Logic to force picking a specific clearing; potentially a future feature
DEBUG_PICK_GUARENTEED_NECK_OF_THE_WOODS = True

# To replace the shop cards, uncomment the following and add cards as you please
OVERRIDE_SHOP_LOCATION = None
# '''
OVERRIDE_SHOP_LOCATION = CardLocation("override-shop-location")

from Dinosaur_Venture.cards.depot.dino_cards import shop_cards

for card in [shop_cards.test01()]: OVERRIDE_SHOP_LOCATION.append(card)
# '''

# Runs the code in this debugging state
code(
    DIFFICULTY_DEBUG_BONUS=DIFFICULTY_DEBUG_BONUS,
    NUMBER_OF_CARDS_TO_LOOT=NUMBER_OF_CARDS_TO_LOOT,
    DO_ROUND_1_LOOTING=DO_ROUND_1_LOOTING,
    NUKE_DINO_DECK=NUKE_DINO_DECK,
    DEBUG_DINO_DECK=DEBUG_DINO_DECK,
    SKIP_SHOP_DEBUG=SKIP_SHOP_DEBUG,
    LOOT_SHELLS_ONLY=LOOT_SHELLS_ONLY,
    SKIP_PICKING_CLEARINGS=SKIP_PICKING_CLEARINGS,
    DEBUG_PICK_GUARENTEED_NECK_OF_THE_WOODS=DEBUG_PICK_GUARENTEED_NECK_OF_THE_WOODS,
    OVERRIDE_SHOP_LOCATION=OVERRIDE_SHOP_LOCATION
)