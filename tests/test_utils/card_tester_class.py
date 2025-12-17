import copy
import random
from abc import ABC
from typing import TYPE_CHECKING

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture.logging import gameplay_logging as log
from tests.test_utils import simulate_gameplay
from tests.test_utils.game_setups import (getCartesianProduct_anyInput,
                                          setup_getDinoEnemiesClearing)

DINOES, ENEMIESES, CLEARINGSES = setup_getDinoEnemiesClearing()
DINOES_ENEMIESES_CLEARINGSES = getCartesianProduct_anyInput([DINOES, ENEMIESES, CLEARINGSES])

if TYPE_CHECKING:
    from Dinosaur_Venture import card as c
    from Dinosaur_Venture.logging.intent import Intent
    from Dinosaur_Venture.logging.log_entry import LogEntry

class TestCard(ABC):
    """
    Inherited by classes to test card functionality.
    """
    pass

class CardTestingMethods():
    """
    List of methods useful for testing cards.
    """
    @staticmethod
    def _assert_logs_match_intent(intents: list["Intent"]):
        """
        Crawls through the log, ensuring that instances of our expected intents match to instances
        of log entries, in order.
        """
        # We have nothing to test
        if len(intents) == 0:
            return True
        
        intent_index = 0

        # Continuously crawls until all intents have found matches
        all_logs_types = [] # Used for printing when we have an error
        while intent_index < len(intents):
            curr_intent: "Intent" = intents[intent_index]

            if not log.contains_next_log_line():
                # We did not end up finding this current intent, so we throw an error
                assert False, (
                    "Failed to find Intent " + str(curr_intent.log_class) + "\n" + 
                    "with object parameters " + str(curr_intent.python_object_parameters) + "\n" +
                    "within the following logs " + str(all_logs_types)
                )

            curr_log_entry: "LogEntry" = log.get_next_log_line()
            all_logs_types.append(type(curr_log_entry))

            # Print statements for debugging
            ## print("CURRENT INTENT: ", curr_intent.log_class, curr_intent.json_parameters, curr_intent.python_object_parameters)
            # print("CURRENT INTENT: ", curr_intent.log_class, curr_intent.python_object_parameters)
            # print("CURRENT LOG ENTRY: ", curr_log_entry)

            # First, do we have matching LogEntry types?
            if not isinstance(curr_log_entry, curr_intent.log_class):
                continue

            # Next, do we have matching JSON parameters?
            contains_json_parameters = True
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
                if (current_object and isinstance(current_object, (int, float, str, bool)) and isinstance(value, (int, float, str, bool))):
                    contains_python_object_parameters = (current_object == value)

                elif (current_object):
                    contains_python_object_parameters = (value.__eq__(current_object))

            # If both are contained, we have a success!
            if contains_json_parameters and contains_python_object_parameters:
                intent_index += 1
        
        # Since we traversed through all intents, the logs match our intents!
        return True

    @staticmethod
    def default_test_card_intent_simulation(
        intent: list["Intent"],
        card_to_test: "c.Card",
        simulateGameEventsArray: list[simulate_gameplay.simulateGameEvent]
    ) -> None:
        """
        Tests the logs created by the input simulateGameEventsArray against the input intent value.
        Uses a single instance of dino, enemies, and clearing.
        """
        # Uses a single instance of dino, enemies, and clearing
        dino, enemies, clearing = CardTestingMethods.default_dino_enemies_clearing_getter()

        # We do not want any of the enemies/dino to die (messes with scripted input), so we give them 999 hp in every channel
        new_healthcons = cll.Healthcons(999, 999, 999, 'nil')
        for entity in enemies + [dino]:
            entity.setHP(copy.deepcopy(new_healthcons))

        # Gains the card to dino's deck
        dino.gainCard(card_to_test(), dino.deck)

        # Runs through playing the card based on our input simulated game events array
        simulate_gameplay.simulate(
            dino,
            enemies,
            clearing,
            simulateGameEventsArray
        )
        
        # Does our intent match our logs?
        assert CardTestingMethods._assert_logs_match_intent(intent)

    @staticmethod
    def default_dino_enemies_clearing_getter() -> tuple:
        """
        Returns a (dino, enemies, clearing) tuple used for testing.
        Most test cases simply need to call this unless the card must test specific, unique behavior.
        """        
        return copy.deepcopy(DINOES_ENEMIESES_CLEARINGSES[random.randint(0, len(DINOES_ENEMIESES_CLEARINGSES) - 1)])

# Constant used to run all of these Card Testing Methods
CARD_TESTING_METHODS = CardTestingMethods()
