import random
from typing import TYPE_CHECKING

import pytest

from Dinosaur_Venture import card as c
from Dinosaur_Venture import card_tokens as tk
from Dinosaur_Venture.entities import entity as e
from tests.test_utils import card_location_utilities, list_utilities
from Dinosaur_Venture.logging import gameplay_logging as log

from Dinosaur_Venture import helper as h


class test_arguments():
    """
    Contains all the arguments neccesary for testing. Utilized to make reading tests easier.
    All parameters default to 0.
    """
    def __init__(
        self,
        plus_cards_count: int=0,
        hand_size: int=0,
        draw_size: int=0,
        discard_size: int=0,
        expected_hand_size: int=0,
        expected_draw_size: int=0,
        expected_discard_size: int=0,
        from_location: str = e.Entity.DEFAULT_CARD_LOCATION,
        to_location: str = e.Entity.DEFAULT_CARD_LOCATION,
        shuffle_location: str = e.Entity.DEFAULT_CARD_LOCATION,
        from_location_length: int=None,     # Only important if we have an alternative from location
        to_location_length: int=None,       # Only important if we have an alternative to location
        shuffle_location_length: int=None,  # Only important if we have an alternative shuffle location
        
    ) -> None:
        self.plus_cards_count = plus_cards_count
        self.hand_size = hand_size
        self.draw_size = draw_size
        self.discard_size = discard_size
        self.expected_hand_size = expected_hand_size
        self.expected_draw_size = expected_draw_size
        self.expected_discard_size = expected_discard_size
        self.from_location = from_location
        self.to_location = to_location
        self.shuffle_location = shuffle_location
        self.from_location_length = from_location_length
        self.to_location_length = to_location_length
        self.shuffle_location_length = shuffle_location_length

def run_test(test_arguments: test_arguments, randomly_entoken_with_feathery=False):
    """Runs the drawing cards tests."""
    # We need to create a caster
    caster: e.Entity = e.Entity()

    # Hand will have lowercase letter'd names, draw will have uppercase letter'd names, and discard will have numeric names.
    # Hand and draw will be ordered from A to Z to test correct sequencing.
    # Discard is an unordered card location.

    # Does that aforementioned populating
    card_location_utilities.populate_card_location(
        test_arguments.hand_size, 
        caster.hand,
        card_location_utilities.LOWERCASE_ALHPABET
    )
    card_location_utilities.populate_card_location(
        test_arguments.draw_size,
        caster.draw, 
        card_location_utilities.UPPERCASE_ALHPABET
    )
    card_location_utilities.populate_card_location(
        test_arguments.discard_size, 
        caster.discard, 
        card_location_utilities.NUMBERS_AS_STRINGS
    )

    # if randomly_entoken_with_feathery == True, we will entoken cards in all of these lists randomly
    for card in caster.hand.getArray() + caster.draw.getArray() + caster.discard.getArray():
        if random.random() <= 0.75:
            card.publishToken(tk.feathery())

    # Does the drawing
    if test_arguments.to_location != e.Entity.DEFAULT_CARD_LOCATION:
        test_arguments.to_location = caster.fetchLocationByConstant(test_arguments.to_location)

    if test_arguments.from_location != e.Entity.DEFAULT_CARD_LOCATION:
        test_arguments.from_location = caster.fetchLocationByConstant(test_arguments.from_location)

    if test_arguments.shuffle_location != e.Entity.DEFAULT_CARD_LOCATION:
        test_arguments.shuffle_location = caster.fetchLocationByConstant(test_arguments.shuffle_location)

    for _ in range(test_arguments.plus_cards_count):
        caster.drawCard(
            fromLocation=test_arguments.from_location,
            toLocation=test_arguments.to_location,
            shuffleLocation=test_arguments.shuffle_location
        )

    # Is the size of our hand as expected?
    assert caster.hand.length() == test_arguments.expected_hand_size

    # Is the size of our draw as expected?
    assert caster.draw.length() == test_arguments.expected_draw_size

    # Is the size of our discard as expected?
    assert caster.discard.length() == test_arguments.expected_discard_size

    # Is our draw still ordered correctly?

    # Did we trigger a shuffle? 
    # If we did not trigger a shuffle, our draw pile should be our orignal draw pile 
    # missing the first plus_card_count number of cards.
    if test_arguments.plus_cards_count <= test_arguments.draw_size:
        # Creates an ordered list of our expected cards
        expected_draw_list = []

        # Did we draw more 
        for i in range(test_arguments.plus_cards_count, test_arguments.draw_size):
            card = c.Card()
            card.name = card_location_utilities.UPPERCASE_ALHPABET[i]
            expected_draw_list.append(card)

        def comparison_parameter(card):
            return card.name

        # Do these lists match?
        assert list_utilities.are_lists_exactly_equal(
            caster.draw.getArray(), 
            expected_draw_list,
            comparison_parameter=comparison_parameter
        )

    # If we did trigger a shuffle, our draw pile should be an unordered subset of our original discard pile.
    else:
        # Creates an unordered list of all possible expected cards
        card_location_utilities.populate_card_location(
            test_arguments.discard_size, 
            caster.discard, 
            card_location_utilities.NUMBERS_AS_STRINGS
        )

        # Since our discard pile had only numeric cards, is our draw pile exclusively numeric?
        for card in caster.draw.getArray():
            assert card.name.isnumeric()

    # Is the size of this alternative to location the correct length?
    if test_arguments.to_location != e.Entity.DEFAULT_CARD_LOCATION:
        assert test_arguments.to_location.length() == test_arguments.to_location_length

    # Is the size of this alternative from location the correct length?
    if test_arguments.from_location != e.Entity.DEFAULT_CARD_LOCATION:
        assert test_arguments.to_location.length() == test_arguments.from_location_length

    # Is the size of this alternative shuffle location the correct length?
    if test_arguments.shuffle_location != e.Entity.DEFAULT_CARD_LOCATION:
        assert test_arguments.shuffle_location.length() == test_arguments.shuffle_location_length

