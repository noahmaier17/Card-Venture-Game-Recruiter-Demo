"""
test_fallow_farmland_cards.py

Tests all Fallow Farmland Cards, comparing what happens when played/packed against expected logging.
"""

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.dino_cards_depot import fallow_farmland_cards
from Dinosaur_Venture.entities import entity as e
from Dinosaur_Venture.logging import intent
from tests.test_utils import simulate_gameplay
from tests.test_utils.card_tester_class import CardTestingMethods, TestCard

'''
class TestBrassMuzzle(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.brassMuzzle

    def test_on_play(self):
        """Tests on play of Brass Muzzle."""
        intents = [
            intent.entity_play_card_intent_factory("Brass Muzzle"),
            intent.entity_damage_intent_factory(
                cll.Attackcons([2, cll.B()],
                cll.Attackcons([2, cll.M()],
                'nil'))
            ),
        ]
'''

class TestRustedScythe(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.rustedScythe

    CORE_ON_PLAY_INTENTS = [
        intent.entity_play_card_intent_factory("Rusted Scythe"),
        intent.entity_damage_intent_factory(
            cll.Attackcons([2, cll.Rnotick()],
            cll.Attackcons([2, cll.M()],
            'nil'))
        ),
        intent.helper_function_yes_or_no_intent_factory("Discard your Hand for +2 Cards?")
    ]
    CORE_SCRIPTED_INPUT = [1, 1]

    def test_on_play_yes_path(self):
        """
        Tests on play of Rusted Scythe when 'yes' is input to discarding your hand for +2 Cards.
        """
        intents = (
            self.CORE_ON_PLAY_INTENTS + 
            intent.entity_draw_several_cards_intent_factories(2) +
            [intent.entity_draw_card_intent_factory()]
        )

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput(
                    self.CORE_SCRIPTED_INPUT + ["yes"]))
            ]
        )

    def test_on_play_no_path(self):
        """
        Tests on play of Rusted Scythe when 'no' is input to discarding your hand for +2 Cards.
        """
        intents = (
            self.CORE_ON_PLAY_INTENTS + 
            [intent.entity_draw_card_intent_factory()]
        )

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput(
                    self.CORE_SCRIPTED_INPUT + ["no"]))
            ]
        )
  

class TestCultivator(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.cultivator

    def test_on_play(self):
        """Tests on play of Cultivator."""
        # We need an instance of dino and the card so we can test card movement
        dino = e.Entity()
        card_to_test = self.CARD_TO_TEST()

        intents = [
            intent.entity_play_card_intent_factory("Cultivator"),
            intent.entity_damage_intent_factory(
                cll.Attackcons([1, cll.M()], 
                cll.Attackcons([1, cll.M()], 
                               'nil'))
            ),
            intent.entity_move_me_intent_factory(
                dino.play,
                card_to_test,
                dino.draw,
                0
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            card_to_test,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ],
            dino = dino
        )
    
    def test_on_packing(self):
        """Tests packing of Cultivator."""
        dino = e.Entity()

        intents = [
            intent.entity_packing_card_intent_factory("Cultivator"),
            intent.entity_draw_card_intent_factory(
                to_location=dino.intoHand
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPackingCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ],
            dino = dino
        )

class TestGnawedCableCord(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.gnawedCableCord

    def test_on_play(self):
        """Tests on play of Gnawed Cable Cord."""
        # We need an instance of dino and the card so we can test card movement
        dino = e.Entity()
        card_to_test = self.CARD_TO_TEST()

        intents = [
            intent.entity_play_card_intent_factory("Gnawed Cable Cord"),
            intent.entity_plus_actions_intent_factory(2),
            intent.entity_damage_intent_factory(
                cll.Attackcons([2, cll.Bnotick()], 'nil')
            ),
            intent.entity_move_me_intent_factory(
                dino.play,
                card_to_test,
                dino.draw,
                0
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            card_to_test,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ],
            dino = dino
        )

    def test_on_packing(self):
        """Tests packing of Gnawed Cable Cord."""
        dino = e.Entity()

        intents = [
            intent.entity_packing_card_intent_factory("Gnawed Cable Cord"),
            intent.entity_draw_card_intent_factory(
                to_location=dino.intoHand
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPackingCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ],
            dino = dino
        )

class TestGrasshopperCache(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.grasshopperCache

    def test_on_play(self):
        """Tests on play of Grasshopper Cache."""
        intents = [
            intent.entity_play_card_intent_factory("Grasshopper Cache"),
            intent.card_function_draw_until_you_have_x_cards_in_hand_intent_factory(3)
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1]))
            ]
        )

    def test_on_packing(self):
        "Tests packing of Grasshopper Cache."
        intents = [
            intent.entity_packing_card_intent_factory("Grasshopper Cache"),
            intent.entity_damage_intent_factory(
                cll.Attackcons([2, cll.Gnotick()],
                cll.Attackcons([2, cll.M()],
                'nil'))
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPackingCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )

class TestDeadHarvestedGrass(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.deadHarvestedGrass

    def test_on_play(self):
        """Tests on play of Dead Harvested Grass."""
        intents = [
            intent.entity_play_card_intent_factory("Dead Harvested Grass"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(cll.Attackcons([3, cll.G()], 'nil')),
            intent.entity_damage_intent_factory(cll.Attackcons([3, cll.L()], 'nil')),
            intent.card_function_draw_until_you_have_x_cards_in_hand_intent_factory(1)
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1, 1]))
            ]
        )

