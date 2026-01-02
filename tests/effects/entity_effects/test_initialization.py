import random

import pytest

from Dinosaur_Venture import helper as h
from Dinosaur_Venture.cards.mechanics import card as c
from Dinosaur_Venture.cards.mechanics import card_tokens as tk
from Dinosaur_Venture.entities import entity as e
from Dinosaur_Venture.cards.mechanics.card_initalization_zones import CardInsertionPostion
from Dinosaur_Venture.cards.mechanics.card_location import CardZoneName

class test_arguments():
    """
    Contains all the arguments neccesary for testing. Utilized to make reading tests easier.
    """
    def __init__(
        self,
        muck_cards: int = 0,
        draw_cards: int = 0,
        top_cards: int = 0,
        bottom_cards: int = 0,
        pocket_cards: int = 0,
        discard_cards: int = 0
    ) -> None:
        self.muck_cards = muck_cards
        self.draw_cards = draw_cards
        self.top_cards = top_cards
        self.bottom_cards = bottom_cards
        self.pocket_cards = pocket_cards
        self.discard_cards = discard_cards

def run_test(test_arguments: test_arguments):
    """Runs the tests."""
    # Gets the caster
    caster: e.Entity = e.Entity()

    # Appends all cards to the deck
    for _ in range(test_arguments.draw_cards):
        card = c.Card()
        caster.deck.append(card)

    for _ in range(test_arguments.muck_cards):
        card = c.Card()
        card.publish_initialization_muck()
        caster.deck.append(card)
    
    for _ in range(test_arguments.top_cards):
        card = c.Card()
        card.publish_initialization_top()
        caster.deck.append(card)
    
    for _ in range(test_arguments.pocket_cards):
        card = c.Card()
        card.publish_initialization_pocket()
        caster.deck.append(card)

    # Does the initialization (moving cards to draw and shuffling accordingly)
    for card in caster.deck.getArray():
        caster.draw.append(card)

    caster.initializationShuffle()

    # Is the draw pile length correct?
    exected_draw_length = (
        test_arguments.bottom_cards + 
        test_arguments.top_cards + 
        test_arguments.draw_cards + 
        test_arguments.muck_cards
    )
    assert caster.draw.length() == exected_draw_length

    # Is our draw pile correctly ordered?
    draw_pile_counts = {
        CardInsertionPostion.TOP: test_arguments.top_cards,
        CardInsertionPostion.DRAW: test_arguments.draw_cards,
        CardInsertionPostion.MUCK: test_arguments.muck_cards,
        CardInsertionPostion.BOTTOM: test_arguments.bottom_cards
    }
    for index, card in enumerate(caster.draw.getArray()):
        # Do we expect any more top cards?
        if draw_pile_counts[CardInsertionPostion.TOP] != 0:
            assert card.initialized == CardInsertionPostion.TOP, str(index)
            draw_pile_counts[CardInsertionPostion.TOP] -= 1

        # Do we expect any more draw cards?
        elif draw_pile_counts[CardInsertionPostion.DRAW] != 0:
            assert card.initialized == CardInsertionPostion.DRAW, str(index)
            draw_pile_counts[CardInsertionPostion.DRAW] -= 1

        # Do we expect any more muck cards?
        elif draw_pile_counts[CardInsertionPostion.MUCK] != 0:
            assert card.initialized == CardInsertionPostion.MUCK, str(index)
            draw_pile_counts[CardInsertionPostion.MUCK] -= 1

        # Do we expect any more bottom cards?
        elif draw_pile_counts[CardInsertionPostion.BOTTOM] != 0:
            assert card.initialized == CardInsertionPostion.BOTTOM, str(index)
            draw_pile_counts[CardInsertionPostion.BOTTOM] -= 1

    # Is our pocket length correct?
    assert caster.pocket.length() == test_arguments.pocket_cards

    # Is our discard length correct?
    assert caster.discard.length() == test_arguments.discard_cards

@pytest.mark.parametrize(
    "test_arguments",
    [
        # Tests with different number of muck and draw-initialized cards
        test_arguments(
            muck_cards=1,
            draw_cards=0
        ),
        test_arguments(
            muck_cards=6,
            draw_cards=7
        ),
        # Tests with no muck cards
        test_arguments(
            draw_cards=20
        )
    ]
)
def test_initialized_muck(test_arguments: test_arguments):
    """
    Does initializing muck cards work correctly?
    """
    run_test(test_arguments)