import pytest
import pytest_timeout
from tests.test_utils import simulate_gameplay
from tests.test_utils.game_setups import (getCartesianProduct_anyInput,
                                   setup_getCardSetTwoWithToLocations,
                                   setup_getDinoEnemiesClearing)
from tests.test_utils.validate_game_state import isCardExclusivelyAtIndexInLocation

from Dinosaur_Venture import gameplay_loop_events as gameEvents
from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture import get_cards_by_table as gcbt

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
            simulate_gameplay.simulate(
            dino, enemies, clearing, 
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard_attemptPlayCardByName([testCard.name]))
            ])

            ## Tests if cards are in expected locations
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.draw, dino, enemies)
            assert isCardExclusivelyAtIndexInLocation(cantrip, 0, dino.hand, dino, enemies)

            ## Plays the cantrip
            simulate_gameplay.simulate(
            dino, enemies, clearing,
            [
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard_attemptPlayCardByName([cantrip.name]))
            ])

            ## Tests if cards are in expected locations
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.hand, dino, enemies)
            assert isCardExclusivelyAtIndexInLocation(cantrip, 0, dino.play, dino, enemies)

            ## Plays the test card once more
            simulate_gameplay.simulate(
            dino, enemies, clearing,
            [
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard_attemptPlayCardByName([testCard.name]))
            ])

            ## Tests if cards are in expected locations
            assert isCardExclusivelyAtIndexInLocation(testCard, 0, dino.draw, dino, enemies)
            assert isCardExclusivelyAtIndexInLocation(cantrip, 0, dino.play, dino, enemies)
            
            ## Can change to: is card exclusively at index in location