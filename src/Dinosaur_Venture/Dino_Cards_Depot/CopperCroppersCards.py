from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import react as r
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Copper Croppers
'''
class rebuildOrDestroy(gdc.DinoCard):
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

class troughBoy(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([4, 'B-notick'], 'nil'))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.breakABand().func(card, caster, dino, enemies, passedInVisuals)

class collectiveBargaining(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'G'], 'nil'))

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

class attemptAppeasement(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'B'], 'nil'))

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

class cardOverthrow(gdc.DinoCard):
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
                enemies[index].damage(caster, dino, enemies, cll.Attackcons([4, 'Notnil'], 'nil'))
                while enemies[index].hand.length() > 0:
                    enemies[index].discardCard(enemies[index].hand, 0, dino, enemies, passedInVisuals)

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.drawCard()

class dethronement(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dethronement"
        self.bodyText = c.bb("-1 Action. 4M / 2G. //Discard the Top Card of Draw. //Discard the Bottom Card of Draw.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.minusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([4, 'M'],
                                                                 cll.Attackcons([2, 'G'],
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

class failedPeaceTreaty(gdc.DinoCard):
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

            cf.toEveryEnemy_dealDamage(cll.Attackcons([2, 'Random-notick'], 'nil')).func(card, caster, dino, enemies, passedInVisuals)

class actionOverthrow(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Action Overthrow"
        self.bodyText = c.bb("2R. Then: 2R.")
        self.publishRoundStart("+1 Action.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'R'], 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'R'], 'nil'))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.plusActions(1)

class newFarmLeader(gdc.DinoCard):
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

            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'G'], 'nil'))

    def onLooted(self, dino):
        card = h.fetchCardFromLocation("Change a Card in Deck to: [ iTop ]", dino.deck)
        card.name = "NEW-ORDER " + card.name
        card.publishInitialization(top = True)

class bayOfPigs(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bay of Pigs"
        self.bodyText = c.bb("2Random-notick / 2Random-notick / 2Random-notick.")
        self.publishPacking("{ HH } Next Turn, +1 Action.")
        self.table = ["Copper Croppers"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'Random-notick'],
                                                                 cll.Attackcons([2, 'Random-notick'],
                                                                 cll.Attackcons([2, 'Random-notick'],
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

class hatchingCoup(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([4, 'R-notick'],
                                                                 cll.Attackcons([4, 'B-notick'],
                                                                 cll.Attackcons([2, 'M'],
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

class organizedArmaments(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, "null", cll.Attackcons([1, 'M'], 'nil'))

        def resetState_TurnEnd(self):
            self.reacted_1 = False