import pytest
import pytest_timeout

from Dinosaur_Venture.entities import dinoes as dinoes_import
from Dinosaur_Venture.entities import entity as e
from tests.test_utils.list_utilities import are_upcoming_lists_equal


@pytest.mark.parametrize(
    "entity, plus_cards_for_next_turn, array_of_expected_plus_cards_by_turn_number",
    [
        (dinoes_import.Dinosaur(), 0, [0, 0]),
        (dinoes_import.Dinosaur(), 1, [1, 0]),
        (dinoes_import.Dinosaur(), 2, [2, 0])
    ]
)
@pytest.mark.timeout(5)
def test_plusXCardsForNextTurn(entity: e.Entity, plus_cards_for_next_turn, array_of_expected_plus_cards_by_turn_number):
    """
        Tests:
        1. Does Plus Cards for the Next Turn work correctly?
    """
    entity.plusUpcomingPlusCard(0, plus_cards_for_next_turn)

    assert are_upcoming_lists_equal(array_of_expected_plus_cards_by_turn_number, entity.upcomingPlusCard)
