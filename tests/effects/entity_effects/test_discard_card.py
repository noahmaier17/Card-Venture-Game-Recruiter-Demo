import pytest

from Dinosaur_Venture import main_visuals as vis
from Dinosaur_Venture.cards.mechanics.card_location import CardLocation
from Dinosaur_Venture.entities import entity as e
from tests.test_utils import card_location_utilities
from tests.test_utils.game_setups import getSingleSliceOfDinoEnemiesClearing


class test_arguments():
    """
    Contains all the arguments neccesary for testing. Utilized to make reading tests easier.
    All parameters default to 0.
    """
    def __init__(
        self,
        from_location_size: int = 0,
        discard_size: int = 0,
        expected_from_location_size: int = 0,
        expected_discard_size: int = 0,
        index_of_discarded_card: int = 0
    ) -> None:
        self.from_location_size = from_location_size
        self.discard_size = discard_size
        self.expected_from_location_size = expected_from_location_size
        self.expected_discard_size = expected_discard_size
        self.index_of_discarded_card = index_of_discarded_card

@pytest.mark.parametrize(
    "test_arguments",
    [
        # Discards a card
        test_arguments(
            from_location_size=1,
            discard_size=10,
            expected_discard_size=11,
            index_of_discarded_card=0
        ),
        test_arguments(
            from_location_size=10,
            expected_discard_size=1,
            expected_from_location_size=9,
            index_of_discarded_card=9
        )
    ]
)
def test_discard_card(test_arguments: test_arguments):
    """
    Does discarding cards work correctly?

    Discarding is essentially the same as moving, so we do not require too many tests.
    """
    # We need to create a caster
    caster: e.Entity = e.Entity()

    # And some filler dino and enemies values
    dino, enemies, _ = getSingleSliceOfDinoEnemiesClearing()

    # And some arbitrary from location
    from_location = CardLocation("from-location")

    # Populates card locations (for these tests, the naming of cards in the locations is not important)
    card_location_utilities.populate_card_location(
        test_arguments.from_location_size, 
        from_location,
        card_location_utilities.LOWERCASE_ALHPABET
    )
    card_location_utilities.populate_card_location(
        test_arguments.discard_size,
        caster.discard, 
        card_location_utilities.NUMBERS_AS_STRINGS
    )

    # Gets access to the card we expect to discard
    expected_discarded_card = from_location.at(test_arguments.index_of_discarded_card)

    # Does the discarding
    discarded_card = caster.discardCard(
        from_location,
        test_arguments.index_of_discarded_card,
        dino,
        enemies,
        vis.prefabEmpty()
    )

    # Did we discard the correct card?
    assert discarded_card == expected_discarded_card

    # Is our from location the correct length?
    assert test_arguments.expected_from_location_size == from_location.length()

    # Is our discard the correct length?
    assert test_arguments.expected_discard_size == caster.discard.length()

    