import pytest
import pytest_timeout
from test_utils import simulateGameplay
from test_utils.gameSetups import (getCartesianProduct_anyInput,
                                   setup_getCardSetTwoWithToLocations,
                                   setup_getDinoEnemiesClearing)
from test_utils.validateGameState import isCardExclusivelyAtIndexInLocation

from Dinosaur_Venture import gameplayLoopEvents as gameEvents
from Dinosaur_Venture import gameplayScriptedInput as scriptInput
from Dinosaur_Venture import getCardsByTable as gcbt

'''
    Tests the case where dinosaur has a card that leaves play.

    Uses cardSetTwo; see setup_getCardSetOne for information. 
'''

class TestSuite():
    '''
        Tests:
        1. Play the card. These cards will reappear in some location.
        2. Plays a default cantrip card.
        3. Replays that card.
    '''
    @pytest.mark.timeout(5)
    def test_playCard_redraw_playCard(self, setup_getDinoEnemiesClearing, setup_getCardSetTwoWithToLocations):
        ## Fixture Setup
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing
        cardsesWithToLocations = setup_getCardSetTwoWithToLocations
        cantripses = [gcbt.getCardByName("Cantrip")]

        for set in getCartesianProduct_anyInput([dinoes, enemieses, clearingses, cardsesWithToLocations, cantripses]):
            dino, enemies, clearing, cardsesWithToLocations, cantrip = set
            testCard, testCardToLocation = cardsesWithToLocations

            ## Adds the test card and cantrip card into dino's deck
            dino.gainCard(testCard, dino.deck)
            dino.gainCard(cantrip, dino.deck)

            ## Run through gameplay
            simulateGameplay.simulate(
            dino, enemies, clearing, 
            [
                simulateGameplay.startRound(),
                simulateGameplay.dinoTurnStart(),
                simulateGameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard_attemptPlayCardByName([testCard.name]))
            ])

            ## Tests if cards are in expected locations
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.draw, dino, enemies)
            assert isCardExclusivelyAtIndexInLocation(cantrip, 0, dino.hand, dino, enemies)

            ## Plays the cantrip
            simulateGameplay.simulate(
            dino, enemies, clearing,
            [
                simulateGameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard_attemptPlayCardByName([cantrip.name]))
            ])

            ## Tests if cards are in expected locations
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.hand, dino, enemies)
            assert isCardExclusivelyAtIndexInLocation(cantrip, 0, dino.play, dino, enemies)

            ## Plays the test card once more
            simulateGameplay.simulate(
            dino, enemies, clearing,
            [
                simulateGameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard_attemptPlayCardByName([testCard.name]))
            ])

            ## Tests if cards are in expected locations
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.draw, dino, enemies)
            assert isCardExclusivelyAtIndexInLocation(cantrip, 0, dino.play, dino, enemies)
            
            ## Can change to: is card exclusively at index in location