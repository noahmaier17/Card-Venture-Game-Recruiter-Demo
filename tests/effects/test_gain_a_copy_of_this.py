import pytest
import pytest_timeout
import random
import copy

from Dinosaur_Venture.entities import dinoes as dinoes_import
from Dinosaur_Venture import card as c
from Dinosaur_Venture import helper as h
from tests.test_utils.check_card_location import check_card_locations_unordered


@pytest.mark.timeout(5)
def test_gainACopyOfThis():
    dino = dinoes_import.Dinosaur()

    # Populates dino's deck with several non-important cards, and gets a list to compare against
    comparison_original_card_location = h.cardLocation("comparison list")
    comparison_after_copy_card_location = h.cardLocation("after comparison list")
    for letter in h.ALPHABET:
        new_card = c.Card()
        new_card.name = letter

        dino.deck.append(new_card)
        comparison_original_card_location.append(new_card)
        comparison_after_copy_card_location.append(new_card)

    # Checks if the state of dino's deck is correct
    assert check_card_locations_unordered(dino.deck, comparison_original_card_location)

    # Has dino gain a copy of a random card in deck
    card_to_copy = dino.deck.getArray()[random.randint(0, dino.deck.length() - 1)]
    dino.gainCopyOfCard(card_to_copy, dino.deck)

    # Checks if dino's deck state is no longer that of the original
    assert not check_card_locations_unordered(dino.deck, comparison_original_card_location)

    # Checks if dino has 2 of the same cards (checking by name)
    instances = 0
    for card in dino.deck.getArray():
        if card.name == card_to_copy.name:
            instances += 1

    assert instances == 2

    # If we add this copied card to a card location, do dino's deck and that list have the same values
    comparison_after_copy_card_location.append(card_to_copy)
    print(dino.deck.getArray())
    print(comparison_after_copy_card_location.getArray())

    def comparison_parameter(card):
        return card.name

    assert check_card_locations_unordered(dino.deck, comparison_after_copy_card_location, comparison_parameter=comparison_parameter)