@pytest.mark.parametrize(
    "test_arguments",
    [
        # Draws less than draw pile size 
        test_arguments(
            plus_cards_count=1,
            draw_size=3,
            expected_hand_size=1,
            expected_draw_size=2
        ),
        # Draws the draw pile with no cards in discard
        test_arguments(
            plus_cards_count=2,
            draw_size=2,
            expected_hand_size=2
        ),
        # Draws the draw pile with cards in discard
        test_arguments(
            plus_cards_count=3,
            draw_size=3,
            expected_hand_size=3
        ),
        # Does the same aforementioned tests with cards already in hand
        test_arguments(
            plus_cards_count=1,
            hand_size=2,
            draw_size=3,
            expected_hand_size=3,
            expected_draw_size=2
        ),
        test_arguments(
            plus_cards_count=2,
            hand_size=20,
            draw_size=2,
            expected_hand_size=22
        ),
        test_arguments(
            plus_cards_count=3,
            hand_size=1,
            draw_size=3,
            expected_hand_size=4
        ),
        # Draws only some of draw pile to test draw pile ordering 
        test_arguments(
            plus_cards_count=1,
            draw_size=10,
            expected_hand_size=1,
            expected_draw_size=9
        ),
        # Draws more cards than cards available with an empty discard
        test_arguments(
            plus_cards_count=50,
            hand_size=2,
            draw_size=5,
            expected_hand_size=7
        )
    ]
)
def test_draw_cards_from_draw(test_arguments: test_arguments):
    """
    Does drawing cards work correctly, exclusively looking at drawing from the draw pile?

    Also checks if the discard pile is correctly left alone when drawing from the draw pile.
    """
    run_test(test_arguments)

