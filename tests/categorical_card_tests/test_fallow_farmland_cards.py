"""
test_fallow_farmland_cards.py

Tests all Fallow Farmland Cards, comparing what happens when played/packed against expected logging.
"""

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture.dino_cards_depot import fallow_farmland_cards
from Dinosaur_Venture.entities import entity as e
from Dinosaur_Venture.logging import intent
from tests.test_utils import simulate_gameplay
from tests.test_utils.card_tester_class import CardTestingMethods, TestCard

class TestBrassMuzzle(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.brassMuzzle

    def test_on_play(self):
        """Tests on play of Brass Muzzle."""
        # We need access to the enemies to check if a card was discarded
        _, enemies, _ = CardTestingMethods.default_dino_enemies_clearing_getter()

        # We will attack the front-most enemy

        intents = (
            intent.EntityFactory.play_card("Brass Muzzle") +
            intent.HelperFactory.pick_living_enemy("Pick Enemy") +
            intent.EntityFactory.damage(
                cll.Attackcons([2, cll.B()],
                cll.Attackcons([2, cll.M()],
                'nil'))
            ) +
            intent.EntityFactory.discard_card(enemies[0].hand, False, False)
        )

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPlayCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ],
            enemies=enemies
        )

class TestRustedScythe(TestCard):
    CARD_TO_TEST = fallow_farmland_cards.rustedScythe

    CORE_ON_PLAY_INTENTS = (
        intent.EntityFactory.play_card("Rusted Scythe") +
        intent.EntityFactory.damage(
            cll.Attackcons([2, cll.Rnotick()],
            cll.Attackcons([2, cll.M()],
            'nil'))
        ) +
        intent.HelperFactory.yes_or_no("Discard your Hand for +1 Card?")
    )
    CORE_SCRIPTED_INPUT = [1, 1]

    def test_on_play_yes_path(self):
        """
        Tests on play of Rusted Scythe when 'yes' is input to discarding your hand for +1 Card.
        """
        intents = (self.CORE_ON_PLAY_INTENTS +
            intent.CardFunctionFactory.discard_your_hand() +
            intent.EntityFactory.draw_card() +
            intent.EntityFactory.draw_card()
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
        Tests on play of Rusted Scythe when 'no' is input to discarding your hand for +1 Card.
        """
        intents = (
            self.CORE_ON_PLAY_INTENTS + 
            intent.EntityFactory.draw_card()
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

        intents = (
            intent.EntityFactory.play_card("Cultivator") +
            intent.EntityFactory.damage(
                cll.Attackcons([1, cll.M()], 
                cll.Attackcons([1, cll.M()], 
                               'nil'))
            ) +
            intent.EntityFactory.move_me(
                dino.play,
                card_to_test,
                dino.draw,
                0
            )
        )

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

        intents = (
            intent.EntityFactory.packing_card("Cultivator") +
            intent.EntityFactory.draw_card(
                to_location=dino.intoHand
            )
        )

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

        intents = (
            intent.EntityFactory.play_card("Gnawed Cable Cord") +
            intent.EntityFactory.plus_actions(2) +
            intent.EntityFactory.damage(
                cll.Attackcons([2, cll.Bnotick()], 'nil')
            ) +
            intent.EntityFactory.move_me(
                dino.play,
                card_to_test,
                dino.draw,
                0
            )
        )

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

        intents = (
            intent.EntityFactory.packing_card("Gnawed Cable Cord") +
            intent.EntityFactory.draw_card(
                to_location=dino.intoHand
            )
        )

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
        intents = (
            intent.EntityFactory.play_card("Grasshopper Cache") +
            intent.CardFunctionFactory.draw_until_you_have_x_cards_in_hand(3)
        )

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
        intents = (
            intent.EntityFactory.packing_card("Grasshopper Cache") +
            intent.EntityFactory.damage(
                cll.Attackcons([2, cll.Gnotick()],
                cll.Attackcons([2, cll.M()],
                'nil'))
            )
        )

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
        intents = (
            intent.EntityFactory.play_card("Dead Harvested Grass") +
            intent.EntityFactory.plus_actions(1) +
            intent.EntityFactory.damage(cll.Attackcons([3, cll.G()], 'nil')) +
            intent.EntityFactory.damage(cll.Attackcons([3, cll.L()], 'nil')) +
            intent.CardFunctionFactory.draw_until_you_have_x_cards_in_hand(1)
        )

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

        intents = (
            intent.EntityFactory.play_card("Trampled Rodent") +
            intent.EntityFactory.plus_actions(1) +
            intent.EntityFactory.damage(
                cll.Attackcons([1, cll.Rnotick()],
                cll.Attackcons([1, cll.Gnotick()],
                cll.Attackcons([1, cll.Bnotick()],
                cll.Attackcons([1, cll.M()],
                'nil'))))
            ) +
            # Per the Trampled Rodent class, we have input=True for this card function and we will test for that
            intent.CardFunctionFactory.arbitrarily_discard_card_from_location(dino.hand, True)
        )
        
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
        intents = (
            intent.EntityFactory.play_card("Mangled Shrew") +
            intent.EntityFactory.damage(
                cll.Attackcons([2, cll.Rnotick()],
                cll.Attackcons([1, cll.Filled()],
                cll.Attackcons([1, cll.Filled()],
                cll.Attackcons([1, cll.Filled()],
                'nil'))))
            )
        )

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
        intents = (
            intent.EntityFactory.play_card("Last Seeds") +
            intent.EntityFactory.plus_actions(1) +
            intent.EntityFactory.damage(
                cll.Attackcons([9, cll.L()], 'nil')
            ) +
            intent.EntityFactory.draw_card()
        )
    
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

        intents = (
            intent.EntityFactory.play_card("Twig-Rock Scarecrow") +
            intent.EntityFactory.plus_upcoming_plus_action(0, 1) +
            intent.EntityFactory.plus_upcoming_plus_card(0, 1) +
            intent.EntityFactory.move_me(
                dino.play,
                card_to_test,
                dino.draw,
                0
            )
        )

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
        intents = (
            intent.EntityFactory.packing_card("Twig-Rock Scarecrow") +
            intent.EntityFactory.damage(
                cll.Attackcons([1, cll.Random()],
                cll.Attackcons([1, cll.Random()],
                'nil'))
            )
        )

        CardTestingMethods.default_test_card_intent_simulation(
            intents,
            self.CARD_TO_TEST(),
            [
                simulate_gameplay.startRound(),
                simulate_gameplay.dinoTurnStart(),
                simulate_gameplay.dinoPackingCard(scriptedInput=scriptInput.gameplayScriptInput([1, 1]))
            ]
        )
