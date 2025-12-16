import copy
import random

from Dinosaur_Venture.logging import gameplay_logging as log
from tests.test_utils.game_setups import setup_getDinoEnemiesClearing, getCartesianProduct_anyInput, getSingleSlice
from tests.test_utils import simulate_gameplay
from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture.dino_cards_depot import fallow_farmland_cards
from Dinosaur_Venture import channel_linked_lists as cll

DINOES, ENEMIESES, CLEARINGSES = setup_getDinoEnemiesClearing()
DINOES_ENEMIESES_CLEARINGSES = getCartesianProduct_anyInput([DINOES, ENEMIESES, CLEARINGSES])

# Move this into test utilities later
def check_logs_match_intent(intents: list[log.Intent]):
    # We must crawl the logs and check if the sequence of intent values matches the sequence of logs
    # We will just do this by starting at the top of the log and crawling
    if len(intents) == 0:
        # We have nothing to test
        return True

    intent_index = 0

    while intent_index < len(intents):
        if not log.contains_next_log_line():
            return False

        curr_log_entry: log.LogEntry = log.get_next_log_line()
        curr_intent: log.Intent = intents[intent_index]

        # print("CURRENT INTENT: ", curr_intent.log_class, curr_intent.json_parameters, curr_intent.python_object_parameters)
        print("CURRENT INTENT: ", curr_intent.log_class, curr_intent.python_object_parameters)
        print("CURRENT LOG ENTRY: ", curr_log_entry)

        # First, do we have matching LogEntry types?
        if not isinstance(curr_log_entry, curr_intent.log_class):
            continue

        # Next, do we have matching JSON parameters?
        contains_json_parameters = True
        '''
        for key_list, value in curr_intent.json_parameters.items():
            # We will traverse down this list of keys, which (if successful) will give us a specific value.
            # We will see if that value matches what we are expecting

            # We can have a sequence of keys, separated by periods
            keys = key_list.split(".")

            # Traverses down the LogEntry to other objects based off the sequence of keys
            current_dictionary_level = curr_log_entry.to_json()
            for key in keys:
                if key not in current_dictionary_level:
                    current_dictionary_level = None
                    break

                else:
                    current_dictionary_level = current_dictionary_level[key]

            if not(current_dictionary_level and value == current_dictionary_level):
                contains_json_parameters = False
        '''

        # Last, do we have matching Python object parameters?
        contains_python_object_parameters = True
        for key_list, value in curr_intent.python_object_parameters.items():
            # We will traverse down this list of keys, which (if successful) will give us a specific value.
            # We will see if that value matches what we are expecting

            # We can have a sequence of keys, separated by periods
            keys = key_list.split(".")

            # Traverses down the LogEntry to other objects based off the sequence of keys
            current_object = curr_log_entry
            for key in keys:
                potential_next_object: None | object = getattr(current_object, key, None)
                if not potential_next_object:
                    current_object = None
                    break

                else:
                    current_object = potential_next_object

            # If we have a current object, and our expected value matches the actual value,
            # our log entries match!
            if not (current_object and value.__eq__(current_object)):
                contains_python_object_parameters = False

        # If both are contained, we have a success!
        if contains_json_parameters and contains_python_object_parameters:
            intent_index += 1
    
    # Since we traversed through all INTENTs, the logs match intent
    return True

class TestTrampledRodent:
    INTENT = [
        log.Intent(
            log.EntityPlayCardLogEntry,
            {"playedCard.name": "Trampled Rodent"}
        ),
        log.Intent(
            log.EntityPlusActionsLogEntry,
            {"plusActions": 1}
        ),
        log.Intent(
            log.EntityDamage,
            {"attackData": cll.Attackcons([1, cll.Rnotick()],
                           cll.Attackcons([1, cll.Gnotick()],
                           cll.Attackcons([1, cll.Bnotick()],
                           cll.Attackcons([1, cll.M()],
                           'nil'))))
            }
        )
    ]

    CARD_TO_TEST = fallow_farmland_cards.trampledRodent

    def test_card_intent(self):
        # We will just test for 1 random slice
        dino, enemies, clearing = copy.deepcopy(DINOES_ENEMIESES_CLEARINGSES[random.randint(0, len(DINOES_ENEMIESES_CLEARINGSES) - 1)])

        # Puts the card into dino's deck
        dino.gainCard(self.CARD_TO_TEST(), dino.deck)

        ## Run through play card
        simulate_gameplay.simulate(
            dino, enemies, clearing, 
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard([1]))
            ])
    
        assert check_logs_match_intent(self.INTENT)

class TestMangledShrew:
    INTENT = [
        log.Intent(
            log.EntityPlayCardLogEntry,
            {"playedCard.name": "Mangled Shrew"},
        ),
        log.Intent(
            log.EntityDamage,
            {"attackData": cll.Attackcons([2, cll.Rnotick()],
                           cll.Attackcons([1, cll.Filled()],
                           cll.Attackcons([1, cll.Filled()],
                           cll.Attackcons([1, cll.Filled()],
                           'nil'))))
            }
        )
    ]

    CARD_TO_TEST = fallow_farmland_cards.mangledShrew

    def test_card_intent(self):
        # We will just test for 1 random slice
        dino, enemies, clearing = copy.deepcopy(DINOES_ENEMIESES_CLEARINGSES[random.randint(0, len(DINOES_ENEMIESES_CLEARINGSES) - 1)])

        # Puts the card into dino's deck
        dino.gainCard(self.CARD_TO_TEST(), dino.deck)

        ## Run through play card
        simulate_gameplay.simulate(
            dino, enemies, clearing, 
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.script_DinoPlayCard([1]))
            ])
    
        assert check_logs_match_intent(self.INTENT)
