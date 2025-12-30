import pytest
import pytest_timeout

from Dinosaur_Venture.entities import dinoes as dinoes_import
from Dinosaur_Venture.entities import entity as e


@pytest.mark.parametrize(
    "plus_actions, starting_actions, expected_remaining_actions",
    [
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 2),
        (1, 2, 3),
        (1, 3, 4),
        (2, 1, 3),
        (2, 2, 4),
        (2, 3, 5)
    ]
)
@pytest.mark.parametrize(
    "entity_class",
    [e.Entity, dinoes_import.Dinosaur]
)
@pytest.mark.timeout(5)
def test_plusXActions(plus_actions, starting_actions, expected_remaining_actions, entity_class):
    """
        Tests:
        1. Does +X Action(s) work correctly?
    """

    entity = entity_class()
    entity.actions = starting_actions

    entity.plusActions(plus_actions)

    assert expected_remaining_actions == entity.actions