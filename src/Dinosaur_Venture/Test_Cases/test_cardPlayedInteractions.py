import pytest, pytest_timeout, random
from Dinosaur_Venture import entity as e, getCardsByTable as gcbt, clearing as clr, gameplayLoopEvents as gameEvents

@pytest.fixture
def setup_getDinoEnemiesClearing():
    ## We want all the casters, dino, enemies, clearing, etc.

    ## (1 and 2) Caster and dino
    dino = e.Dinosaur() ## Empty Player Character
    dino.gainCard(gcbt.getCardByName("Twig!"), dino.deck)

    ## (3) Enemies
    enemies = []
    enemies.append(e.Copperals())

    ## (4) Gets a clearing
    setOfAllWoods = []
    for neck in clr.NeckOfTheWoods.__subclasses__():
        if neck().include:
            setOfAllWoods.append(neck())
    random.shuffle(setOfAllWoods)
    neckOfTheWoods = setOfAllWoods[0]
    clearing = neckOfTheWoods.clearing

    return (dino, enemies, clearing)

class TestSuite():
    @pytest.mark.timeout(25)
    def test_twigExclamation_expectedBehavior(self, setup_getDinoEnemiesClearing):
        dino, enemies, clearing = setup_getDinoEnemiesClearing
        gameEvents.startRound(dino, enemies)
        gameEvents.dinoPlayCard(dino, enemies, 0, clearing, "Dino Play Card", None, None) # , automatedUserInput = [1])
        assert True

'''
    NOTES:

    1. all test files must begin with test_ (or alternatively end with _test).
    2. all test suites must start with Test.
    3. we can define 'fixtures,' which is run and sets up several variables. We can return tuples with them.
    4. "@pytest.mark.timeout(5)" prevents infinite waits, simply crashing the running pytest call.
    5. call pytest -s
'''