class TestTrampledRodent(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.trampledRodent

    def test_on_play(self):
        """Tests on play of Trampled Rodent."""
        # We need an instance of dino and the card so we can test card movement
        dino = e.Entity()

        intents = [
            intent.entity_play_card_intent_factory("Trampled Rodent"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(
                cll.Attackcons([1, cll.Rnotick()],
                cll.Attackcons([1, cll.Gnotick()],
                cll.Attackcons([1, cll.Bnotick()],
                cll.Attackcons([1, cll.M()],
                'nil'))))
            ),
            # Per the Trampled Rodent class, we have input=True for this card function and we will test for that
            intent.card_function_arbitrarily_discard_card_from_location_intent_factory(dino.hand, True)
        ]
        
        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ], 
            dino = dino
        )

class TestMangledShrew(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.mangledShrew

    def test_on_play(self):
        """Tests on play of Mangled Shrew."""
        intents = [
            intent.entity_play_card_intent_factory("Mangled Shrew"),
            intent.entity_damage_intent_factory(
                cll.Attackcons([2, cll.Rnotick()],
                cll.Attackcons([1, cll.Filled()],
                cll.Attackcons([1, cll.Filled()],
                cll.Attackcons([1, cll.Filled()],
                'nil'))))
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )

class TestLastSeeds(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.lastSeeds

    def test_on_play(self):
        "Tests on play of Last Seeds."
        intents = [
            intent.entity_play_card_intent_factory("Last Seeds"),
            intent.entity_plus_actions_intent_factory(1),
            intent.entity_damage_intent_factory(
                cll.Attackcons([9, cll.L()], 'nil')
            ),
            intent.entity_draw_card_intent_factory()
        ]
    
        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
    )

class TestTwigRockScarecrow(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.twigRockScarecrow

    def test_on_play(self):
        """Tests on play of Twig-Rock Scarecrow."""
        dino = e.Entity()
        card_to_test = self.CARD_TO_TEST()

        intents = [
            intent.entity_play_card_intent_factory("Twig-Rock Scarecrow"),
            intent.entity_plus_upcoming_plus_action_intent_factory(0, 1),
            intent.entity_plus_upcoming_plus_card_intent_factory(0, 1),
            intent.entity_move_me_intent_factory(
                dino.play,
                card_to_test,
                dino.draw,
                0
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            card_to_test,
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1]))
            ],
            dino = dino
        )
    
    def test_on_packing(self):
        """Tests packing of Twig-Rock Scarecrow."""
        intents = [
            intent.entity_packing_card_intent_factory("Twig-Rock Scarecrow"),
            intent.entity_damage_intent_factory(
                cll.Attackcons([1, cll.Random()],
                cll.Attackcons([1, cll.Random()],
                'nil'))
            )
        ]

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPackingCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )
