"""
test_card_testing.py

Tests if the card testing works correctly. Sees if we have accurate successes and accurate failures.
"""

import pytest

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.dino_cards_depot import fallow_farmland_cards
from Dinosaur_Venture.logging import intent
from tests.test_utils import simulate_gameplay
from tests.test_utils.card_tester_class import CardTestingMethods, TestCard


class TestCardTesting(TestCard):
    # We just use Trampled Rodent just for fun
    CARD_TO_TEST = fallow_farmland_cards.trampledRodent

    def test_assertion_for_wrong_name(self):
        """
        If we have an incorrect intent parameter (specifically a wrong name), do we correctly have a false?
        """
        intents = [
            intent.entity_play_card_intent_factory("SUPER DUPER WRONG NAME SO WRONG"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(
                cll.Attackcons([1, cll.Rnotick()],
                cll.Attackcons([1, cll.Gnotick()],
                cll.Attackcons([1, cll.Bnotick()],
                cll.Attackcons([1, cll.M()],
                'nil'))))
            ),
            intent.card_function_arbitrarily_discard_card_from_location_intent_factory(h.CARD_LOCATION_HAND, True)
        ]
        
        # Expects the assertion
        with pytest.raises(AssertionError):
            CardTestingMethods.default_test_card_intent_simulation(
                intents,
                self.CARD_TO_TEST,
                [
                    simulate_gameplay.startRound(),
                    simulate_gameplay.dinoTurnStart(),
                    simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
                ]
            )

    def test_assertion_for_incorrect_damage_intent(self):
        """
        Does an incorrect damage intent factory cause an error?
        """
        intents = [
            intent.entity_play_card_intent_factory("Trampled Rodent"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(
                cll.Attackcons([999, cll.Rnotick()],
                cll.Attackcons([999, cll.Gnotick()],
                cll.Attackcons([999, cll.Bnotick()],
                cll.Attackcons([1999, cll.M()],
                cll.Attackcons([999, cll.Rnotick()],
                cll.Attackcons([999, cll.Gnotick()],
                cll.Attackcons([999, cll.Bnotick()],
                cll.Attackcons([1999, cll.M()],
                'nil'))))))))
            ),
            intent.card_function_arbitrarily_discard_card_from_location_intent_factory(h.CARD_LOCATION_HAND, True)
        ]

        # Expects the assertion
        with pytest.raises(AssertionError):
            CardTestingMethods.default_test_card_intent_simulation(
                intents,
                self.CARD_TO_TEST,
                [
                    simulate_gameplay.startRound(),
                    simulate_gameplay.dinoTurnStart(),
                    simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
                ]
            )

    def test_missing_intents_still_successful(self):
        """
        If we have partial, yet nevertheless still correctly ordered intents, are we successful?
        """
        intents = [
            intent.entity_play_card_intent_factory("Trampled Rodent"),
            # ...
            intent.card_function_arbitrarily_discard_card_from_location_intent_factory(h.CARD_LOCATION_HAND, True)
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )

        