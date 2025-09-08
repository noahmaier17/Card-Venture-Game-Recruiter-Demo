import pytest, pytest_timeout, copy
from Dinosaur_Venture import gameplayLoopEvents as gameEvents, gameplayScriptedInput as scriptInput
from Dinosaur_Venture.Test_Cases.Test_Utils.gameSetups import setup_getDinoEnemiesClearing, setup_getCardSetOne
from Dinosaur_Venture.Test_Cases.Test_Utils.validateGameState import isCardAtIndexInLocation

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
                                                scriptedInput=scriptInput.script_DinoPlayCard([1]))

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