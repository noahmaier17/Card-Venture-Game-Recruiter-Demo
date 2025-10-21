import copy
import random

from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import cardModFunctions as cmf
from Dinosaur_Venture import cardTokens as tk
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis
from Dinosaur_Venture import react as r
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    SHOP CARDS
'''

## Nothing Cards are a special type of Cards; they function the same
class purge(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Purge"
        self.bodyText = c.bb("> Change the Body Text of this to: + Cantrip.")
        # self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "PURGED " + cardToEnshell.name
        cardToEnshell.purgeThrowText(cf.shellTextWrapper("+ Cantrip.", cf.plusCantrip()))

    '''
    def onLooted(self, dino):
        preamble = []
        index = 1
        for card in dino.deck.getArray():
            preamble.append(str(index) + ": ^" + card.name + "^.")
            index += 1

        pick = h.pickValue("Pick a Card in Deck to Change its Body Text to: + Cantrip.", range(1, index), preamble = preamble) - 1
        card = dino.deck.at(pick)
        card.name = "Purged " + card.name
        card.purgeThrowText(cf.shellTextWrapper("+ Cantrip.", cf.plusCantrip()))
    '''

class persevere(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Persevere"
        self.bodyText = c.bb("~ At Rest Stops, heal by an extra 1R / 1G / 1B.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        dino.resetR += 1
        dino.resetG += 1
        dino.resetB += 1
        h.splash("+1R Max Health, +1G Max Health, +1B Max Health.")

class proliferate(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Proliferate"
        self.bodyText = c.bb("~ -1 Looting. Gain a copy of a Card in Deck.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        dino.looting = -1

        preamble = []
        index = 1
        for card in dino.deck.getArray():
            preamble.append(str(index) + ": ^" + card.name + "^.")
            index += 1

        pick = h.pickValue("Pick a Card in Deck to Gain a Copy of", range(1, index), preamble = preamble) - 1
        card = copy.deepcopy(dino.deck.at(pick))
        card.name = "COPY OF " + card.name
        dino.gainCard(card, dino.deck)

'''
class rampage(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "Rampage"
        self.bodyText = c.bb("> Destroy a Card in Deck. Gain a Muck-type Card, that is initialized to Deck, and that reads: + Cantrip.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]
'''

class ransack(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Ransack"
        self.bodyText = c.bb("~ -1 Looting. Arbitrarily Pick 3 Tier-I Cards; Loot 1 of them.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        dino.looting -= 1

        purgeLocation = gcbt.getCardsByTable(gcbt.TIER_1_TABLES)

        for card in purgeLocation.getArray():
            card.mustDestroyCardWhenLooted = False

        h.selectCard(dino, "Ransacked Spoils", 0, [purgeLocation], [3], lootVacuously = True)

class renovate(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Renovate"
        self.bodyText = c.bb("~ To an Arbitrary Card in Deck, Enshell it as follows: //    > Shell this. +1 Action. //    > ...")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        value = random.randint(0, dino.deck.length() - 1)
        cardToEnshell = dino.deck.at(value)
        h.splash("The Card picked to Renovate is: ^" + cardToEnshell.name + "^.")
        cardToEnshell.name = "RENOVATED " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("+1 Action.", cf.plusXActions(1)))
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Shell this.", cf.shellThis(), excludeLineBreak = True))

class twig(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Twig"
        self.bodyText = c.bb("+2 Cards.")
        self.publishRoundStart("0.5 Chance to Enshell this as follows: //    > +1 Action. //    > ...")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(2):
                caster.drawCard()

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        if cf.chance(0.5, onSuccess_printInsteadOfInput = True).func(self, caster, dino, enemies, passedInVisuals):
            formerName = self.name
            self.name += "!"
            self.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("+1 Action.", cf.plusXActions(1), excludeLineBreak = True))
            h.splash("^" + formerName + "^ is now ^" + self.name + "^.")

class leavesRake(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Leaves Rake"
        self.bodyText = c.bb("+1 Action. Discard your Hand, then +3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            for i in range(3):
                caster.drawCard()

class snowShovel(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Snow Shovel"
        self.bodyText = c.bb("+1 Action. Draw until you have 2 Cards in Hand. +1 Card.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            priorLength = -1
            while caster.hand.lengthExcludingFeathery() < 2 and caster.hand.length() != priorLength:
                priorLength = caster.hand.length()
                caster.drawCard()
            caster.drawCard()

class firewoodAxe(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Firewood Axe"
        self.bodyText = c.bb("+ Cantrip. Next Turn, +1 Card.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            caster.drawCard()

            caster.plusUpcomingPlusCard(0, 1)

class rock(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rock"
        self.bodyText = c.bb("+2 Actions.")
        self.publishRoundStart("0.5 Chance to Enshell this as follows: //    > ... //    > +1 Card.")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        if cf.chance(0.5, onSuccess_printInsteadOfInput = True).func(self, caster, dino, enemies, passedInVisuals):
            formerName = self.name
            self.name += "!"
            self.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("+1 Card.", cf.plusXCards(1)))
            h.splash("^" + formerName + "^ is now ^" + self.name + "^.")

class stick(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Stick"
        self.bodyText = c.bb("+3 Cards.")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(3):
                caster.drawCard()

'''
class morningMantra(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Morning Mantra"
        self.bodyText = c.bb("~ Draw 1 More Card for your 1st Hand.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        dino.publishPermanentPlusCard(0, 1)

class afternoonMantra(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Afternoon Mantra"
        self.bodyText = c.bb("~ Draw 1 More Card for your 2nd Hand.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        dino.publishPermanentPlusCard(1, 1)

class eveningMantra(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Evening Mantra"
        self.bodyText = c.bb("~ Draw 1 More Card for your 3rd Hand.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        dino.publishPermanentPlusCard(2, 1)

class nightMantra(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Night Mantra"
        self.bodyText = c.bb("~ Draw 1 More Card for your 4th through 9th Hand.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        for i in range(4, 9 + 1):
            dino.publishPermanentPlusCard(i, 1)
'''

class muscles(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Muscles"
        self.bodyText = c.bb("+1 Action. 1Random. +1 Card.")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'Random'], 'nil'))
            caster.drawCard()

class magicalFeather(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Feather"
        self.bodyText = c.bb("> Entoken this with: <<feathery>>.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "FEATHERED " + cardToEnshell.name
        cardToEnshell.publishToken(tk.feathery())

class magicalPocketWatch(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Pocket Watch"
        self.bodyText = c.bb("> Change the Packing Text of this to: //> |>| Pocket this.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "POCKET-WATCHED " + cardToEnshell.name
        cardToEnshell.purgePackingText(cf.shellTextWrapper("Pocket this.", cf.packingText_PocketThis()))

class magicalCounterWeight(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Counter Weight"
        self.bodyText = c.bb("> ... //> At Turn End, you may: 0.25 Chance to reduce heaviness to { 0H }.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "COUNTER-WEIGHTED " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("At Turn End, you may: 0.25 Chance to reduce heaviness to { 0H }.", cf.dots()))
        cardToEnshell.triggers.append(r.reaction(cardToEnshell, True, self.trigger_1(cardToEnshell)))

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^", "",
                                            "0.25 Chance to reduce heaviness to { 0H }")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            if cf.chance(0.25).func(card, caster, dino, enemies, vis.prefabEmpty):
                card.reduceLingering(0)
                ## caster.discardMe(caster.play, card, dino, enemies, vis.prefabEmpty)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class magicalReassortment(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Reassortment"
        self.bodyText = c.bb("> Change this to: < iTop >.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "REASSORTED " + cardToEnshell.name
        cardToEnshell.publishReshuffle(top = True)

class magicalAssortment(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Assortment"
        self.bodyText = c.bb("> Change this to: [ iTop ].")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "ASSORTED " + cardToEnshell.name
        cardToEnshell.publishInitialization(top = True)

class liquidation(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Liquidation"
        self.bodyText = c.bb("~ Trash a Destructable Card in Deck. Loot an Arbitrary Tier-I Card.")
        self.mustEnshellCardWhenLooted = False
        self.table = ["Shop"]

    def onLooted(self, dino):
        preamble = []
        incrementTable = []
        index = 1
        for card in dino.deck.getArray():
            if card.destructable:
                preamble.append(str(index) + ": ^" + card.name + "^.")
                incrementTable.append(0)
            else:
                incrementTable.append(1)
            index += 1

        pick = h.pickValue("Pick a Card in Deck to Trash", range(1, index), preamble = preamble) - 1
        pick += sum(incrementTable[0:pick])
        dino.deck.pop(pick)

        purgeLocation = gcbt.getCardsByTable(gcbt.TIER_1_TABLES)
        for card in purgeLocation.getArray():
            card.mustDestroyCardWhenLooted = False
        h.selectCard(dino, "Liquidated Card", 0, [purgeLocation], [1], lootVacuously = True)

'''
class test01(DinoCard):
    def __init__(self):
        super
        super().__init__()
        self.name = "Spiteful"
        self.bodyText = c.bb("Enbadge with 'Spite Sickness'.")
        self.table = ["Debug"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.cmfDepot.append(cmf.dealDamage_dropNotick())
'''

class badFortune(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "Bad Fortune"
        self.bodyText = c.bb("> Change this' Chance values to 0.15.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "UNLUCKY " + cardToEnshell.name

        cardModifierFunction = cmf.chance_modifyChance(0.15)
        cardToEnshell.cmfDepot.append(cardModifierFunction)
        cardModifierFunction.mutateCardBodyText(cardToEnshell)

class goodFortune(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "Good Fortune"
        self.bodyText = c.bb("> Change this' Chance values to 0.85.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "LUCKY " + cardToEnshell.name

        cardModifierFunction = cmf.chance_modifyChance(0.85)
        cardToEnshell.cmfDepot.append(cardModifierFunction)
        cardModifierFunction.mutateCardBodyText(cardToEnshell)

class bolster(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "Bolster"
        self.bodyText = c.bb("> Change this' #x and x# values to 4.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "BOLSTERED " + cardToEnshell.name

        cardModifierFunction = cmf.getter_numberX_modifyX(4)
        cardToEnshell.cmfDepot.append(cardModifierFunction)
        cardModifierFunction.mutateCardBodyText(cardToEnshell)