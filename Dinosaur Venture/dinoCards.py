import math, random, os, copy
import card as c
import helper as h
import cardFunctions as cf
import cardModFunctions as cmf
import cardTokens as tk
import getCardsByTable as gcbt
import mainVisuals as vis
import re
import react as r
from colorama import init, Fore, Back, Style
init(autoreset=True)

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

## Dino Cards
class DinoCard(c.Card):
    def __init__(self):
        super().__init__()

## A special Dino Card type called \\Shell\\ Cards.
##  These are not gained to Dino's Deck, but instead modify one of Dino's already-existing Cards.
class DinoShellCard(c.Card):
    def __init__(self):
        super().__init__()
        self.isShellCard = True
        self.isGainedCard = False

        self.isConfidant = False

        self.mustDestroyCardWhenLooted = False
        self.mustEnshellCardWhenLooted = True

    def onLootedEnshelling(self, dino, cardToEnshell):
        # this just exists to make adding something easy (since it is already prepped)
        pass

''' 
    Debug/Testing Suite
'''
class draw6(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Draw 6"
        self.bodyText = c.bb("+6 Cards.")
        self.publishInitialization(top = True)
        self.table = ["Debug"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(6):
                caster.drawCard()

class drawAll(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Draw All"
        self.bodyText = c.bb("+20 Cards.")
        self.publishInitialization(top = True)
        self.table = ["Debug"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(20):
                caster.drawCard()

class pocketTest(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Pocket Test"
        self.bodyText = c.bb("Move this onto the Pocket Mat.")
        self.table = ["Debug"]
        self.publishInitialization(top = True)
        self.publishPacking("999M.")
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            index = h.locateCardIndex(caster.play, caster)
            if index >= 0:
                caster.moveCard(caster.play, index, caster.pocket, position = 0)
            else:
                h.splash('FAIL_MOVE')

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([999, 'M'], 'nil'))

class megaDamage(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "MEGA Damage"
        self.bodyText = c.bb("+1 Action. 10R / 10G / 10B. Pocket this.")
        self.table = ["Debug"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([10, 'R'],
                                                                 h.acons([10, 'G'],
                                                                 h.acons([10, 'B'],
                                                                 'nil'))))
            caster.moveMe(caster.play, card, caster.pocket)

'''
    Muck Cards
'''
class junk(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Junk"
        self.bodyText = c.bb("Do Nothing.")
        self.bodyText.heavinessText("{ 1H }")
        self.table = ["Muck"]
        self.publishInitialization(muck = True)
        self.destructable = False
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            h.splash(" Do Nothing. ", printInsteadOfInput = True)

class miscellany(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Miscellany"
        self.bodyText = c.bb("Do Nothing.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Muck"]
        self.publishInitialization(pocket = True)
        self.destructable = False
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            h.splash(" Do Nothing. ", printInsteadOfInput = True)

'''
    Cross-clearing Fundamental Cards
'''
class shovel(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shovel"
        self.bodyText = c.bb("||Temporary|| +1 Action. Discard your Hand, then +3 Cards. Destroy this.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            for i in range(3):
                caster.drawCard()

            cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals)

class rubbish(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rubbish"
        self.bodyText = c.bb("||Temporary|| { 3H } Do Nothing.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(3)
            h.splash(" Do Nothing. ", printInsteadOfInput = True)

class twigExclamation(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Twig!"
        self.bodyText = c.bb("+1 Action. +2 Cards.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            for i in range(2):
                caster.drawCard()

'''
    Copper Croppers
'''
class rebuildOrDestroy(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rebuild or Destroy"
        ## self.bodyText = c.bb("+ Cantrip. 2x, 0.25 Chance for: //(1) Draw 1 More Card for your Next Hand.")
        self.bodyText = c.bb("+3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.publishPacking("{ HH } To every Enemy: Discard a Card.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            ## caster.plusActions(1)
            for i in range(3):
                caster.drawCard()
            ## for i in range(2):
            ##     if cf.chance(0.25, onSuccess_printInsteadOfInput = True,
            ##                        onFailure_printInsteadOfInput = True).func(card, caster, dino, enemies, passedInVisuals):
            ##         caster.plusUpcomingPlusCard(0, 1)
            ## h.splash(" ... ")

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.toBlankEnemy_DiscardBlank_fromHand(numberOfCardsToDiscard = 1, toEveryEnemy = True).func(card, caster, dino, enemies, passedInVisuals)

class troughBoy(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trough Boy"
        self.bodyText = c.bb("+1 Action. 4B-notick.")
        self.publishPacking("{ HH } Break a Band.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([4, 'B-notick'], 'nil'))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.breakABand().func(card, caster, dino, enemies, passedInVisuals)

class collectiveBargaining(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Collective Bargaining"
        self.bodyText = c.bb("+1 Action. 2G. //At This Turn End, if you have 1+ Actions, you may: //(1) Plus 1 Action for your Next Turn.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, True, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'G'], 'nil'))

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^", "1+ Actions",
                                            "Plus 1 Action for your Next Turn")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and caster.actions >= 1
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            caster.plusUpcomingPlusAction(0, 1)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class attemptAppeasement(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Attempt Appeasement"
        self.bodyText = c.bb("+1 Action. 2B.")
        self.bodyText.heavinessText("{ HH }")
        self.bodyText.lootingText("Bottom-Text Upgrade this Card's Play Text with either: //(1) +1 Card. //(2) +1 Action.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            self.foreverLinger = True
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'B'], 'nil'))

            if card.bool1:
                ## h.splash("While Resolving: +1 Card.", printInsteadOfInput = True)
                caster.drawCard(printCard = True)
            if card.bool2:
                ## h.splash("While Resolving: +1 Action.", printInsteadOfInput = True)
                caster.plusActions(1)

    def onLooted(self, dino):
        preamble = []
        preamble.append("1: Bottom-Text Upgrade Play Text with: +1 Card.")
        preamble.append("2: Bottom-Text Upgrade Play Text with: +1 Action.")
        
        pick = h.pickValue("Pick One", [1, 2], preamble = preamble)
            
        if pick == 1:
            self.bool1 = True
            self.bodyText.appendThrowText("+1 Card.")
        else:
            self.bool2 = False
            self.bodyText.appendThrowText("+1 Action.")

class cardOverthrow(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Card Overthrow"
        self.bodyText = c.bb("+1 Action. Pick an Enemy. To it: 4Notnil; Discard their Hand.")
        self.bodyText.heavinessText("{ HH }")
        self.publishRoundStart("+1 Card.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
            if index != -1:
                enemies[index].damage(caster, dino, enemies, h.acons([4, 'Notnil'], 'nil'))
                while enemies[index].hand.length() > 0:
                    enemies[index].discardCard(enemies[index].hand, 0, dino, enemies, passedInVisuals)

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.drawCard()

class dethronement(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dethronement"
        self.bodyText = c.bb("-1 Action. 4M / 2G. //Discard the Top Card of Draw. //Discard the Bottom Card of Draw.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.minusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([4, 'M'],
                                                                 h.acons([2, 'G'],
                                                                 'nil')))
            if caster.draw.length() > 0:
                caster.discardCard(caster.draw, 0, dino, enemies, passedInVisuals, printCard = True)
            else:
                h.splash("FAIL_MOVE")
            if caster.draw.length() > 0:
                caster.discardCard(caster.draw, caster.draw.length() - 1, dino, enemies, passedInVisuals, printCard = True)
            else:
                h.splash("FAIL_MOVE")
            input(" ... ")

class failedPeaceTreaty(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Failed Peace Treaty"
        self.bodyText = c.bb("+2 Actions.")
        self.publishPacking("{ HH } To every Enemy: 2Random-notick.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.toEveryEnemy_dealDamage(h.acons([2, 'Random-notick'], 'nil')).func(card, caster, dino, enemies, passedInVisuals)

class actionOverthrow(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Action Overthrow"
        self.bodyText = c.bb("2R. Then: 2R.")
        self.publishRoundStart("+1 Action.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.plusActions(1)

class newFarmLeader(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "New Farm Order"
        self.bodyText = c.bb("+ Cantrip. Mill. Then, reverse-order Immill, and +1 Card.")
        self.publishPacking("{ HH } 1G.")
        self.bodyText.lootingText("Change a Card in Deck to: [ iTop ].")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard(printCard = True)

            millCardFunction = cf.mill()
            millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals)

            millLocation = millCardFunction.getToLocation()
            millLocation.reverse()
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

            caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], 'nil'))

    def onLooted(self, dino):
        card = h.fetchCardFromLocation("Change a Card in Deck to: [ iTop ]", dino.deck)
        card.name = "NEW-ORDER " + card.name
        card.publishInitialization(top = True)

class bayOfPigs(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bay of Pigs"
        self.bodyText = c.bb("2Random-notick / 2Random-notick / 2Random-notick.")
        self.publishPacking("{ HH } Next Turn, +1 Action.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'Random-notick'],
                                                                 h.acons([2, 'Random-notick'],
                                                                 h.acons([2, 'Random-notick'],
                                                                 'nil'))))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            card.custom1 = True

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 and self.custom1 == True):
            caster.plusActions(1)
            self.custom1 = False

class hatchingCoup(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hatching Coup"
        self.bodyText = c.bb("4R-notick / 4B-notick / 2M. //At Any Turn End, if you have 1+ Actions, you may: //(1) Move this onto Draw.")
        self.bodyText.heavinessText("{ HH }")
        self.publishRoundStart("-1 Action.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, True, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([4, 'R-notick'],
                                                                 h.acons([4, 'B-notick'],
                                                                 h.acons([2, 'M'],
                                                                 'nil'))))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.minusActions(1)

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^",
                                            "1+ Actions",
                                            "Move this onto Draw")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and caster.actions >= 1, self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            caster.moveMe(caster.play, card, caster.draw)

class organizedArmaments(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Organized Armaments"
        self.bodyText = c.bb("+2 Actions. //At Every Turn End, if you have 1+ Actions, you may: //(1) 1M.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(2)

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^",
                                            "1+ Actions",
                                            "1M")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0
                and self.reacted_1 == False
                and caster.actions >= 1, self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            cf.dealDamage().func(card, caster, dino, enemies, "null", h.acons([1, 'M'], 'nil'))

        def resetState_TurnEnd(self):
            self.reacted_1 = False

'''
    Fruit-Bearing Monks Cards
    Long lost at see, they have finally made landfall, and wish to spread their fruits upon the foreign land. 
'''

class missionary(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Missionary"
        self.bodyText = c.bb("+1 Action. 3R. //Next Next Turn, + Cantrip.")
        self.bodyText.heavinessText("{ 2H }")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(2)
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'R'], 'nil'))
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 2):
            ## h.splash("From ^" + self.name + "^: + Cantrip.")
            caster.plusActions(1)
            caster.drawCard()

'''
    BUGGED: When you do the Packing Text, there is unexpected behavior if the Card is currently Pocketed.
class gangways(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Gangways"
        self.bodyText = c.bb("+1 Action. Next Turn, and Next Next Turn: +1 Action.")
        self.bodyText.heavinessText("{ 2H }")
        self.publishPacking("Play this.")
        self.table = ["Fruit-Bearing Monks"]
    
    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
        self.monotonicLingering(2)
        caster.plusActions(1)
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        success = caster.playMe(caster.hand, self, caster, dino, enemies, passedInVisuals)
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 or self.turnsLingering == 2):
            ## h.splash("From ^" + self.name + "^: +1 Action.")
            caster.plusActions(1)

class oarsmen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Oarsmen"
        self.bodyText = c.bb("+1 Card. Next Turn, and Next Next Turn: +1 Card.")
        self.bodyText.heavinessText("{ 2H }")
        self.publishPacking("Play this.")
        self.table = ["Fruit-Bearing Monks"]
    
    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
        self.monotonicLingering(2)
        caster.drawCard(printCard = True)
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        caster.playMe(caster.hand, self, caster, dino, enemies, passedInVisuals)
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 or self.turnsLingering == 2):
            ## h.splash("From ^" + self.name + "^: +1 Card.")
            caster.drawCard(printCard = True)
'''

class rowers(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rowers"
        self.bodyText = c.bb("3Notnil. Next Turn, and Next Next Turn: +1 Card.")
        self.bodyText.heavinessText("{ 2H }")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(2)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'Notnil'], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 or self.turnsLingering == 2):
            ## h.splash("From ^" + self.name + "^: +1 Card.")
            caster.drawCard(printCard = True) 

class diligentDeckhand(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Diligent Deckhand"
        self.bodyText = c.bb("+ Cantrip. Move the Bottom Card of Draw onto the Into-Into Hand mat.")
        self.publishRoundStart("Move the Bottom Card of Draw onto the Into-Into Hand mat.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard(printCard = True)
            if caster.draw.length() > 0:
                caster.moveCard(caster.draw, caster.draw.length(), caster.intoIntoHand, inputCard = True)
            else:
                h.splash('FAIL_MOVE')
       
    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        if caster.draw.length() > 0:
            caster.moveCard(caster.draw, caster.draw.length(), caster.intoIntoHand, inputCard = True)
        else:
            h.splash('FAIL_MOVE')
       
class castaway(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Castaway"
        self.bodyText = c.bb("6R.")
        self.publishPacking("Move a Card from Hand onto Draw.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([6, 'R'], 'nil'))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.moveACardFromHandOntoDraw().func(card, caster, dino, enemies, passedInVisuals)

class rescuedPlankwalker(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rescued Plankwalker"
        self.bodyText = c.bb("+1 Action. 3B. //Next Next Turn, Discard both this and Draw.")
        self.bodyText.heavinessText("{ 2H }")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(2)
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'B'], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 2):
            ## h.splash("")
            caster.discardMe(caster.play, self, dino, enemies, vis.prefabEmpty)

            while caster.draw.length() > 0:
                caster.discardCard(caster.draw, 0, dino, enemies, vis.prefabEmpty)

class anchorperson(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Anchorman"
        self.bodyText = c.bb("3M. From Hand, Pick a Card to Save, Discarding all others.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'M'], 'nil'))

            if caster.hand.length() > 0:
                index = 1
                preamble = []
                preamble.append("These are the Cards in Hand:")
                for card in caster.hand.getArray():
                    preamble.append(str(index) + ": ^" + card.name + "^.")
                    index += 1

                pick = h.pickValue("Pick a Card from Hand to not Discard", range(1, index), preamble = preamble, passedInVisuals = passedInVisuals) - 1
                
                offset = 0
                for i in range(caster.hand.length()):
                    if i != pick:
                        caster.discardCard(caster.hand, i - offset, dino, enemies, passedInVisuals)
                        offset += 1
            else:
                h.splash('FAIL_PICK_CARD')

class headCaptain(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Navigator"
        self.bodyText = c.bb("3G. Look at the top 3 Card of Draw; you may Discard them.")
        self.publishPacking("{ 2H } Play this.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], 'nil'))
            pickUp = h.cardLocation("Pick Up")

            for i in range(3):
                if caster.draw.length() > 0:
                    caster.moveCard(caster.draw, 0, pickUp)
                else:
                    h.splash('FAIL_MOVE')

            if pickUp.length() > 0:
                preamble = []
                preamble.append("Picked Up these Cards:")
                index = 1
                for card in pickUp.getArray():
                    preamble.append(str(index) + ": ^" + card.name + "^.")
                    index += 1

                query = h.yesOrNo("Discard these Cards?", preamble = preamble, passedInVisuals = passedInVisuals)

                if query:
                    while pickUp.length() > 0:
                        caster.discardCard(pickUp, 0, dino, enemies, passedInVisuals)
                else:
                    while pickUp.length() > 0:
                        caster.moveCard(pickUp, pickUp.length() - 1, caster.draw, 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(2)
            caster.playMe(caster.hand, card, caster, dino, enemies, passedInVisuals)

'''
    Bandits of the Highway Cards
'''
class coercionCultivator(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Coercion Cultivator"
        self.bodyText = c.bb("+1 Action. 1L; if non-Fatal, Pocket a ^Shovel^ Card.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)

            damageData = cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'],
                                                                                            'nil'))
            if not damageData.fatalDamage:
                h.splash("Dealt non-Fatal Damage: Pocket a ^Shovel^ Card.")
                caster.gainCard(shovel(), caster.pocket)

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

class badFortune(DinoShellCard):
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

class goodFortune(DinoShellCard):
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

class bolster(DinoShellCard):
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

class carCasing(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Car Casing"
        self.bodyText = c.bb("0.67 Chance for: 2R-notick / 2G-notick / 2B-notick / 2M. //Otherwise: Pocket this.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            if cf.chance(0.67, onSuccess_printInsteadOfInput = True).func(card, caster, dino, enemies, passedInVisuals):
                cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'],
                                                                     h.acons([2, 'G-notick'],
                                                                     h.acons([2, 'B-notick'],
                                                                     h.acons([2, 'M'],
                                                                     'nil')))))
            else:
                caster.moveMe(caster.play, card, caster.pocket)


class highwayGrassMedian(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Highway-Grass Median"
        self.bodyText = c.bb("2G-notick / 2B-notick. //You may Discard your Hand for: + Cantrip. //0.25 Chance for: + Cantrip.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'G-notick'],
                                                                 h.acons([2, 'B-notick'],
                                                                 'nil')))

            query = h.yesOrNo("Discard your Hand for: + Cantrip?", preamble = [], passedInVisuals = passedInVisuals)
            if query:
                while caster.hand.length() > 0:
                    caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
                caster.plusActions(1)
                caster.drawCard()

            if cf.chance(0.25).func(card, caster, dino, enemies, passedInVisuals):
                caster.plusActions(1)
                caster.drawCard()

class hunkOfJunk(DinoCard):
    def __init__(self):
        super().__init__()
        self.bodyText = c.bb("+1 Action. 1G / 1G-notick / 1R / 1R-notick. //You may: (+1 Card. 0.5 Chance for: Pocket a ^Rubbish^.).")
        self.name = "Hunk of Junk"
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G'],
                                                                 h.acons([1, 'G-notick'],
                                                                 h.acons([1, 'R'],
                                                                 h.acons([1, 'R-notick'],
                                                                 'nil')))))
            query = h.yesOrNo("+1 Card and 0.5 Chance for: Pocket a Rubbish Card?", passedInVisuals = passedInVisuals)
            if query:
                caster.drawCard()
                if cf.chance(0.5).func(card, caster, dino, enemies, passedInVisuals):
                    caster.gainCard(rubbish(), dino.pocket)

class brakeCutters(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Brake Cutters"
        self.bodyText = c.bb("+1 Action. 1M / 1M / 1M. Gain a ^Rubbish^.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], h.acons([1, 'M'], h.acons([1, 'M'], 'nil'))))
            caster.gainCard(rubbish(), dino.discard)

class wheelShrapnel(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Wheel Shrapnel"
        self.bodyText = c.bb("+1 Action. 2R-notick / 2M. Discard your Hand.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'], h.acons([2, 'M'], 'nil')))
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)

class shamSpeedSign(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Sham Speed Sign"
        self.bodyText = c.bb("2B. +3 Cards.")
        self.publishPacking("Pocket this.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'B'], 'nil'))
            for i in range(3):
                caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.packingText_PocketThis().func(card, caster, dino, enemies, passedInVisuals)

class bandItBond(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Band-it Bond"
        self.bodyText = c.bb("Break a Band. Discard your Hand.")
        ## self.bodyText = c.bb("2R-notick / 2G-notick / 2B-notick. Discard your Hand.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.breakABand().func(card, caster, dino, enemies, passedInVisuals)

            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)

class infiltratorInterrogators(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Infiltrator Interrogators"
        self.bodyText = c.bb("+2 Actions. 2x, Draw a Card to the Pocket Mat. //Discard your Hand.")
        self.bodyText.heavinessText("{ HH }")
        self.publishRoundStart("Pocket a ^Rubbish^ Card.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(2)
            for i in range(cf.getter_numberX(2).func(card, caster, dino, enemies, passedInVisuals)):
                caster.drawCard(toLocation = caster.pocket)

            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.gainCard(rubbish(), caster.pocket)

class raccoonHeist(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Raccoon Heist"
        self.bodyText = c.bb("+2 Actions. Pocket a ^Shovel^ Card.")
        self.publishPacking("1B / 1B.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)
            caster.gainCard(shovel(), dino.pocket)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'B'],
                                                                               h.acons([1, 'B'],
                                                                               'nil')))

class roadSignAugers(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Road Sign Augers"
        self.bodyText = c.bb("+1 Action. Discard your Hand, then +3 Cards.")
        self.publishRoundStart("Pocket a ^Shovel^ Card.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            for i in range(3):
                caster.drawCard()

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.gainCard(shovel(), caster.pocket)

class carFeigning(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Car Feigning"
        self.bodyText = c.bb("1G / 1R. If your Hand is Empty: + Cantrip; + Cantrip.")
        self.publishPacking("Pocket this.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], h.acons([1, 'R'], 'nil')))
            if dino.hand.length() == 0:
                h.splash("Hand is Empty, so: + Cantrip, + Cantrip.")
                for i in range(2):
                    caster.plusActions(1)
                    caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.packingText_PocketThis().func(card, caster, dino, enemies, passedInVisuals)

'''
    New Bear Order Cards
'''
class bearBeret(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Beret"
        self.bodyText = c.bb("# <-- a Non-Negative Number. #x, 0.67 Chance for a Success. //On all Successes: +# Actions. //Otherwise, +2 Actions.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            number = h.pickNonNegativeNumber("Pick a Non-Negative Number", passedInVisuals = passedInVisuals)
            text = ""
            onlySuccesses = True
            for i in range(number):
                if i != 0:
                    text += ", "

                if cf.chance(0.67, onSuccess_noOutput = True, onFailure_noOutput = True).func(card, caster, dino, enemies, passedInVisuals):
                    text += "Success"
                else:
                    text += "Failure"
                    onlySuccesses = False

            if text == "":
                text += "..."

            h.splash(text, printInsteadOfInput = True)
            if onlySuccesses:
                h.splash("Only Successes; +" + str(number) + " Action(s).")
                ## card.foreverLinger = True
                caster.plusActions(number)
            else:
                h.splash("Had a Failure; +2 Actions.")
                caster.plusActions(2)

            # caster.drawCard()

class playDead(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Play Dead"
        self.bodyText = c.bb("+4 Actions. Discard your Hand. +1 Card.")
        self.publishPacking("+4 Actions. 1B-notick.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(4)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(4)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'B-notick'],
                                                                 'nil'))

class reveredBearSkull(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Revered Bear Skull"
        self.bodyText = c.bb("(1R-notick x8).")
        self.publishPacking("{ HH } Per Remaining Action, to that many Subsequent Turns: //    (1) Plus 1 Action.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(self, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                h.acons([1, 'R-notick'],
                                                                'nil')))))))))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            for i in range(caster.actions):
                caster.plusUpcomingPlusAction(i, 1)

class torchBearing(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Torch Bearing"
        self.bodyText = c.bb("+2 Actions.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

'''
class recyclingBin(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Recycling Bin"
        self.bodyText = c.bb("1B / 1B / 1B / 1G / 1G. //+1 Card. Discard the Bottom Card of Draw.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'B'],
                                                                 h.acons([1, 'B'],
                                                                 h.acons([1, 'B'],
                                                                 h.acons([1, 'G'],
                                                                 h.acons([1, 'G'],
                                                                 'nil'))))))

            caster.drawCard()
            cf.discardBottomCardOfDraw().func(card, caster, dino, enemies, passedInVisuals)
'''

'''
class boneGnaw(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bone-Gnaw"
        self.bodyText = c.bb("+1 Card. (1M x4).")
        self.publishRoundStart("Arbitrarily Discard 4 Cards of Draw.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard(printCard = True)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'M'],
                                                                 h.acons([1, 'M'],
                                                                 h.acons([1, 'M'],
                                                                 h.acons([1, 'M'],
                                                                 'nil')))))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        for i in range(4):
            cf.arbitrarilyDiscardCardFromDraw().func(self, caster, dino, enemies, passedInVisuals)
'''

class reclaimedApexPredation(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Reclaimed Apex Predation"
        self.bodyText = c.bb("> [ iTop ], < iTop > Shell this. //> ...")
        self.table = ["New Bear Order"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "APEX " + cardToEnshell.name
        cardToEnshell.publishInitialization(top = True)
        cardToEnshell.publishReshuffle(top = True)
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Shell this.", cf.shellThis()))

class shoulderHump(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shoulder Hump"
        self.bodyText = c.bb("5Notnil / 4Notnil.")
        self.publishPacking("{ 1H } Next Turn, +1 Action.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([5, 'Notnil'],
                                                                 h.acons([4, 'Notnil'],
                                                                 'nil')))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

            success = caster.moveMe(caster.hand, card, caster.play, supressFailText = True)
            if not success:
                success = caster.moveMe(caster.pocket, card, caster.play)

            card.custom1 = True

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 and self.custom1 == True):
            caster.plusActions(1)
            self.custom1 = False

class honeyPot(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Honey Pot"
        self.bodyText = c.bb("Discard your Hand. //Next Turn, +2 Actions.")
        self.bodyText.heavinessText("{ 1H }")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            caster.plusActions(2)

class hibernation(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hibernation"
        self.bodyText = c.bb("To each Enemy that has yet to take a Turn: //(1) Discard their Hand. //Discard your Hand.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for enemy in enemies:
                if enemy.turn == 0:
                    h.splash("To '" + enemy.name + "': Discarding their Hand.", printInsteadOfInput = True)
                    while enemy.hand.length() > 0:
                        enemy.discardCard(enemy.hand, 0, dino, enemies, passedInVisuals)

            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)

'''
class bearClaws(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Claws"
        self.bodyText = c.bb("3R. Then: 2B.")
        self.bodyText.heavinessText("{ HH }")
        self.publishPacking("Discard your Draw.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'R'],
                                                                 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'B'],
                                                                 'nil'))

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.discardYourDraw().func(self, caster, dino, enemies, passedInVisuals)
'''

class backScratcher(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Back Scratcher"
        self.bodyText = c.bb("+1 Action. (1L x6). +1 Card.")
        self.publishInitialization(discard = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'],
                                                                 h.acons([1, 'L'],
                                                                 h.acons([1, 'L'],
                                                                 h.acons([1, 'L'],
                                                                 h.acons([1, 'L'],
                                                                 h.acons([1, 'L'],
                                                                 'nil')))))))
            caster.drawCard()

class beesNest(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bees Nest"
        self.bodyText = c.bb("3x, to an Arbitrary Enemy: 1L. //Next Turn, +1 Action.")
        self.bodyText.heavinessText("{ 1H }")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            cf.numberX_toArbitraryEnemy_dealDamage(3, h.acons([1, 'L'], 'nil')).func(card, caster, dino, enemies, passedInVisuals)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            caster.plusActions(1)

class leaveNoTraceMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Leave No Trace Mantra"
        self.bodyText = c.bb("+2 Actions. Move an Arbitrary non-^Muck^ Card from Discard into Hand.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

            caster.discard.shuffle()
            index = 0
            match = False
            while match == False and index < caster.discard.length():
                if "Muck" not in caster.discard.getArray()[index].table:
                    match = True
                    caster.moveCard(caster.discard, index, caster.hand, position = caster.hand.length())
                index += 1
            if match == False:
                h.splash("FAIL_MOVE")

class chaseUntilExhaustion(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Chase Until Exhaustion"
        self.bodyText = c.bb("+1 Action. 1Notnil. //Discard your Draw. 0.67 Chance for: { HH }.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Notnil'],
                                                                 'nil'))
            cf.discardYourDraw().func(card, caster, dino, enemies, passedInVisuals)

            if cf.chance(0.67).func(card, caster, dino, enemies, passedInVisuals):
                card.foreverLinger = True

'''
    Graverobber Cards
'''

class heirloom(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Heirloom"
        self.bodyText = c.bb("2M.")
        # self.bodyText.lootingText("When Replaced with Loot: Change Replacement Card with [ iTop ].")
        # self.publishInitialization(top = True)
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'M'],
                                                                 'nil'))

    # def onReplacedWithLoot(self, dino, newCard):
    #     h.splash("Triggered On Replaced with Loot: Changing Replacement Card with [ iTop ].")
    #     newCard.publishInitialization(top = True)

class emptyMantle(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Empty Mantle"
        self.bodyText = c.bb("Do Nothing.")
        # self.bodyText.lootingText("When Replaced with Loot: Change Replacement Card with [ iDiscard ].")
        self.publishInitialization(discard = True)
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            pass

    # def onReplacedWithLoot(self, dino, newCard):
    #     h.splash("Triggered On Replaced with Loot: Changing Replacement Card with [ iDiscard ].")
    #     newCard.publishInitialization(discard = True)

class luggedCreature(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Lugged Creature"
        self.bodyText = c.bb("+1 Action. 1B-notick.")
        self.publishRoundStart("Pocket a ^Holy Shovel^ Card.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'B-notick'],
                                                                 'nil'))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.gainCard(holyShovel(), caster.pocket)

class faithfulHound(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Faithful Hound"
        self.bodyText = c.bb("1Notnil / 1Notnil.")
        self.publishRoundStart("Pocket a ^Friendly Bark^ Card.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Notnil'],
                                                                 h.acons([1, 'Notnil'],
                                                                 'nil')))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.gainCard(friendlyBark(), caster.pocket)

class spareSpade(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Spare Spade"
        self.bodyText = c.bb("+1 Action. Discard your Hand, for +2 Cards.")
        self.publishInitialization(pocket = True)
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            for i in range(2):
                caster.drawCard()

class stowaway(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Stowaway"
        self.bodyText = c.bb("+1 Action. 3G.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'G'],
                                                                 'nil'))

class willOWisps(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Will-o-Wisps"
        self.bodyText = c.bb("2x, to an Arbitrary Enemy: 1L.")
        # self.bodyText.lootingText("When Replaced with Loot: Change Replacement Card with [ iTop ].")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.numberX_toArbitraryEnemy_dealDamage(2, h.acons([1, 'L'], 'nil')).func(card, caster, dino, enemies, passedInVisuals)

    # def onReplacedWithLoot(self, dino, newCard):
    #     h.splash("Triggered On Replaced with Loot: Changing Replacement Card with [ iTop ].")
    #     newCard.publishInitialization(top = True)

class flickeringLantern(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Flickering Lantern"
        self.bodyText = c.bb("+1 Action. 1R-notick.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                 'nil'))

    '''
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.discardBottomCardOfDraw().func(self, caster, dino, enemies, passedInVisuals)

        success = caster.moveMe(caster.hand, self, caster.draw, position = caster.draw.length(), supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, self, caster.draw, position = caster.draw.length())
    '''

class courageBuilding(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Courage Building"
        self.bodyText = c.bb("1B-notick / 1R.")
        self.publishPacking("Pocket a ^Trip^ Card.")
        ## Could change to use the Into-Hand or even Into-Pocket mat.
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            ## caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'B-notick'],
                                                                 h.acons([1, 'R'],
                                                                 'nil')))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.gainCard(trip(), caster.pocket)

class trip(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trip"
        self.bodyText = c.bb("||Temporary|| + Cantrip.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

class friendlyBark(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Friendly Bark"
        self.bodyText = c.bb("||Temporary|| +1 Card. Destroy this.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(1):
                caster.drawCard()
            cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals)

class holyShovel(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Holy Shovel"
        self.bodyText = c.bb("||Temporary|| +1 Action. Discard your Hand, for +2 Cards.")
        self.publishPacking("Entoken all Pocket Cards with <<feathery>>.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            for i in range(2):
                caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for card in caster.pocket.getArray():
                card.publishToken(tk.feathery())

'''
    Packing Bot Cards
'''
class metalCrate(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Metal Crate"
        self.bodyText = c.bb("1M / 1M.")
        ## self.bodyText.heavinessText("{ HH }")
        ## self.bodyText.lootingText("When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            ## card.foreverLinger = True
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], h.acons([1, 'M'], 'nil')))

    '''
    def onReplacedWithLoot(self, dino, newCard):
        h.splash("Triggered On Replaced with Loot: +1 Looting.")
        dino.looting += 1
    '''

class packingPeanuts(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Packing Peanuts"
        self.bodyText = c.bb("1L. Then: 1L.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'], 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'], 'nil'))

'''
class shippingTape(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shipping Tape"
        self.bodyText = c.bb("2R.")
        ## self.bodyText.lootingText("WTID, when you Loot a Card, you may change its Initialization Location to: (1) Top; (2) Bottom; (3) Discard.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))
'''

class forkliftCertificate(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Forklift Certificate"
        self.bodyText = c.bb("+2 Actions. At Turn End, if you have 2+ ^Junk^ in Play: //(1) Move this onto the Into-Hand Mat.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(2)
            ## caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "2+ ^Junk^ in Play",
                                            "Move this onto the Into-Hand Mat")
            ##  --> Static because: the trigger is always 100% what it says it will be. 

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            detritusCount = 0
            ## Sees if Card is in desired Location
            if h.locateCardIndex(caster.play, card) >= 0:
                ## Sees if Card there exists a Detritus in Play
                for cardInPlay in caster.play.getArray():
                    if (cardInPlay.unmodifiedName == "Junk"):
                        detritusCount += 1
            return (detritusCount >= 2, self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            index = h.locateCardIndex(caster.play, card)
            if index >= 0:
                caster.moveCard(caster.play, index, caster.intoHand)
                h.splash(self.END_OF_DINO_TURN_RT.getText(), printInsteadOfInput = True)
            else:
                h.splash('FAIL_MOVE')

class newFreshAir(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "New Fresh Air"
        self.bodyText = c.bb("+1 Action. 1G-notick.")
        self.publishPacking("1G-notick.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

class stampGun(DinoCard):
    def __init__(self): 
        super().__init__()
        self.name = "Stamp Gun"
        self.bodyText = c.bb("1R-notick / 1B-notick.")
        self.publishPacking("Draw a Card to the Into-Hand mat.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                 h.acons([1, 'B-notick'],
                                                                 'nil')))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class warehouseHelmet(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Warehouse Helmet"
        self.bodyText = c.bb("+3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            for i in range(3):
                caster.drawCard()

class filledFile(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Filled File"
        self.bodyText = c.bb("1Notnil.")
        ## self.bodyText.push("looting", "When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Notnil'], 'nil'))

class potpourri(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Potpourri"
        self.bodyText = c.bb("1Random.")
        ## self.bodyText.push("looting", "When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Random'], 'nil'))

'''
    Fallow Farmland
'''
class finalStraw(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Final Straw"
        ## self.bodyText = c.bb("~ When Looted, Enshell a Card as follows: //> { HH } Shell this. //> ... //> + Cantrip.")
        self.bodyText = c.bb("> { HH } Shell this. //> ... //> + Cantrip.")
        self.table = ["Fallow Farmland"]

    ## This is a good example of how to do this, but we have a Cantrip C.F. function now.
    class customBelowTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard()
            caster.plusActions(1)

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "CONCLUDING " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("{ HH } Shell this.", cf.foreverLingerShellThis()),
                                   belowThrowTextWrapper = cf.shellTextWrapper("+ Cantrip.", self.customBelowTextFunction()))

class rustedScythe(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rusted Scythe"
        self.bodyText = c.bb("2R-notick / 2M. You may: Discard your Hand for +2 Cards. //Then, +1 Card.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'], h.acons([2, 'M'], 'nil')))
            query = h.yesOrNo("Discard your Hand for +2 Cards?", passedInVisuals = passedInVisuals)
            if query:
                while caster.hand.length() > 0:
                    caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
                for i in range(2):
                    dino.drawCard()
            dino.drawCard()

class cultivator(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cultivator"
        self.bodyText = c.bb("1M / 1M. Move this onto Draw.")
        self.publishPacking("Draw a Card to the Into-Hand mat.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'M'],
                                                                               h.acons([1, 'M'],
                                                                               'nil')))
            caster.moveMe(caster.play, card, caster.draw, position = 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class brassMuzzle(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Brass Muzzle"
        self.bodyText = c.bb("+1 Action. Pick an Enemy. To it: 2B / 2M; Discard a Card.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
            if index != -1:
                enemies[index].damage(caster, dino, enemies, h.acons([2, 'B'], h.acons([2, 'M'], 'nil')))
                if enemies[index].hand.length() > 0:
                    enemies[index].discardCard(enemies[index].hand, 0, dino, enemies, passedInVisuals)

class deadHarvestedGrass(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dead Harvested Grass"
        self.bodyText = c.bb("+1 Action. 3G. Then: 3L. //Draw until you have 1 Card in Hand.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([3, 'L'], 'nil'))
            priorLength = -1
            while caster.hand.lengthExcludingFeathery() < 1 and caster.hand.length() != priorLength:
                priorLength = caster.hand.length()
                caster.drawCard()

class gnawedCableCord(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Gnawed Cable Cord"
        self.bodyText = c.bb("+2 Actions. 2B-notick. Move this onto Draw.")
        self.publishPacking("Draw a Card to the Into-Hand mat.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'B-notick'], 'nil'))
            caster.moveMe(caster.play, card, caster.draw, position = 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class rust(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Rust"
        ## self.bodyText = c.bb("~ When Looted, Enshell a Card as follows: //> Shell this. //> ... //> Draw until you have 3 Cards in Hand.")
        self.bodyText = c.bb("> Shell this. //> ... //> Draw until you have 3 Cards in Hand.")
        self.table = ["Fallow Farmland"]

    class customBelowTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            priorLength = -1
            while caster.hand.lengthExcludingFeathery() < 3 and caster.hand.length() != priorLength:
                priorLength = caster.hand.length()
                caster.drawCard()

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "RUSTED " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("{ HH } Shell this.", cf.foreverLingerShellThis()),
                                   belowThrowTextWrapper = cf.shellTextWrapper("Draw until you have 3 Cards in Hand.", self.customBelowTextFunction()))

class grasshopperCache(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Grasshopper Cache"
        self.bodyText = c.bb("Draw until you have 3 Cards in Hand.")
        self.publishPacking("2G-notick / 2M.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            priorLength = -1
            while caster.hand.lengthExcludingFeathery() < 3 and caster.hand.length() != priorLength:
                priorLength = caster.hand.length()
                caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'G-notick'], h.acons([2, 'M'], 'nil')))

class trampledRodent(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trampled Rodent"
        self.bodyText = c.bb("+1 Action. 1R-notick / 1G-notick / 1B-notick / 1M. //Then, Discard an Arbitrary Card in Hand.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                 h.acons([1, 'G-notick'],
                                                                 h.acons([1, 'B-notick'],
                                                                 h.acons([1, 'M'],
                                                                 'nil')))))
            cf.arbitrarilyDiscardCardFrom_Location(caster.hand, inputCard = True).func(card, caster, dino, enemies, passedInVisuals)

class twigRockScarecrow(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Twig-Rock Scarecrow"
        self.bodyText = c.bb("Plus 1 Action and Draw 1 More Card for your Next Turn. //Move this onto Draw.")
        self.publishPacking("1Random / 1Random.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusUpcomingPlusAction(0, 1)
            caster.plusUpcomingPlusCard(0, 1)
            caster.moveMe(caster.play, card, caster.draw, position = 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Random'],
                                                                               h.acons([1, 'Random'],
                                                                               'nil')))

class mangledShrew(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Mangled Shrew"
        self.bodyText = c.bb("2R-notick / 1Notnil / 1Notnil / 1Notnil.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'],
                                                                 h.acons([1, 'Notnil'],
                                                                 h.acons([1, 'Notnil'],
                                                                 h.acons([1, 'Notnil'],
                                                                 'nil')))))

class lastSeeds(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Last Seeds"
        self.bodyText = c.bb("+1 Action. 9L. +1 Card.")
        self.bodyText.lootingText("Gain a Copy of this.")
        self.publishInitialization(muck = True)
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([9, 'L'], 'nil'))
            caster.drawCard()

    def onLooted(self, dino):
        dino.gainCopyOfCard(self, dino.deck)

'''
    Horse Hostelry
'''
class brokenBottle(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Broken Bottle"
        self.bodyText = c.bb("||Temporary|| +1 Action. 0.5 Chance for: +1 Card.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            if cf.chance(0.5).func(card, caster, dino, enemies, passedInVisuals):
                caster.drawCard(inputCard = True)

class bottleCaps(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bottle Caps"
        self.bodyText = c.bb("(1Notnil x3); //If Fatal or Broke a Band, Replace this with ^Broken Bottle^. //Otherwise, Discard this.")
        ## self.publishToken(tk.alliance())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            damageData = cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Notnil'],
                                                                                            h.acons([1, 'Notnil'],
                                                                                            h.acons([1, 'Notnil'],
                                                                                            'nil'))))
            if damageData.fatalDamage:
                h.splash("Dealt Fatal Damage: Replacing this with ^Broken Bottle^.")
                card.mutateThis(brokenBottle())
            elif damageData.brokeABand:
                h.splash("Broke a Band: Replacing this with ^Broken Bottle^.")
                card.mutateThis(brokenBottle())
            else:
                caster.discardMe(caster.play, card, dino, enemies, passedInVisuals)

class cowboyDuelMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cowboy Duel Mantra"
        self.bodyText = c.bb("Pick an Enemy. 3x, to it: //(1) If it has any Cards in Hand, Discard a Card; Otherwise 1Notnil. //Replace this with ^Broken Bottle^.")
        ## self.publishPacking("Draw a Card to the Into-Hand mat.")
        ## self.publishPacking("Gain 3 ^Broken Bottle^ Cards onto the Into-Hand mat.")
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
            if index != -1:
                enemy = enemies[index]
                for i in range(3):
                    if enemy.hand.length() > 0:
                        enemy.discardCard(enemy.hand, random.randint(0, enemy.hand.length() - 1), dino, enemies, passedInVisuals)
                    else:
                        enemy.damage(caster, dino, enemies, h.acons([1, 'Notnil'], 'nil'))
            card.mutateThis(brokenBottle())

    ## def onPacking(self, caster, dino, enemies, passedInVisuals):
    ##     super().onPacking(caster, dino, enemies, passedInVisuals)
    ##     caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

    ## def onPacking(self, caster, dino, enemies, passedInVisuals):
    ##     super().onPacking(caster, dino, enemies, passedInVisuals)
    ##     for i in range(3):
    ##         caster.gainCard(brokenBottle(), caster.intoHand)

class trotTrot(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trot Trot"
        self.bodyText = c.bb("+1 Action. 1R-notick / 1R. +1 Card. //Replace this with ^Broken Bottle^.")
        self.publishToken(tk.feathery())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                               h.acons([1, 'R'],
                                                                               'nil')))
            caster.drawCard()
            card.mutateThis(brokenBottle())

class goodBadAndUgly(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Good Bad and Ugly"
        self.bodyText = c.bb("1M / 1L / 1Random. +1 Card. //Replace this with ^Broken Bottle^.")
        self.publishToken(tk.alliance())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'M'],
                                                                               h.acons([1, 'L'],
                                                                               h.acons([1, 'Random'],
                                                                               'nil'))))
            caster.drawCard()
            card.mutateThis(brokenBottle())

class expiredMilk(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Expired Milk"
        self.bodyText = c.bb("+1 Action. Pick an Enemy. To it: //(1) 1G-notick / 1M. //(2) Replace an Arbitrary Card in Hand with ^Broken Bottle^.")
        self.publishToken(tk.alliance())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
            if index != -1:
                enemy = enemies[index]
                h.splash("To '" + enemy.name + "': 1G-notick / 1M; Replace an Arbitrary Card in Hand with ^Broken Bottle^.", printInsteadOfInput = True)
                enemy.damage(caster, dino, enemies, h.acons([1, 'G-notick'],
                                                    h.acons([1, 'M'],
                                                    'nil')))

                if enemy.hand.length() > 0:
                    position = random.randint(0, enemy.hand.length() - 1)
                    enemy.hand.at(position).mutateThis(brokenBottle())
                else:
                    h.splash('FAIL_PICK_CARD')

class cowboysInExile(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cowboys In Exile"
        self.bodyText = c.bb("+2 Actions.")
        self.publishPacking("Entoken all Cards in Play with <<feathery>>.")
        self.publishToken(tk.alliance())
        self.publishInitialization(muck = True)
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for card in caster.play.getArray():
                card.publishToken(tk.feathery())

class getawayHorse(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Getaway Horse"
        ## "Trainyard Rendezvous"
        self.bodyText = c.bb("Discard all ^Junk^ in Hand. +4 Cards.")
        self.publishToken(tk.alliance())
        self.publishInitialization(muck = True)
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.discardAll_names_fromLocation(caster.hand, ["Junk"]).func(card, caster, dino, enemies, passedInVisuals)

            for i in range(4):
                caster.drawCard()

class icelandicHorse(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Icelandic Horse"
        self.bodyText = c.bb("+ Cantrip. Mill, Unless a Card with '+1 Card', '+X Cards' or '+ Cantrip' in body-text is found; Move such a Card into Hand. Then, Immill.")
        ## self.publishPacking("1B / 1M.")
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

        ## self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def custom_checkClause(self, card):
            text = card.bodyText.unpacking + " " + card.bodyText.core + " " + card.bodyText.packing
            cardsMatchObject = re.search("(\\d)+ Card[(s)(\\W)]", text)
            cantripMatchObject = re.search("\\+ Cantrip", text)
            return (cardsMatchObject != None) or (cantripMatchObject != None)

        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

            millCardFunction = cf.mill(usingCheckClause = True, checkClause = self.custom_checkClause)

            matchingCard = millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals, inputMatchCard = True)
            if matchingCard != 'NO MATCHES':
                caster.moveMe(millCardFunction.toLocation, matchingCard, caster.hand, position = caster.hand.length())
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

class sheriffsBadge(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Sheriff's Badge"
        self.bodyText = c.bb("> Entoken this with: <<feathery>>, <<alliance>>.")
        self.table = ["Horse Hostelry"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "HONORED " + cardToEnshell.name
        cardToEnshell.publishToken(tk.feathery())
        cardToEnshell.publishToken(tk.alliance())

class timeInABottle(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Time in a Bottle"
        self.bodyText = c.bb("+ Cantrip.")
        ## self.publishPacking("Take a 2nd Turn. To every Enemy: Take a 2nd Turn. //    Replace this with ^Broken Bottle^.")
        self.publishPacking("{ HH } Take a 2nd Turn. To every Enemy: Take a 2nd Turn. //    Gain a ^Broken Bottle^.")
        self.publishInitialization(muck = True)
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            caster.plusExtraTurn()
            for enemy in enemies:
                enemy.plusExtraTurn()
            ## card.mutateThis(brokenBottle())
            caster.gainCard(brokenBottle(), caster.discard)

class smashedBottles(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Smashed Bottles"
        self.bodyText = c.bb("")
        self.table = ["Horse Hostelry"]
        ## self.bundle(throwCardFunction = self.duringPlay())

class fightOrFlight(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fight or Flight"
        self.bodyText = c.bb("1G-notick / 1B-notick / 1G / 1B.")
        self.publishPacking("Entoken the top Card of Draw with <<feathery>>.")
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'],
                                                                               h.acons([1, 'B-notick'],
                                                                               h.acons([1, 'G'],
                                                                               h.acons([1, 'B'],
                                                                               'nil')))))

'''
    Leeches
'''

# class actionLeech(DinoCard):
    

'''
    SHOP CARDS
'''

## Nothing Cards are a special type of Cards; they function the same
class purge(DinoShellCard):
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

class persevere(DinoShellCard):
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

class proliferate(DinoShellCard):
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

class ransack(DinoShellCard):
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

class renovate(DinoShellCard):
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

class twig(DinoCard):
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

class leavesRake(DinoCard):
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

class snowShovel(DinoCard):
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

class firewoodAxe(DinoCard):
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

class rock(DinoCard):
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

class stick(DinoCard):
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

class muscles(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Muscles"
        self.bodyText = c.bb("+1 Action. 1Random. +1 Card.")
        self.table = ["Shop"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Random'], 'nil'))
            caster.drawCard()

class magicalFeather(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Feather"
        self.bodyText = c.bb("> Entoken this with: <<feathery>>.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "FEATHERED " + cardToEnshell.name
        cardToEnshell.publishToken(tk.feathery())

class magicalPocketWatch(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Pocket Watch"
        self.bodyText = c.bb("> Change the Packing Text of this to: //> |>| Pocket this.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "POCKET-WATCHED " + cardToEnshell.name
        cardToEnshell.purgePackingText(cf.shellTextWrapper("Pocket this.", cf.packingText_PocketThis()))

class magicalCounterWeight(DinoShellCard):
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

class magicalReassortment(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Reassortment"
        self.bodyText = c.bb("> Change this to: < iTop >.")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "REASSORTED " + cardToEnshell.name
        cardToEnshell.publishReshuffle(top = True)

class magicalAssortment(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Magical Assortment"
        self.bodyText = c.bb("> Change this to: [ iTop ].")
        self.table = ["Shop"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "ASSORTED " + cardToEnshell.name
        cardToEnshell.publishInitialization(top = True)

class liquidation(DinoShellCard):
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
    Apple Orchard
'''
class orchardTree(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Orchard Tree"
        self.bodyText = c.bb("6G-notick / 1Random-notick. Move this into Hand.")
        self.publishPacking("2x, 'Plow' Draw.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([6, 'G-notick'],
                                                                               h.acons([1, 'Random-notick'],
                                                                               'nil')))
            success = caster.moveMe(caster.play, card, caster.hand, position = caster.hand.length(), supressFailText = True)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.plow(6, caster.draw).func(card, caster, dino, enemies, passedInVisuals)

class barnWood(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Barn Wood"
        self.bodyText = c.bb("+2 Cards. Entoken this with <<prepared>>.")
        self.publishPacking("Play this.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(2):
                caster.drawCard()
            card.publishToken(tk.prepare())

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            success = caster.playMe(caster.hand, card, caster, dino, enemies, passedInVisuals, supressFailText = False)
            if not success:
                caster.playMe(caster.pocket, card, caster, dino, enemies, passedInVisuals)

class grainCart(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Grain Cart"
        self.bodyText = c.bb("1R-notick / 1G-notick / 1B-notick.")
        self.publishPacking("Entoken this with <<prepared>>.")
        self.publishRoundStart("Entoken this with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                               h.acons([1, 'G-notick'],
                                                                               h.acons([1, 'B-notick'],
                                                                               'nil'))))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.publishToken(tk.prepare())

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        self.publishToken(tk.prepare())

'''
class disperseAppleSeeds(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Disperse Apple Seeds"
        self.bodyText = c.bb("3x, 'Plow' Hand.")
        self.publishPacking("3x, 'Plow' Draw.")
        self.bodyText.lootingText("Gain a ^Twig!^.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.plow(3, caster.hand).func(card, caster, dino, enemies, passedInVisuals)

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.plow(3, caster.draw).func(self, caster, dino, enemies, passedInVisuals)

    def onLooted(self, dino):
        dino.gainCard(twigExclamation(), dino.deck)
'''

class treeTrellis(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Tree Trellis"
        self.bodyText = c.bb("> Shell this, and Entoken it with <<prepared>>. //> ...")
        self.table = ["Apple Orchard Hollow"]

    class customTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.shellThis().func(card, caster, dino, enemies, passedInVisuals)
            card.publishToken(tk.prepare())

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "TRELLIS OF " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Shell this, and Entoken it with <<prepared>>.", self.customTextFunction()))


class ripeMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Ripe Mantra"
        self.bodyText = c.bb("+1 Action. 1R. +1 Card. //Mill, Unless a ^Junk^ is found; Discard such a Card. Then, Immill. //9x, 'Plow' Discard.")
        self.publishInitialization(top = True)
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def custom_checkClause(self, card):
            return (card.unmodifiedName == "Junk")

        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R'],
                                                                               'nil'))
            caster.drawCard()

            millCardFunction = cf.mill(usingCheckClause = True, checkClause = self.custom_checkClause)

            matchingCard = millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals, inputMatchCard = True)
            if matchingCard != 'NO MATCHES':
                caster.discardMe(millCardFunction.toLocation, matchingCard, dino, enemies, passedInVisuals)
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

            cf.plow(9, caster.discard).func(card, caster, dino, enemies, passedInVisuals)

class bobbingForApples(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bobbing For Apples"
        self.bodyText = c.bb("-1 Action. 2x, to an Arbitrary Card in Draw: //(1) Entoken it with <<prepared>>. //(2) Move it into Hand.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.minusActions(1)
            for i in range(2):
                card, success = cf.getter_toArbitraryCardInLocation(caster.draw).func(card, caster, dino, enemies, passedInVisuals)
                if success:
                    card.publishToken(tk.prepare())
                    caster.moveMe(caster.draw, card, caster.hand, position = caster.hand.length())

class prepareToHarvestApples(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Prepare To Harvest Apples"
        ## self.bodyText = c.bb("1R-notick / 1G-notick. //Next Turn, to Cards you Play, After Resolution: //(1) If in Play, Entoken it with <<prepared>>.")
        self.bodyText = c.bb("Next Turn, to Cards you Play, After Resolution: //(1) If in Play, Entoken it with <<prepared>>.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            ## cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
            ##                                                                    h.acons([1, 'G-notick'],
            ##                                                                    'nil')))

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.cardThatWasResolved = None

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if (not r.moments_isLeftInRight([r.AfterCardPlayResolution], moments)
                or card.turnsLingering != 1):
                return (False, r.EMPTY_RT)

            ## Fetches the Card
            moment_afterCardPlayResolution = r.moments_fetchInRight([r.AfterCardPlayResolution], moments)
            if moment_afterCardPlayResolution == None:
                return (False, r.EMPTY_RT)

            self.cardThatWasResolved = moment_afterCardPlayResolution.cardThatWasResolved

            ## Is the Card still in Play?
            if h.locateCardIndex(caster.play, self.cardThatWasResolved) == -1:
                return (False, r.EMPTY_RT)

            ## Success, unless reacted
            CARD_AFTER_PLAY_RESOLUTION = r.rt(False,
                                              "^" + card.name + "^",
                                              "^" + self.cardThatWasResolved.name + "^ is in Play after Resolve",
                                              "Entoken it with <<prepared>>")
            return (not self.reacted_1, CARD_AFTER_PLAY_RESOLUTION)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            self.cardThatWasResolved.publishToken(tk.prepare())
            self.cardThatWasResolved = None

        def resetState_AfterAnyCardResolves(self):
            self.reacted_1 = False

class cornucopia(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cornucopia"
        self.bodyText = c.bb("5x, 'Plow' Play.")
        self.publishPacking("{ HH } 1R / 1G / 1B / 1M / 1Random / 1L / 1Notnil.")
        self.publishRoundStart("Entoken this with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.plow(5, caster.play).func(card, caster, dino, enemies, passedInVisuals)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R'],
                                                                               h.acons([1, 'G'],
                                                                               h.acons([1, 'B'],
                                                                               h.acons([1, 'M'],
                                                                               h.acons([1, 'Random'],
                                                                               h.acons([1, 'L'],
                                                                               h.acons([1, 'Notnil'],
                                                                               'nil'))))))))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        self.publishToken(tk.prepare())


'''
class fruitsOfLabor(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fruits of Labor"
        ## self.name = "Fruits of Labor"
        ## self.bodyText = c.bb("4x, 'Plow' Play. Discard the Bottom Card of Draw.")
        self.bodyText = c.bb("+1 Action. Discard the Bottom Card of Draw. //4x, 'Plow' Play.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.discardBottomCardOfDraw().func(card, caster, dino, enemies, passedInVisuals)
            cf.plow(4, caster.play).func(card, caster, dino, enemies, passedInVisuals)
'''

'''
class callousedHands(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Calloused Hands"
        self.bodyText = c.bb("+1 Action. At Turn End, if you have 3+ Cards in Hand: //(1) Per Card in Hand minus 3, 'Plow' Draw. ") 
        ## //(2) To an Arbitrary Enemy, 1R-notick.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        self.triggers.append(r.reaction(self, True, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            pass

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            cardsInHandIgnoring3 = str(caster.hand.length() - 3)
            self.end_of_dino_turn_rt = r.rt(True,
                                            "^" + card.name + "^", "Cards in Hand > 3",
                                            cardsInHandIgnoring3 + "x: 'Plow' Draw")
                                            ## cardsInHandIgnoring3 + "x: 'Plow' Hand; Arbitrary 1R-notick")

            return (h.locateCardIndex(caster.play, card) >= 0 
                and (caster.hand.length() - 3) > 0
                and card.reacted_1 == False,
                    self.end_of_dino_turn_rt)

        def trigger(self, card, caster, dino, enemies):
            card.reacted_1 = True
            ## Max is for weird edge cases / bug prevention
            cf.plow(max(caster.hand.length() - 3, 0), caster.draw).func(card, caster, dino, enemies, vis.prefabEmpty)
            """
            for i in range(3, max(3, caster.hand.length())):
                cf.plow(4, caster.hand).func(card, caster, dino, enemies, vis.prefabEmpty)
                cf.numberX_toArbitraryEnemy_dealDamage(1, h.acons([1, 'R-notick'], 'nil')).func(card, caster, dino, enemies, vis.prefabEmpty)
            """

    ## BUGGY
    def resetCardStateTurnEnd(self):
        self.reacted_1 = False
'''

class appleWorm(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Apple Worm"
        self.bodyText = c.bb("+1 Action. 4B. //To the Previous Card in Play, Entoken it with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([4, 'B'],
                                                                               'nil'))

            previousCard, success = cf.getter_toPreviousCardInPlay().func(card, caster, dino, enemies, passedInVisuals)
            if success:
                previousCard.publishToken(tk.prepare())

class compostBin(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Compost Bin"
        self.bodyText = c.bb("2G-notick / 2B-notick.")
        self.publishRoundStart("Invisibly, to every [ iMuck ] Card: //(1) 0.33 Chance to Entoken it with <<prepared>>.")
        self.publishInitialization(muck = True)
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'G-notick'],
                                                                               h.acons([2, 'B-notick'],
                                                                               'nil')))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        locations = caster.getLocations()
        for card in locations:
            if card.initialized == "Muck" and cf.chance(0.33, onSuccess_noOutput = True,
                                                              onFailure_noOutput = True).func(card, caster, dino, enemies, passedInVisuals):
                card.publishToken(tk.prepare())

'''
class callousedHands(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Calloused Hands"
        self.bodyText = c.bb("+ Cantrip. At Turn End, if you have no Cards in Hand: 2x, 'Plow' Draw.") 
        self.publishPacking("6R-notick.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.dealDamage().func(self, caster, dino, enemies, passedInVisuals, h.acons([6, 'R-notick'],
                                                                           'nil'))
        

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "Empty Hand",
                                            "2x: 'Plow' Draw")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and caster.hand.length() == 0
                and card.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            card.reacted_1 = True
            cf.plow(2, caster.draw).func(card, caster, dino, enemies, vis.prefabEmpty)

    ## BUGGY
    def resetCardStateTurnEnd(self):
        self.reacted_1 = False
'''

class cherryBlossoms(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cherry Blossoms"
        self.bodyText = c.bb("+1 Card. At Turn End, to the Previous and Subsequent Card in Play: //(1) Entoken it with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "",
                                            "<<prepared>> on prior/next Card")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            previousCard, success1 = cf.getter_toPreviousCardInPlay().func(card, caster, dino, enemies, vis.prefabEmpty)
            if success1:
                previousCard.publishToken(tk.prepare())
            subsequentCard, success2 = cf.getter_toSubsequentCardInPlay().func(card, caster, dino, enemies, vis.prefabEmpty)
            if success2:
                subsequentCard.publishToken(tk.prepare())

        def resetState_TurnEnd(self):
            self.reacted_1 = False

'''
class plantSeedsForSummertime(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Plant Seeds For Summertime"
        self.bodyText = c.bb("6x, 'Plow' Hand. Then, Discard Hand. //Take a 2nd Turn, wherein you Retain Action Count.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        ## self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()
'''

class dullOrchardAxe(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dull Orchard Axe"
        self.bodyText = c.bb("2R-notick / 2M; if non-Fatal, Entoken this with <<prepared>>.")
        ## self.publishRoundStart("Entoken this with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            damageData = cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'],
                                                                                            h.acons([2, 'M'],
                                                                                            'nil')))
            if not damageData.fatalDamage:
                h.splash("Dealt non-Fatal Damage: Entoken this with <<prepared>>.")
                card.publishToken(tk.prepare())

    ## def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
    ##     self.publishToken(tk.prepare())

'''
    Fast-Food Mascots
'''
class plastic(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Plastic"
        self.bodyText = c.bb("Destroy this.")
        self.publishPacking("0.25 Chance: Destroy this.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            if cf.chance(0.25).func(card, caster, dino, enemies, passedInVisuals):
                success = cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals, location = caster.pocket, suppressErrorText = True)
                if not success:
                    success = cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals, location = caster.hand)

'''
class strawberryShake(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Strawberry Shake"
        self.bodyText = c.bb("5x, to an Arbitrary.")
        self.table = ["Fast-Food Mascots"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals)
'''

class straws(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Straws"
        self.bodyText = c.bb("3x, to an Arbitrary Enemy: 1L; 0.33 Chance to Discard a Card.")
        self.publishPacking("3x, to an Arbitrary Enemy: 1L.")
        self.table = ["Fast-Food Mascots"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            pass






'''
    The Pier
'''

class fish(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fish"
        self.bodyText = c.bb("+1 Action. 1L. +1 Card. Destroy this.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

        ## For enemy uses

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'],
                                                                               'nil'))
            caster.drawCard()
            cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals)

class fishFry(DinoCard):
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
                caster.gainCard(fish(), caster.hand, position = caster.hand.length())

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            success = caster.moveMe(caster.hand, card, caster.draw, supressFailText = True)
            if not success:
                caster.moveMe(caster.pocket, card, caster.draw)

class sleepingWithTheFishes(DinoCard):
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
                    caster.gainCard(fish(), caster.discard)
            if anyDeadEnemies:
                input(" ... ")

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            success = caster.moveMe(caster.hand, card, caster.draw, supressFailText = True)
            if not success:
                caster.moveMe(caster.pocket, card, caster.draw)

class tackleBox(DinoCard):
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
                    caster.gainCard(fish(), caster.draw)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class goneFishing(DinoCard):
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
                caster.gainCard(fish(), caster.discard)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class weatheredBoat(DinoCard):
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

class fishPot(DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R'],
                                                                               h.acons([2, 'M'],
                                                                               'nil')))

            millCardFunction = cf.mill(usingCheckClause = True, checkClause = self.custom_checkClause)

            matchingCard = millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals, inputMatchCard = True)
            if matchingCard != 'NO MATCHES':
                caster.moveMe(millCardFunction.toLocation, matchingCard, caster.hand, position = caster.hand.length())
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

    def onLooted(self, dino):
        toAddCard = fish()
        toAddCard.publishInitialization(muck = True)
        dino.gainCard(toAddCard, dino.deck)

class dipNetting(DinoCard):
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

class useJunkAsBait(DinoShellCard):
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
                caster.gainCard(fish(), caster.discard)

class tangledFishLine(DinoCard):
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
                caster.gainCard(fish(), caster.hand, position = caster.hand.length())

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(5)

            success = caster.moveMe(caster.hand, card, caster.play, supressFailText = True)
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

class disphoticFishZone(DinoCard):
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
                    caster.gainCard(fish(), caster.hand, position = caster.hand.length())
                h.splash("With " + str(cardsInHand) + " Card(s) in Hand: Gained " + str(difference) + " ^Fish^ to Hand.")

            card.publishToken(tk.inoperable())

class aphoticFishZone(DinoCard):
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
                    caster.gainCard(fish(), caster.discard)
                h.splash("With " + str(cardsInHand) + " Card(s) in Hand: Gained " + str(difference) + " ^Fish^.")

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.packingText_PocketThis().func(card, caster, dino, enemies, passedInVisuals)

class rustyNetCutter(DinoCard):
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
                    caster.gainCard(fish(), caster.discard)

        def resetState_AfterAfterEntityAttacked(self):
            self.reacted_1 = False

'''
    Rubble Dwellers
'''

class rubble(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rubble"
        self.bodyText = c.bb("+ Cantrip. To an Arbitrary Enemy: Discard a Card.")
        self.table = ["Fundamental"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()
            attackedEnemy = cf.toBlankEnemy_DiscardBlank_fromHand(numberOfCardsToDiscard = 1,
                                                                  toArbitraryEnemy = 1).func(card, caster, dino, enemies, passedInVisuals)

class rubbleReorganizers(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rubble-Reorganizers"
        self.bodyText = c.bb("+1 Action. Then: 2x, Discard a Card. //Then: +3 Cards.")
        self.bodyText.lootingText("Gain 2 ^Rubble^.")
        self.table = ["Rubble-Dwellers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            for i in range(2):
                cf.arbitrarilyDiscardCardFrom_Location(caster.hand).func(card, caster, dino, enemies, passedInVisuals)
            for i in range(3):
                caster.drawCard()

    def onLooted(self, dino):
        for i in range(2):
            dino.gainCard(rubble())

class rubbleReclaimers(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rubble-Reclaimers"
        self.bodyText = c.bb("+2 Cards. //At Turn End, to the Subsequent Card in Play: Gain a Copy of it.")
        self.bodyText.heavinessText("{ HH }")
        self.bodyText.lootingText("Gain a ^Rubble^.")
        self.table = ["Rubble-Dwellers"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            for i in range(2):
                caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "",
                                            "Gain Copy of next Card")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            subsequentCard, success2 = cf.getter_toSubsequentCardInPlay().func(card, caster, dino, enemies, vis.prefabEmpty)
            if success2:
                caster.gainCopyOfCard(subsequentCard, caster.discard)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

    def onLooted(self, dino):
        for i in range(1):
            dino.gainCard(rubble())

class rubbleRequesters(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rubble-Requesters"
        self.bodyText = c.bb("+1 Action. //At Every Turn End, if you have 3+ Cards in Hand: //(1) Gain a ^Rubble^.")
        self.bodyText.heavinessText("{ HH }")
        self.bodyText.lootingText("Gain a ^Rubble^.")
        self.table = ["Rubble-Dwellers"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "3+ Cards in Hand",
                                            "Gain a ^Rubble^")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            ## 3+ Cards in hand?
            if caster.hand.length() < 3:
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            caster.gainCard(rubble(), caster.discard)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

    def onLooted(self, dino):
        for i in range(1):
            dino.gainCard(rubble())

'''
    Cattle Caste System
'''

class inWaitingCounterRevolt(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "In-Waiting Counter-Revolt"
        self.bodyText = c.bb("+1 Action. (2M x4). +1 Card.")
        self.publishDollarTrigger("WTI-Zones of yours (EXCEPT Play and Discard), at your Turn End, if you have 2+ Actions, you may: Move this onto Draw.")
        self.publishInitialization(muck = True)
        self.publishReshuffle(muck = True)
        self.table = ["Cattle Caste System"]
        self.bundle(throwCardFunction = self.duringPlay())

        ## self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))
        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'M'],
                                                                 h.acons([2, 'M'],
                                                                 h.acons([2, 'M'],
                                                                 h.acons([2, 'M'],
                                                                 'nil')))))
            caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^", "2+ Actions",
                                            "Move this onto Draw")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            ## Is this in a location EXCLUDING play and discard?
            locationName = caster.findMe(card).getName()
            if locationName == 'play' or locationName == 'discard':
                return (False, r.EMPTY_RT)

            ## 2+ Actions remaining?
            return (caster.actions >= 2
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            fromLocation = caster.findMe(card)
            caster.moveMe(fromLocation, card, caster.draw, position = 0)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class revolutionarysMilitia(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Revolutionary's Militia"
        self.bodyText = c.bb("Break a Band.")
        self.publishInitialization(muck = True)
        self.publishReshuffle(muck = True)
        self.bodyText.lootingText("Change a Card in Deck to: [ iMuck ], < iMuck >.")
        self.table = ["Cattle Caste System"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.breakABand().func(card, caster, dino, enemies, passedInVisuals)

    def onLooted(self, dino):
        card = h.fetchCardFromLocation("Change a Card in Deck to: [ iMuck ], < iMuck >", dino.deck)
        card.name = "MILITANT " + card.name
        card.publishInitialization(muck = True)
        card.publishReshuffle(muck = True)

class persecutedProtestors(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Persecuted Protestors"
        self.bodyText = c.bb("+ Cantrip. +2 Cards.")
        self.publishInitialization(muck = True)
        self.publishReshuffle(muck = True)
        self.table = ["Cattle Caste System"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()
            for i in range(2):
                caster.drawCard()

class jailbreaker(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//confidant// Jailbreaker"
        self.bodyText = c.bb("> Change this to: [ iMuck ], < iMuck >. //> Then, Enshell this as Follows: //    > ... //    > At Turn End, Discard this.")
        self.isConfidant = True
        self.table = ["Cattle Caste System"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "LIBERATED " + cardToEnshell.name
        cardToEnshell.publishInitialization(muck = True)
        cardToEnshell.publishReshuffle(muck = True)
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("At Turn End, Discard this.", cf.dots()))
        cardToEnshell.triggers.append(r.reaction(cardToEnshell, False, self.trigger_1(cardToEnshell)))

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "",
                                            "Discard this")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            caster.discardMe(caster.play, card, dino, enemies, vis.prefabEmpty)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class cardOverlord(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Card Overlord"
        self.bodyText = c.bb("9G-notick. +1 Card. Draw 1 More Card for your Next Turn.")
        self.publishPacking("Entoken this with <<feathery>>. Draw a Card to the Into-Hand mat.")
        self.publishRoundStart("+ Cantrip.")
        self.table = ["Cattle Caste System"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([9, 'G-notick'],
                                                                               'nil'))
            caster.drawCard()
            caster.plusUpcomingPlusCard(0, 1)
            ## caster.moveMe(caster.play, card, caster.hand, position = caster.hand.length(), supressFailText = True)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.publishToken(tk.feathery())
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.plusActions(1)
        caster.drawCard()

class freedomTrail(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Freedom Trail"
        self.bodyText = c.bb("+3 Cards. At Turn End, you may: Discard this, for +3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Cattle Caste System"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            for i in range(3):
                caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^", "",
                                            "Discard this for +3 Cards")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            caster.discardMe(caster.play, card, dino, enemies, vis.prefabEmpty)
            for i in range(3):
                caster.drawCard(printCard = True)
            h.splash("...")

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class autocratCapitulation(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Autocrat Capitulation"
        self.bodyText = c.bb("+1 Action. 1Row. //Once at Any Turn End, if you have 2+ Actions, you may: //(1) Plus 1 Action for your Next Turn, and Discard this.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Cattle Caste System"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Row'], 'nil'))

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(True,
                                            "^" + card.name + "^",
                                            "2+ Actions",
                                            "(1) Plus 1 Action for your Next Turn and Discard this.")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0
                and caster.actions >= 2
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            caster.plusUpcomingPlusAction(0, 1)
            caster.discardMe(caster.play, card, dino, enemies, vis.prefabEmpty)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

class surveillanceState(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Surveillance State"
        self.bodyText = c.bb("(1Row x1).")
        self.publishDollarTrigger("WTI-Hand or Pocket, During your Turns when you Play a Card, after Resolution, if said Card is not in Play: //(1) Uptick all #x and x# values on this Card by 1.")
        self.table = ["Cattle Caste System"]
        ## self.bundle(throwCardFunction = self.duringPlay())

        ## self.triggers.append(r.reaction(self, True, self.trigger_1(self)))


'''
    Debuffs
'''
class lethargic(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Lethargic"
        self.bodyText = c.bb("> ... //> -1 Action.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "LETHARGIC " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("-1 Action.", cf.minusXActions(1)))

class dirty(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Dirty"
        self.bodyText = c.bb("> [ iMuck ] ...")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "DIRTY " + cardToEnshell.name
        cardToEnshell.publishInitialization(muck = True)

class misplaced(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Misplaced"
        self.bodyText = c.bb("> [ iDiscard ] ...")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "MISPLACED " + cardToEnshell.name
        cardToEnshell.publishInitialization(discard = True)

class heavy(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Heavy"
        self.bodyText = c.bb("> { HH } ...")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "HEAVY " + cardToEnshell.name
        cardToEnshell.bodyText.heavinessText("{ HH }")
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("", cf.foreverLinger()))

class inRuins(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// In-Ruins"
        self.bodyText = c.bb("> ... //> Gain a ^Junk^.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "IN-RUINS " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("Gain a ^Junk^.", cf.gainACard(junk)))

class invigorating(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Invigorating"
        self.bodyText = c.bb("> ... //To an Arbitrary Enemy: +1 Action.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "INVIGORATING " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("To an Arbitrary Enemy: +1 Action.",
                                                                               cf.toBlankEnemy_Plus1Action(toArbitraryEnemy = True)))

class undercover(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Undercover"
        self.bodyText = c.bb("> ... //To an Arbitrary Enemy: Heal 1L.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "UNDERCOVER " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("To an Arbitrary Enemy: Heal 1Random.",
                                                                               cf.toBlankEnemy_Heal(h.acons([1, 'Random'], 'nil'),
                                                                               toArbitraryEnemy = True)))

class doubleAgent(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Double-Agent"
        self.bodyText = c.bb("> ... //To an Arbitrary Enemy: Heal 2M.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "DOUBLE-AGENT " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("To an Arbitrary Enemy: Heal 2M.",
                                                                               cf.toBlankEnemy_Heal(h.acons([2, 'M'], 'nil'),
                                                                               toArbitraryEnemy = True)))

'''
class antitrust(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Antitrust"
        self.bodyText = c.bb("~ Skip the Next Shop.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        dino.skipNextShop = True
'''


'''
class finalStraw(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Final Straw"
        ## self.bodyText = c.bb("~ When Looted, Enshell a Card as follows: //> { HH } Shell this. //> ... //> + Cantrip.")
        self.bodyText = c.bb("> { HH } Shell this. //> ... //> + Cantrip.")
        self.table = ["Fallow Farmland"]

    ## This is a good example of how to do this, but we have a Cantrip C.F. function now.
    class customBelowTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard()
            caster.plusActions(1)

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "CONCLUDING " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("{ HH } Shell this.", cf.foreverLingerShellThis()),
                                   belowThrowTextWrapper = cf.shellTextWrapper("+ Cantrip.", self.customBelowTextFunction()))
'''