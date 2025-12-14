import pytest
import random

from Dinosaur_Venture import helper as h
from tests.test_utils.game_setups import setup_getDinoEnemiesClearing, getCartesianProduct_anyInput
from Dinosaur_Venture import gameplay_scripted_input as scriptInput

DINOES, ENEMIESES, CLEARINGSES = setup_getDinoEnemiesClearing()
DINOES_ENEMIESES_CLEARINGSES = getCartesianProduct_anyInput([DINOES, ENEMIESES, CLEARINGSES])

@pytest.mark.parametrize(
    "dino, enemies, clearings",
    DINOES_ENEMIESES_CLEARINGSES
)
def test_pickLivingEnemy_allLiving(dino, enemies, clearings):
    """
    Does h.pickLivingEnemy accurately pick an enemy will all living enemies?
    """
    # Picks a random index
    pick_index = random.randint(0, len(enemies) - 1) + 1
    assert pick_index - 1 == h.pickLivingEnemy("Splash text", enemies, scriptedInput=scriptInput.gameplayScriptInput([pick_index]))

    # Picks a random index but starting with gibberish text
    pick_index = random.randint(0, len(enemies) - 1) + 1
    assert pick_index - 1 == h.pickLivingEnemy("Splash text", enemies, scriptedInput=scriptInput.gameplayScriptInput(
        ["gibberish", "sdhfjasdjhfsadhfjasdhjf", "MORE gibberish", pick_index]
    ))

@pytest.mark.parametrize(
    "dino, enemies, clearings",
    DINOES_ENEMIESES_CLEARINGSES
)
def test_pickLivingEnemy_pickInvalidThenLiving(dino, enemies, clearings):
    """
    Does h.pickLivingEnemy accurately pick an enemy when first selecting wrong values?
    """
    # If we have a clearing with only 1 enemy, skips this test
    if len(enemies) < 2:
        return

    all_indices = list(range(0, len(enemies)))
    # Picks a random index to kill
    kill_index = all_indices.pop(random.randint(0, len(all_indices) - 1)) + 1
    enemies[kill_index - 1].dead = True

    # Picks a different but still random index to pick
    pick_index = all_indices.pop(random.randint(0, len(all_indices) - 1)) + 1

    # Picks another number outside the range of possible values
    outside_of_range_index = len(enemies) + 1

    # Can we pick this living enemy?
    assert pick_index - 1 == h.pickLivingEnemy("Splash text", enemies, scriptedInput=scriptInput.gameplayScriptInput([pick_index]))

    # Can we accurately pick the dead enemy then the living enemy?
    assert pick_index - 1 == h.pickLivingEnemy("Splash text", enemies, scriptedInput=scriptInput.gameplayScriptInput(
        ["gibberish text", kill_index, "more gibberish", pick_index]
    ))

    # Can we accurately pick an out of bounds value, dead enemy, then living enemy?
    assert pick_index - 1 == h.pickLivingEnemy("Splash text", enemies, scriptedInput=scriptInput.gameplayScriptInput(
        [outside_of_range_index, kill_index, "kdsfjaskdfjksadjfkasdjkfj", kill_index, outside_of_range_index, pick_index]
    ))


@pytest.mark.parametrize(
    "dino, enemies, clearings",
    DINOES_ENEMIESES_CLEARINGSES
)
def test_pickLivingEnemy_allEnemiesAreDead(dino, enemies, clearings):
    """
    Does h.pickLivingEnemy correctly return -1 when no enemies are living?
    """

    # Makes all enemies dead, and then tests the output by h.pickLivingEnemy
    for enemy in enemies:
        enemy.dead = True

    assert -1 == h.pickLivingEnemy("Splash text", enemies)