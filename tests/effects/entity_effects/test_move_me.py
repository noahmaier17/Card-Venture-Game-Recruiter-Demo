import pytest

from Dinosaur_Venture import helper as h
from Dinosaur_Venture.cards.mechanics import card as c
from Dinosaur_Venture.entities import entity as e
from tests.test_utils import card_location_utilities, list_utilities


class test_arguments():
    """
    Contains all the arguments neccesary for testing. Utilized to make reading tests easier.
    """
    def __init__(
        self,
        from_location_size: int = 0,
        card_by_index_to_move: int = 0,
        to_location_size: int = 0,
        position: int = 0,
        expect_successful_move: bool = True        # Do we expect the card to actually get moved?
    ) -> None:
        self.from_location_size = from_location_size
        self.card_by_index_to_move = card_by_index_to_move
        self.to_location_size = to_location_size
        self.position = position
        self.expect_successful_move = expect_successful_move


@pytest.mark.parametrize(
    "test_arguments",
    [
        # Moves a card from a location onto the other location
        test_arguments(
            from_location_size=1,
            card_by_index_to_move=0,
            to_location_size=10,
            position=0
        ),
        test_arguments(
            from_location_size=5,
            card_by_index_to_move=2,
            to_location_size=3,
            position=0
        ),
        test_arguments(
            from_location_size=7,
            card_by_index_to_move=6,
            position=0
        ),
        # Fails to find the card meaning it cannot be moved
        test_arguments(
            from_location_size=20,
            card_by_index_to_move=-1,
            to_location_size=20,
            position=0,
            expect_successful_move=False
        )
    ]
)
def test_move_card_onto_location(test_arguments: test_arguments):
    """
    Does moving a card onto the top of a location work correctly?
    """
    # We need to create a caster
    caster: e.Entity = e.Entity()

    # fromLocation will have lowercase letter'd names, toLocation will have uppercase letter'd names.
    # fromLocation and toLocation will be ordered from A to Z to test correct sequencing.

    # Does that aforementioned populating
    fromLocation = h.cardLocation("from-location")
    card_location_utilities.populate_card_location(
        test_arguments.from_location_size, 
        fromLocation,
        card_location_utilities.LOWERCASE_ALHPABET
    )

    toLocation = h.cardLocation("to-location")
    card_location_utilities.populate_card_location(
        test_arguments.to_location_size,
        toLocation, 
        card_location_utilities.UPPERCASE_ALHPABET
    )

    # The card we care about is at index card_by_index_to_move
    if test_arguments.card_by_index_to_move < 0 or test_arguments.card_by_index_to_move >= test_arguments.from_location_size:
        # Out of bounds value, so we will try to move a card that does not exist
        card = c.Card()
        card.name = "Card That Does Not Exist In From Location"
    else:
        card = fromLocation.at(test_arguments.card_by_index_to_move)

    # Does the moving
    response = caster.moveMe(fromLocation, card, toLocation, test_arguments.position, suppressFailText=True)

    # Was the moving successful if expected to be successful, and vice versa?
    assert response == test_arguments.expect_successful_move

    # If we are expecting a successful move...
    if test_arguments.expect_successful_move:
        # ... is this card no longer in the fromLocation?
        assert card not in fromLocation.getArray()

        # ... is this card in the toLocation?
        assert card in toLocation.getArray()

        # ... is our fromLocation still correctly ordered?
        assert card_location_utilities.is_location_sorted_per_parameter(fromLocation, card_location_utilities.LOWERCASE_ALHPABET)

        # ... does our toLocation contain this card at index position while otherwise remaining unchanged?
        compare_to_location = h.cardLocation("compare-to-location")
        card_location_utilities.populate_card_location(
            test_arguments.to_location_size,
            compare_to_location, 
            card_location_utilities.UPPERCASE_ALHPABET
        )
        compare_to_location.insert(test_arguments.position, card)

        assert list_utilities.are_lists_exactly_equal(
            toLocation.getArray(), 
            compare_to_location.getArray(),
            comparison_parameter=list_utilities.default_name_comparison_parameter
        )

    # ... if not...
    else:
        # ... is our fromLocation still correctly ordered?
        assert card_location_utilities.is_location_sorted_per_parameter(fromLocation, card_location_utilities.LOWERCASE_ALHPABET)

        # ... is our toLocation still correctly ordered?
        assert card_location_utilities.is_location_sorted_per_parameter(toLocation, card_location_utilities.UPPERCASE_ALHPABET)

        # ... is this card correctly not in the toLocation?
        assert card not in toLocation.getArray()

        # ... is this card correctly not in the fromLocation?
        assert card not in fromLocation.getArray()