import random
import re

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
    The Pier
'''

class fishFry(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fish Fry"
        self.bodyText = c.bb("+3 Actions. You can no longer gain Actions this Turn. //Gain a ^Fish^ into Hand.")
        self.publishPacking("Move this onto Draw.")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(3)
            caster.canGainActionsThisTurn = False
            for i in range(1):
                caster.gainCard(gcbt.getCardByName("Fish"), caster.hand, position = caster.hand.length())

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            success = caster.moveMe(caster.hand, card, caster.draw, suppressFailText = True)
            if not success:
                caster.moveMe(caster.pocket, card, caster.draw)

class sleepingWithTheFishes(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Sleeping With The Fishes"
        self.bodyText = c.bb("+2 Cards. Per Carcass, Gain a ^Fish^.")
        self.publishPacking("Move this onto Draw.")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(2):
                caster.drawCard()

            anyDeadEnemies = False
            for enemy in enemies:
                if enemy.dead:
                    anyDeadEnemies = True
                    h.splash("'" + enemy.name + "' is a Carcass, so: Gaining a ^Fish^.", printInsteadOfInput = True)
                    caster.gainCard(gcbt.getCardByName("Fish"), caster.discard)
            if anyDeadEnemies:
                input(" ... ")

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            success = caster.moveMe(caster.hand, card, caster.draw, suppressFailText = True)
            if not success:
                caster.moveMe(caster.pocket, card, caster.draw)

class tackleBox(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tackle Box"
        self.bodyText = c.bb("+ Cantrip. //At Every Turn End, per ^Junk^ in Play: Gain a ^Fish^ onto Draw.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.detritusCount = 0

        def response(self, card, caster, dino, enemies, moments):
            ## Resets variables
            self.detritusCount = 0

            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            ## Have we reacted already?
            if (self.reacted_1):
                return (False, r.EMPTY_RT)

            ## Sees if Card is in desired Location
            if h.locateCardIndex(caster.play, card) >= 0:
                ## Sees if Card there exists a Detritus in Play
                for cardInPlay in caster.play.getArray():
                    if (cardInPlay.unmodifiedName == "Junk"):
                        self.detritusCount += 1
            
            SUCCESSFUL_RT = r.rt(False,
                                 "^" + card.name + "^",
                                 str(self.detritusCount) + " ^Junk^ in Play",
                                 "Gain " + str(self.detritusCount * 1) + " ^Fish^ onto Draw")

            return (self.detritusCount >= 1, SUCCESSFUL_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            for i in range(self.detritusCount):
                for j in range(1):
                    caster.gainCard(gcbt.getCardByName("Fish"), caster.draw)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class goneFishing(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Gone Fishing"
        self.bodyText = c.bb("At Every Turn End, per Remaining Action: Gain a ^Fish^.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.countedActions = 0

        def response(self, card, caster, dino, enemies, moments):
            ## Resets variables
            self.countedActions = 0

            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            ## Have we reacted already?
            if (self.reacted_1):
                return (False, r.EMPTY_RT)

            ## Sees if Card is in desired Location
            if not h.locateCardIndex(caster.play, card) >= 0:
                return (False, r.EMPTY_RT)

            self.countedActions = caster.actions
            SUCCESSFUL_RT = r.rt(False,
                                 "^" + card.name + "^",
                                 str(caster.actions) + " Remaining Action(s)",
                                 "Gain " + str(caster.actions) + " ^Fish^")

            return (True, SUCCESSFUL_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            for i in range(self.countedActions):
                caster.gainCard(gcbt.getCardByName("Fish"), caster.discard)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class weatheredBoat(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Weathered Boat"
        self.bodyText = c.bb("+1 Action. +2 Cards.")
        self.publishPacking("Remove <<inoperable>> from this.")
        self.publishRoundStart("Entoken this with <<inoperable>>.")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            for i in range(2):
                caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.removeToken(tk.inoperable())

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        self.publishToken(tk.inoperable())

class fishPot(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fish Pot"
        self.bodyText = c.bb("2R / 2M. //Mill, Unless a Card with '_L' in body-text is found; Move such a Card into Hand. Then, Immill.")
        self.bodyText.lootingText("Gain a [ iMuck ] ^Fish^.")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def custom_checkClause(self, card):
            text = card.bodyText.unpacking + " " + card.bodyText.core + " " + card.bodyText.packing
            LDamageMatchObject = re.search("(\\d)L", text)
            return (LDamageMatchObject != None)

        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'R'],
                                                                               cll.Attackcons([2, 'M'],
                                                                               'nil')))

            millCardFunction = cf.mill(usingCheckClause = True, checkClause = self.custom_checkClause)

            matchingCard = millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals, inputMatchCard = True)
            if matchingCard != 'NO MATCHES':
                caster.moveMe(millCardFunction.toLocation, matchingCard, caster.hand, position = caster.hand.length())
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

    def onLooted(self, dino):
        toAddCard = gcbt.getCardByName("Fish")
        toAddCard.publishInitialization(muck = True)
        dino.gainCard(toAddCard, dino.deck)

class dipNetting(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dip Netting"
        self.bodyText = c.bb("To the Frontmost Enemy with 2+ Bands: Break a Band.")
        self.publishPacking("Entoken this with <<feathery>> and <<inoperable>>.")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            index = -1
            for i in range(len(enemies)):
                if not enemies[i].dead and enemies[i].hp.getBands() >= 2:
                    index = i
                    break

            if index == -1:
                h.splash('FAIL_FIND_ENEMY')
            else:
                enemy = enemies[index]
                enemy.destroyBand(dino, enemies)
                h.splash("To '" + enemy.name + "': Broke a Band.", printInsteadOfInput = True)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.publishToken(tk.feathery())
            card.publishToken(tk.inoperable())

class useJunkAsBait(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//rune// Use Junk as Bait"
        self.bodyText = c.bb("~ To an Arbitrary [ iMuck ] or < iMuck > Card, Enshell it as follows: //    > Shell this. Gain 4 ^Fish^. //    > ...")
        self.mustEnshellCardWhenLooted = False
        self.table = ["The Pier"]

    def onLooted(self, dino):
        setOfCards = []
        for card in dino.deck.getArray():
            if card.initialized == "Muck" or card.reshuffleLocation == "Muck":
                setOfCards.append(card)

        if len(setOfCards) == 0:
            h.splash('FAIL_FIND_CARD')
            return

        value = random.randint(0, len(setOfCards) - 1)

        cardToEnshell = setOfCards[value]
        h.splash("The Card picked as Bait is: ^" + cardToEnshell.name + "^.")
        cardToEnshell.name = "USED-FOR-BAIT " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Gain 4 ^Fish^.", self.customAboveTextFunction()))
        ## cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("+1 Action.", cf.plusXActions(1), excludeLineBreak = True))
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Shell this.", cf.shellThis(), excludeLineBreak = True))

    class customAboveTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(4):
                caster.gainCard(gcbt.getCardByName("Fish"), caster.discard)

class tangledFishLine(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tangled Fish Line"
        self.bodyText = c.bb("+2 Actions. Gain 2 ^Fish^ into Hand.")
        self.publishPacking("{ 5H }.")
        self.DOLLAR_TRIGGER_1 = "When Discarded (EXCEPT at Turn-End Tidying from Hand), remove <<inoperable>> and this Trigger from this."
        self.publishDollarTrigger(self.DOLLAR_TRIGGER_1)
        self.publishToken(tk.inoperable())
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)
            for i in range(2):
                caster.gainCard(gcbt.getCardByName("Fish"), caster.hand, position = caster.hand.length())

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(5)

            success = caster.moveMe(caster.hand, card, caster.play, suppressFailText = True)
            if not success:
                success = caster.moveMe(caster.pocket, card, caster.play)

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            ## Any moment is correct

            ## Fetches the fromLocation and card
            moment_discardedCard = r.moments_fetchInRight([r.DiscardedCard], moments)
            if moment_discardedCard == None:
                return (False, r.EMPTY_RT)

            ## Was this card the discarded card?
            if moment_discardedCard.cardThatWasDiscarded != card:
                return (False, r.EMPTY_RT)

            ## Did we discard at Turn End Tidying from Hand?
            if "hand" == moment_discardedCard.fromLocation.name and r.moments_isLeftInRight([r.AtTurnEndTidying], moments):
                return (False, r.EMPTY_RT)

            on_discard_rt = r.rt(False,
                                 "^" + card.name + "^", "Discarded from " + moment_discardedCard.fromLocation.niceName(),
                                 "Remove <<inoperable>> and this Trigger")

            return (h.locateCardIndex(caster.discard, card) >= 0 
                and tk.checkTokensOnThis(card, [tk.inoperable()])
                and self.reacted_1 == False,
                    on_discard_rt)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            card.removeToken(tk.inoperable())
            card.removeDollarTrigger(self, caster, dino, enemies, card.DOLLAR_TRIGGER_1)

class disphoticFishZone(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Disphotic Fish Zone"
        self.bodyText = c.bb("+1 Action. Per Card in Hand below 3, Gain a ^Fish^ to Hand. //Entoken this with <<inoperable>>.")
        self.publishInitialization(pocket = True)
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cardsInHand = caster.hand.length()
            if cardsInHand >= 3:
                h.splash("With " + str(cardsInHand) + " Cards in Hand: Gained no ^Fish^ to Hand.")
            else:
                difference = 3 - cardsInHand
                for i in range(difference):
                    caster.gainCard(gcbt.getCardByName("Fish"), caster.hand, position = caster.hand.length())
                h.splash("With " + str(cardsInHand) + " Card(s) in Hand: Gained " + str(difference) + " ^Fish^ to Hand.")

            card.publishToken(tk.inoperable())

class aphoticFishZone(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Aphotic Fish Zone"
        self.bodyText = c.bb("+1 Action. Per Card in Hand below 5, Gain a ^Fish^.")
        self.publishPacking("Pocket this.")
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cardsInHand = caster.hand.length()
            if cardsInHand >= 5:
                h.splash("With " + str(cardsInHand) + " Cards in Hand: Gained no ^Fish^.")
            else:
                difference = 5 - cardsInHand
                for i in range(difference):
                    caster.gainCard(gcbt.getCardByName("Fish"), caster.discard)
                h.splash("With " + str(cardsInHand) + " Card(s) in Hand: Gained " + str(difference) + " ^Fish^.")

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.packingText_PocketThis().func(card, caster, dino, enemies, passedInVisuals)

class rustyNetCutter(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rusty Net Cutter"
        self.bodyText = c.bb("Does Nothing.")
        self.publishDollarTrigger("WTI-Hand or Pocket, at your Turn End, Destroy this.")
        self.publishDollarTrigger("WTI-Hand or Pocket, when an Enemy dies, Gain 3 ^Fish^.")
        self.publishToken(tk.inoperable())
        self.table = ["The Pier"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self)))
        self.triggers.append(r.reaction(self, False, self.trigger_2(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            pass

    ## Trigger to Trash at Turn End
    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            ## Is this in Hand or Pocket?
            if not (h.locateCardIndex(caster.hand, card) >= 0 or h.locateCardIndex(caster.pocket, card) >= 0):
                return (False, r.EMPTY_RT)

            return (True, r.rt(False,
                               "^" + card.name + "^",
                               "This in Hand or Pocket",
                               "Destroy this"))

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            index = h.locateCardIndex(caster.hand, card)
            if index >= 0:
                caster.destroyCard(caster.hand, index)
                return
            index = h.locateCardIndex(caster.pocket, card)
            if index >= 0:
                caster.destroyCard(caster.pocket, index)
                return

    ## Trigger to Gain Fish
    class trigger_2(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            ## Any moment is fine

            ## Have we already reacted?
            if self.reacted_1:
                return (False, r.EMPTY_RT)

            ## Is this in Hand or Pocket?
            if not (h.locateCardIndex(caster.hand, card) >= 0 or h.locateCardIndex(caster.pocket, card) >= 0):
                return (False, r.EMPTY_RT)

            ## Was an enemy attacked fatally?
            moment_enemyAttacked = r.moments_fetchInRight([r.AfterEntityAttacked], moments)
            if moment_enemyAttacked == None:
                return (False, r.EMPTY_RT)
            if not moment_enemyAttacked.DamageData.fatalDamage:
                return (False, r.EMPTY_RT)

            return (True, r.rt(False,
                               "^" + card.name + "^",
                               "Enemy Died WTI-Hand or Pocket",
                               "Gain 3 ^Fish^"))

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            for i in range(3):
                    caster.gainCard(gcbt.getCardByName("Fish"), caster.discard)

        def resetState_AfterAfterEntityAttacked(self):
            self.reacted_1 = False
