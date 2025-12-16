from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture.dino_cards_depot import fallow_farmland_cards
from Dinosaur_Venture.logging import intent
from tests.test_utils import simulate_gameplay
from tests.test_utils.card_tester_class import CARD_TESTING_METHODS, TestCard
# from tests.test_utils.game_setups import (getCartesianProduct_anyInput,
#                                           setup_getDinoEnemiesClearing)


# DINOES, ENEMIESES, CLEARINGSES = setup_getDinoEnemiesClearing()
# DINOES_ENEMIESES_CLEARINGSES = getCartesianProduct_anyInput([DINOES, ENEMIESES, CLEARINGSES])

class TestDeadHarvestedGrass(TestCard):
    def test_on_play(self):
        INTENT = [
            intent.entity_play_card_intent_factory("Dead Harvested Grass"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(cll.Attackcons([3, cll.G()], 'nil')),
            intent.entity_damage_intent_factory(cll.Attackcons([3, cll.L()], 'nil')),
            intent.card_function_draw_until_you_have_x_cards_in_hand_intent_factory(1)
        ]

        CARD_TO_TEST = fallow_farmland_cards.deadHarvestedGrass

        CARD_TESTING_METHODS.default_test_card_intent_on_play(
            INTENT,
            CARD_TO_TEST,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1, 1]))
            ]
        )

class TestTrampledRodent(TestCard):
    def test_on_play(self):
        INTENT = [
            intent.entity_play_card_intent_factory("Trampled Rodent"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(
                cll.Attackcons([1, cll.Rnotick()],
                cll.Attackcons([1, cll.Gnotick()],
                cll.Attackcons([1, cll.Bnotick()],
                cll.Attackcons([1, cll.M()],
                'nil'))))
            )
        ]

        CARD_TO_TEST = fallow_farmland_cards.trampledRodent
        
        CARD_TESTING_METHODS.default_test_card_intent_on_play(
            INTENT,
            CARD_TO_TEST,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )

class TestMangledShrew(TestCard):
    def test_on_play(self):
        INTENT = [
            intent.entity_play_card_intent_factory("Mangled Shrew"),
            intent.entity_damage_intent_factory(
                cll.Attackcons([2, cll.Rnotick()],
                cll.Attackcons([1, cll.Filled()],
                cll.Attackcons([1, cll.Filled()],
                cll.Attackcons([1, cll.Filled()],
                'nil'))))
            )
        ]

        CARD_TO_TEST = fallow_farmland_cards.mangledShrew

        CARD_TESTING_METHODS.default_test_card_intent_on_play(
            INTENT,
            CARD_TO_TEST,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )