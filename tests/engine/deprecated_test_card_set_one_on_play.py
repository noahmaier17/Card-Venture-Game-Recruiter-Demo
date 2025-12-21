# Commented out this test. It was one of my first tests and it does not match the direction I took for testing.
"""
import pytest
import pytest_timeout

from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from tests.test_utils import simulate_gameplay
from tests.test_utils.game_setups import (
    getCartesianProduct_dinoEnemiesClearingCards, setup_getCardSetOne,
    setup_getDinoEnemiesClearing)
from tests.test_utils.validate_game_state import \
    isCardExclusivelyAtIndexInLocation

'''
    Tests the case where dinosaur has only one card in deck, and if the game can successfully:
    (1) Play the card
    (2) Not play the card with "pass" input
    (3) Handle gibberish input
    (4) Handle gibberish input, then handle playing the card

    Uses cardSetOne; see setup_getCardSetOne for information.
'''

class TestSuite():
    @pytest.mark.timeout(5)
    def test_cardSetOne_onlyCard_expectedBehavior(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for set in getCartesianProduct_dinoEnemiesClearingCards(dinoes, enemieses, clearingses, cardses):
            dino, enemies, clearing, testCard = set

            ## Adds a card into dino's deck
            dino.gainCard(testCard, dino.deck)

            ## Run through play card
            simulate_gameplay.simulate(
                dino, enemies, clearing, 
                [
                    simulate_gameplay.startRound(),
                    simulate_gameplay.dinoTurnStart(),
                    simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard([1]))
                ])

            ## Checks if the card is in play
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.play, dino, enemies)

    @pytest.mark.timeout(5)
    def test_cardSetOne_onlyCard_handlePassing(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for set in getCartesianProduct_dinoEnemiesClearingCards(dinoes, enemieses, clearingses, cardses):
            dino, enemies, clearing, testCard = set

            ## Adds a card into dino's deck
            dino.gainCard(testCard, dino.deck)

            ## Run through play card
            simulate_gameplay.simulate(
                dino, enemies, clearing, 
                [
                    simulate_gameplay.startRound(),
                    simulate_gameplay.dinoTurnStart(),
                    simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard(["pass"]))
                ])

            ## Checks if the card is in play
            assert not isCardExclusivelyAtIndexInLocation(testCard, 0, dino.play, dino, enemies)

    @pytest.mark.timeout(5)
    def test_cardSetOne_onlyCard_handleGibberishInput_intoPass(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for set in getCartesianProduct_dinoEnemiesClearingCards(dinoes, enemieses, clearingses, cardses):
            dino, enemies, clearing, testCard = set

            ## Adds a card into dino's deck
            dino.gainCard(testCard, dino.deck)

            ## Run through play card
            simulate_gameplay.simulate(
                dino, enemies, clearing, 
                [
                    simulate_gameplay.startRound(),
                    simulate_gameplay.dinoTurnStart(),
                    simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard(["askdfaskdjfksa", "128391823912839", "0", "pass"]))
                ])

            ## Checks if the card is in play exclusively
            assert not isCardExclusivelyAtIndexInLocation(testCard, 0, dino.play, dino, enemies)
    
    @pytest.mark.timeout(5)
    def test_cardSetOne_onlyCard_handleGibberishInput_intoPlayCard(self, setup_getDinoEnemiesClearing, setup_getCardSetOne):
        ## Fixture Setup
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing
        cardses = setup_getCardSetOne

        for set in getCartesianProduct_dinoEnemiesClearingCards(dinoes, enemieses, clearingses, cardses):
            dino, enemies, clearing, testCard = set

            ## Adds a card into dino's deck
            dino.gainCard(testCard, dino.deck)

            ## Run through play card
            simulate_gameplay.simulate(
                dino, enemies, clearing, 
                [
                    simulate_gameplay.startRound(),
                    simulate_gameplay.dinoTurnStart(),
                    simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard(["askdfaskdjfksa", "128391823912839", "0", "1"]))
                ])

            ## Checks if the card is in play
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.play, dino, enemies)
"""

'''
    NOTES:

    1. all test files must begin with test_ (or alternatively end with _test).
    2. all test suites must start with Test.
    3. we can define 'fixtures,' which is run and sets up several variables. We can return tuples with them.
    4. "@pytest.mark.timeout(5)" prevents infinite waits, simply crashing the running pytest call.
    5. call pytest -s
'''