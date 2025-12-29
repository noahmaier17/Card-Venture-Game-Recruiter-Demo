"""
test_draw_to_x_in_hand.py

Tests drawing to X cards in hand.
Does not perform any tests on ordering of card locations after drawing. Such behavior should be fairly thouroughly tested
with the test_draw_cards.py test cases.
"""

import pytest

from Dinosaur_Venture.cards.mechanics import card as c
from Dinosaur_Venture.cards.mechanics.card_functions import \
    drawUntilYouHaveXCardsInHand
from Dinosaur_Venture.entities import entity as e
from Dinosaur_Venture.main_visuals import prefabEmpty
from tests.test_utils import card_location_utilities
from tests.test_utils.game_setups import getSingleSliceOfDinoEnemiesClearing

# We just need some arbitrary single instance of these classes
DINO, ENEMIES, CLEARING = getSingleSliceOfDinoEnemiesClearing()

@pytest.mark.parametrize(
    "cards_in_hand, cards_in_draw, cards_in_discard, draw_to_x_value, expected_hand_size, expected_draw_size, expected_discard_size",
    [
        (0, 0, 0, 1, 0, 0, 0),      # Drawing to X without any cards to draw
        (0, 0, 0, 10, 0, 0, 0),
        (5, 9, 0, 9, 9, 5, 0),      # Drawing through part of our draw pile
        (0, 3, 9, 3, 3, 0, 9),      # Drawing through all of the draw pile
        (0, 0, 8, 4, 4, 4, 0),      # Drawing by triggering a shuffle
        (2, 2, 2, 5, 5, 1, 0),
        (1, 1, 0, 5, 2, 0, 0)       # Drawing to 5 with only 1 card to draw (and 1 in hand)
    ]
)
def test_drawToXInHand(
    cards_in_hand, 
    cards_in_draw,
    cards_in_discard, 
    draw_to_x_value, 
    expected_hand_size, 
    expected_draw_size, 
    expected_discard_size
):
    """
    Does draw to X work as expected?
    """
    # We need to create a caster
    caster: e.Entity = e.Entity()

    # Hand will have lowercase letter'd names, draw will have uppercase letter'd names, and discard will have numeric names.
    # Hand and draw will be ordered from A to Z to test correct sequencing (not currently implemented).
    # Discard is an unordered card location.

    # Does that aforementioned populating
    card_location_utilities.populate_card_location(cards_in_hand, caster.hand, card_location_utilities.LOWERCASE_ALHPABET)
    card_location_utilities.populate_card_location(cards_in_draw, caster.draw, card_location_utilities.UPPERCASE_ALHPABET)
    card_location_utilities.populate_card_location(cards_in_discard, caster.discard, card_location_utilities.NUMBERS_AS_STRINGS)

    # As of right now, our "card", dino, enemies, and passedInVisuals are not important.
    # If we were to later implement a card_mod_function, we will still pass in burner values to these.
    drawUntilYouHaveXCardsInHand(draw_to_x_value).func(c.Card(), caster, DINO, ENEMIES, prefabEmpty())

    # Is the size of our hand as expected?
    assert caster.hand.length() == expected_hand_size

    # Is the size of our draw as expected?
    assert caster.draw.length() == expected_draw_size

    # Is the size of our discard as expected?
    assert caster.discard.length() == expected_discard_size

class test_attributes():
    """Parameterization attributes."""
    def __init__(
        self,
        list_of_hand_feathered_cards: list[bool],
        list_of_draw_feathered_cards: list[bool],
        list_of_discard_feathered_cards: list[bool],
        draw_to_x_value,
        expected_hand_size,
        expected_draw_size,
        expected_discard_size
    ):
        self.list_of_hand_feathered_cards = list_of_hand_feathered_cards
        self.list_of_draw_feathered_cards = list_of_draw_feathered_cards
        self.list_of_discard_feathered_cards = list_of_discard_feathered_cards
        self.draw_to_x_value = draw_to_x_value
        self.expected_hand_size = expected_hand_size
        self.expected_draw_size = expected_draw_size
        self.expected_discard_size = expected_discard_size
    
