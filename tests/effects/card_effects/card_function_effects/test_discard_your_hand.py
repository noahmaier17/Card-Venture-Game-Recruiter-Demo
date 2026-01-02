import pytest

from Dinosaur_Venture import helper as h
from Dinosaur_Venture.cards.mechanics import card as c
from Dinosaur_Venture.cards.mechanics import card_location
from Dinosaur_Venture.cards.mechanics.card_functions import discardYourHand
from Dinosaur_Venture.entities import entity as e
from Dinosaur_Venture.main_visuals import prefabEmpty
from tests.test_utils.card_location_utilities import \
    check_card_locations_unordered
from tests.test_utils.game_setups import getSingleSliceOfDinoEnemiesClearing

# We just need some arbitrary single instance of these classes
DINO, ENEMIES, CLEARING = getSingleSliceOfDinoEnemiesClearing()

class test_arguments():
    """
    Contains all the arguments neccesary for testing. Utilized to make reading tests easier.
    """
    def __init__(
        self,
        hand_size: int = 0,
        discard_size: int = 0
    ) -> None:
        self.hand_size = hand_size
        self.discard_size = discard_size

def run_test(test_arguments: test_arguments):
    """Runs the tests."""
    # Creates an entity
    caster: e.Entity = e.Entity()

    # Puts cards into its hand
    starting_hand_cards: card_location.CardLocation = card_location.CardLocation("starting hand")
    for _ in range(test_arguments.hand_size):
        card: c.Card = c.Card()
        starting_hand_cards.append(card)
        caster.hand.append(card)

    # And puts cards into its discard pile
    starting_discard_cards: card_location.CardLocation = card_location.CardLocation("starting discard")
    for _ in range(test_arguments.discard_size):
        card: c.Card = c.Card()
        starting_discard_cards.append(card)
        caster.discard.append(card)
    
    # Runs the card function
    # As of right now, our "card", dino, enemies, and passedInVisuals are not important.
    discardYourHand().func(c.Card(), caster, DINO, ENEMIES, prefabEmpty())

    # Is our hand now empty?
    assert caster.hand.length() == 0

    # Is our discard now the size of hand + original discard?
    assert caster.discard.length() == test_arguments.discard_size + test_arguments.hand_size

    # Are all cards in discard that of which we expect?
    expected_discard_location = h.unionCardLocations(starting_hand_cards, starting_discard_cards)
    assert check_card_locations_unordered(expected_discard_location, caster.discard)

@pytest.mark.parametrize(
    "test_arguments",
    [
        test_arguments(
            hand_size=0,
            discard_size=0
        ),
        test_arguments(
            hand_size=5,
            discard_size=0
        ),
        test_arguments(
            hand_size=4,
            discard_size=7
        ),        
        test_arguments(
            hand_size=0,
            discard_size=8
        )
    ]
)
def test_discardYourHand(test_arguments: test_arguments):
    """Does the discard your hand card function work as expected?"""
    run_test(test_arguments)