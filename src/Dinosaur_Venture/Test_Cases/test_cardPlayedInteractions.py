import pytest, pytest_timeout, random, copy
from Dinosaur_Venture import entity as e, getCardsByTable as gcbt, clearing as clr, gameplayLoopEvents as gameEvents, gameplayScriptedInput as scriptInput

## Sets up dino, enemies, and the clearing.
## Clearing is randomly assigned.
@pytest.fixture
def setup_getDinoEnemiesClearing():
    ## We want all the casters, dino, enemies, clearing, etc.

    ## (1 and 2) Caster and dino
    dinoes = [e.Dinosaur()] ## Empty Player Character

    ## (3) Enemies
    enemieses = []
    enemieses.append([e.Copperals()])

    ## (4) Gets 5 clearings (randomly, allowing duplicates)
    clearinges = []
    setOfAllWoods = []
    for neck in clr.NeckOfTheWoods.__subclasses__():
        if neck().include:
            setOfAllWoods.append(neck())
    for i in range(3):
        random.shuffle(setOfAllWoods)
        neckOfTheWoods = setOfAllWoods[0]
        clearinges.append(neckOfTheWoods.clearing)

    return (dinoes, enemieses, clearinges)

## Gets card set 1, defined as cards that are:
## (1) Dino's and Vanilla
## (2) { 0H }
## (3) Stay in play after resolution
## (4) Requires no further input upon being played
## There are no guarentees about:
## (1) [ Text ] nor < Text >            - Although they will be vanilla
## (2) Tokens                           - Although they will be vanilla
@ pytest.fixture
def setup_getCardSetOne():
    cardses = []
    cardses.append(gcbt.getCardByName("Twig!"))
    cardses.append(gcbt.getCardByName("Stick"))
    cardses.append(gcbt.getCardByName("Grasshopper Cache"))
    cardses.append(gcbt.getCardByName("Torch Bearing"))
    return cardses

## Checks if a card is at a specific index in a specific location.
## To be robust against deep copies (and the like), checks against the card's uniqueID.
def isCardAtIndexInLocation(card, index, location):
    if location.length() <= index:
        return False

    crosscompareCard = location.at(index)
    return (card.uniqueID == crosscompareCard.uniqueID)

class TestSuite():
    @pytest.mark.timeout(5)
    def test_cardSetOne_onlyCard_expectedBehavior(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearinges = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for dinoCopy in dinoes:
            for enemiesCopy in enemieses:
                for clearingCopy in clearinges:
                    for cardCopy in cardses:
                        ## Gets copies of all these items
                        dino = copy.deepcopy(dinoCopy)
                        enemies = copy.deepcopy(enemiesCopy)
                        clearing = copy.deepcopy(clearingCopy)
                        card = copy.deepcopy(cardCopy)

                        ## Adds a card into dino's deck
                        dino.gainCard(card, dino.deck)

                        ## --- Runs the gameplay ---
                        gameEvents.startRound(dino, enemies)
                        gameEvents.dinoTurnStart(dino, enemies)
                        gameEvents.dinoPlayCard(dino, enemies, 0, clearing, "Dino Play Card", None, None,
                                                scriptedInput = scriptInput.script_DinoPlayCard([1]))

                        ## Checks if the card is in play
                        assert isCardAtIndexInLocation(card, 0, dino.play)
                        assert not isCardAtIndexInLocation(card, 0, dino.hand)

    @pytest.mark.timeout(5)
    def test_twigExclamation_onlyCard_handlePassing(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearinges = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for dinoCopy in dinoes:
            for enemiesCopy in enemieses:
                for clearingCopy in clearinges:
                    for cardCopy in cardses:
                        ## Gets copies of all these items
                        dino = copy.deepcopy(dinoCopy)
                        enemies = copy.deepcopy(enemiesCopy)
                        clearing = copy.deepcopy(clearingCopy)
                        card = copy.deepcopy(cardCopy)

                        ## Adds a card into dino's deck
                        dino.gainCard(card, dino.deck)

                        ## --- Runs the gameplay ---
                        gameEvents.startRound(dino, enemies)
                        gameEvents.dinoTurnStart(dino, enemies)
                        gameEvents.dinoPlayCard(dino, enemies, 0, clearing, "Dino Play Card", None, None,
                                                scriptedInput = scriptInput.script_DinoPlayCard(["pass"]))

                        ## Checks if the card is in play
                        assert not isCardAtIndexInLocation(card, 0, dino.play)
                        assert isCardAtIndexInLocation(card, 0, dino.hand)

    @pytest.mark.timeout(5)
    def test_twigExclamation_onlyCard_handleGibberishInput(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearinges = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for dinoCopy in dinoes:
            for enemiesCopy in enemieses:
                for clearingCopy in clearinges:
                    for cardCopy in cardses:
                        ## Gets copies of all these items
                        dino = copy.deepcopy(dinoCopy)
                        enemies = copy.deepcopy(enemiesCopy)
                        clearing = copy.deepcopy(clearingCopy)
                        card = copy.deepcopy(cardCopy)

                        ## Adds a card into dino's deck
                        dino.gainCard(card, dino.deck)

                        ## --- Runs the gameplay ---
                        gameEvents.startRound(dino, enemies)
                        gameEvents.dinoTurnStart(dino, enemies)
                        gameEvents.dinoPlayCard(dino, enemies, 0, clearing, "Dino Play Card", None, None,
                                                scriptedInput = scriptInput.script_DinoPlayCard(["pass"]))

                        ## Checks if the card is in play
                        assert not isCardAtIndexInLocation(card, 0, dino.play)
                        assert isCardAtIndexInLocation(card, 0, dino.hand)
        
'''
    NOTES:

    1. all test files must begin with test_ (or alternatively end with _test).
    2. all test suites must start with Test.
    3. we can define 'fixtures,' which is run and sets up several variables. We can return tuples with them.
    4. "@pytest.mark.timeout(5)" prevents infinite waits, simply crashing the running pytest call.
    5. call pytest -s
'''