@pytest.mark.parametrize(
    "test_attributes",
    [
        # Draws feathery cards from draw
        test_attributes(
            list_of_hand_feathered_cards=[False, False, True, True],
            list_of_draw_feathered_cards=[False, True, False, True, False, True, False, True, False, True, False, True],
            list_of_discard_feathered_cards=[],
            draw_to_x_value=5,
            expected_hand_size=9,
            expected_draw_size=7,
            expected_discard_size=0
        ),
        # Draws feathery cards from draw with a non-empty discard (no cards from discard are drawn however)
        test_attributes(
            list_of_hand_feathered_cards=[],
            list_of_draw_feathered_cards=[True, True, False, False, True, True, False, False],
            list_of_discard_feathered_cards=[True, False, True, True, False, False, True, False, False, True, True],
            draw_to_x_value=3,
            expected_hand_size=7,
            expected_draw_size=1,
            expected_discard_size=11
        ),
        # Draws feathery cards from draw, AND normal cards from discard
        test_attributes(
            list_of_hand_feathered_cards=[True],
            list_of_draw_feathered_cards=[False, False, False, True, True, True],
            list_of_discard_feathered_cards=[False, False, False, False],
            draw_to_x_value=4,
            expected_hand_size=8,
            expected_draw_size=3,
            expected_discard_size=0
        ),
        # Draws feathery cards from draw AND from discard
        # Draws all of discard, since we do not have deterministic shuffling and cannot guess
        # how many cards will remain in our draw pile
        test_attributes(
            list_of_hand_feathered_cards=[True],
            list_of_draw_feathered_cards=[True, True, True],
            list_of_discard_feathered_cards=[True, True, True, True],
            draw_to_x_value=1,
            expected_hand_size=8,
            expected_draw_size=0,
            expected_discard_size=0
        )
    ]
)
def test_drawToXInHand_withFeatheryCards(
    test_attributes: test_attributes
):
    """
    Does draw to X work as expected including with <<feathery>> cards?
    """
    # We need to create a caster
    caster: e.Entity = e.Entity()

    # Hand will have lowercase letter'd names, draw will have uppercase letter'd names, and discard will have numeric names.
    # Hand and draw will be ordered from A to Z to test correct sequencing.
    # Discard is an unordered card location.

    # Does that aforementioned populating
    card_location_utilities.populate_card_location(
        len(test_attributes.list_of_hand_feathered_cards), 
        caster.hand,
        card_location_utilities.LOWERCASE_ALHPABET,
        feathery_list_by_index=test_attributes.list_of_hand_feathered_cards
    )
    card_location_utilities.populate_card_location(
        len(test_attributes.list_of_draw_feathered_cards), 
        caster.draw, 
        card_location_utilities.UPPERCASE_ALHPABET,
        feathery_list_by_index=test_attributes.list_of_draw_feathered_cards
    )
    card_location_utilities.populate_card_location(
        len(test_attributes.list_of_discard_feathered_cards), 
        caster.discard, 
        card_location_utilities.NUMBERS_AS_STRINGS,
        feathery_list_by_index=test_attributes.list_of_discard_feathered_cards
    )

    # As of right now, our "card", dino, enemies, and passedInVisuals are not important.
    # If we were to later implement a card_mod_function, we will still pass in burner values to these.
    drawUntilYouHaveXCardsInHand(test_attributes.draw_to_x_value).func(c.Card(), caster, DINO, ENEMIES, prefabEmpty())

    # Is the size of our hand as expected?
    assert caster.hand.length() == test_attributes.expected_hand_size

    # Is the size of our draw as expected?
    assert caster.draw.length() == test_attributes.expected_draw_size

    # Is the size of our discard as expected?
    assert caster.discard.length() == test_attributes.expected_discard_size