@pytest.mark.parametrize(
    "test_arguments",
    [
        # Draws past the draw AND discard pile
        test_arguments(
            plus_cards_count=100,
            draw_size=5,
            discard_size=6,
            hand_size=7,
            expected_hand_size=18
        ),
        # Draws the entire draw pile and only part of the discard pile
        test_arguments(
            plus_cards_count=4,
            hand_size=1,
            draw_size=1,
            discard_size=20,
            expected_hand_size=5,
            expected_draw_size=17
        ),
        # Again, draws the entire draw pile and only part of the discard pile
        test_arguments(
            plus_cards_count=3,
            discard_size=4,
            expected_hand_size=3,
            expected_draw_size=1
        ),
        # Draws exactly the draw and discard pile
        test_arguments(
            plus_cards_count=6,
            hand_size=16,
            draw_size=3,
            discard_size=3,
            expected_hand_size=22
        )
    ]
)
def test_draw_cards_from_draw_then_discard(test_arguments: test_arguments):
    """
    Does drawing cards work correctly, exclusively looking at drawing through the draw pile, 
    triggering a shuffle, and then drawing through the new draw pile?
    """
    run_test(test_arguments)

@pytest.mark.parametrize(
    "test_arguments",
    [
        # Draws less than draw pile size 
        test_arguments(
            plus_cards_count=1,
            draw_size=3,
            expected_hand_size=1,
            expected_draw_size=2
        ),
        # Draws the draw pile with no cards in discard
        test_arguments(
            plus_cards_count=2,
            draw_size=2,
            expected_hand_size=2
        ),
        # Draws the draw pile with cards in discard
        test_arguments(
            plus_cards_count=3,
            draw_size=3,
            expected_hand_size=3
        ),
        # Does the same aforementioned tests with cards already in hand
        test_arguments(
            plus_cards_count=1,
            hand_size=2,
            draw_size=3,
            expected_hand_size=3,
            expected_draw_size=2
        ),
        # Draws past the draw AND discard pile
        test_arguments(
            plus_cards_count=100,
            draw_size=5,
            discard_size=6,
            hand_size=7,
            expected_hand_size=18
        ),
        # Draws the entire draw pile and only part of the discard pile
        test_arguments(
            plus_cards_count=4,
            hand_size=1,
            draw_size=1,
            discard_size=20,
            expected_hand_size=5,
            expected_draw_size=17
        ),
        # Again, draws the entire draw pile and only part of the discard pile
        test_arguments(
            plus_cards_count=3,
            discard_size=4,
            expected_hand_size=3,
            expected_draw_size=1
        ),
        # Draws exactly the draw and discard pile
        test_arguments(
            plus_cards_count=6,
            hand_size=16,
            draw_size=3,
            discard_size=3,
            expected_hand_size=22
        )
    ]
)
def test_draw_cards_ignoring_feathery_cards(test_arguments: test_arguments):
    """
    Does drawing cards work correctly and ignore <<feathery>> cards?

    This is very unlikely to be bugged, so randomly testing this functionality is fine.
    """
    # Since all feathery cards are not important for + Cards, we will make a random
    # assortment of cards feathery and run tests
    run_test(test_arguments, randomly_entoken_with_feathery=True)

@pytest.mark.parametrize(
    "test_arguments",
    [
        # Draws a card to the into-hand mat
        test_arguments(
            plus_cards_count=1,
            draw_size=3,
            expected_draw_size=2,
            to_location=h.CARD_LOCATION_INTO_HAND,
            to_location_length=1
        ),
        # Draws a card to the play mat
        test_arguments(
            plus_cards_count=8,
            draw_size=2,
            discard_size=3,
            to_location=h.CARD_LOCATION_PLAY,
            to_location_length=5
        ),
        # Fails to draw a card to the discard mat (no cards to draw)
        test_arguments(
            plus_cards_count=16,
            to_location=h.CARD_LOCATION_DISCARD,
            to_location_length=0
        )
    ]
)
def test_draw_to_alternative_location(test_arguments: test_arguments):
    """
    Does drawing cards to a different to location work correctly?
    """
    run_test(test_arguments)