from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import cardTokens as tk
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis
from Dinosaur_Venture import react as r
from Dinosaur_Venture.dino_cards_depot import GeneralDinoCards as gdc

'''
    Chicken Coup
'''

class inWaitingCounterRevolt(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "In-Waiting Counter-Revolt"
        self.bodyText = c.bb("+1 Action. (2M x4). +1 Card.")
        self.publishDollarTrigger("WTI-Zones of yours (EXCEPT Play and Discard), at your Turn End, if you have 2+ Actions, you may: Move this onto Draw.")
        self.publishInitialization(muck = True)
        self.publishReshuffle(muck = True)
        self.table = ["Chicken Coup"]
        self.bundle(throwCardFunction = self.duringPlay())

        ## self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))
        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'M'],
                                                                 cll.Attackcons([2, 'M'],
                                                                 cll.Attackcons([2, 'M'],
                                                                 cll.Attackcons([2, 'M'],
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

class revolutionarysMilitia(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Revolutionary's Militia"
        self.bodyText = c.bb("Break a Band.")
        self.publishInitialization(muck = True)
        self.publishReshuffle(muck = True)
        self.bodyText.lootingText("Change a Card in Deck to: [ iMuck ], < iMuck >.")
        self.table = ["Chicken Coup"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.breakABand().func(card, caster, dino, enemies, passedInVisuals)

    def onLooted(self, dino):
        card = h.fetchCardFromLocation("Change a Card in Deck to: [ iMuck ], < iMuck >", dino.deck)
        card.name = "MILITANT " + card.name
        card.publishInitialization(muck = True)
        card.publishReshuffle(muck = True)

class persecutedProtestors(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Persecuted Protestors"
        self.bodyText = c.bb("+ Cantrip. +2 Cards.")
        self.publishInitialization(muck = True)
        self.publishReshuffle(muck = True)
        self.table = ["Chicken Coup"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()
            for i in range(2):
                caster.drawCard()

class jailbreaker(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//confidant// Jailbreaker"
        self.bodyText = c.bb("> Change this to: [ iMuck ], < iMuck >. //> Then, Enshell this as Follows: //    > ... //    > At Turn End, Discard this.")
        self.isConfidant = True
        self.table = ["Chicken Coup"]

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

class cardOverlord(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Card Overlord"
        self.bodyText = c.bb("9G-notick. +1 Card. Draw 1 More Card for your Next Turn.")
        self.publishPacking("Entoken this with <<feathery>>. Draw a Card to the Into-Hand mat.")
        self.publishRoundStart("+ Cantrip.")
        self.table = ["Chicken Coup"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([9, 'G-notick'],
                                                                               'nil'))
            caster.drawCard()
            caster.plusUpcomingPlusCard(0, 1)
            ## caster.moveMe(caster.play, card, caster.hand, position = caster.hand.length(), suppressFailText = True)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.publishToken(tk.feathery())
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.plusActions(1)
        caster.drawCard()

class freedomTrail(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Freedom Trail"
        self.bodyText = c.bb("+3 Cards. At Turn End, you may: Discard this, for +3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Chicken Coup"]
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

class autocratCapitulation(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Autocrat Capitulation"
        self.bodyText = c.bb("+1 Action. 1Row. //Once at Any Turn End, if you have 2+ Actions, you may: //(1) Plus 1 Action for your Next Turn, and Discard this.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Chicken Coup"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'Row'], 'nil'))

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

class surveillanceState(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Surveillance State"
        self.bodyText = c.bb("(1Row x1).")
        self.publishDollarTrigger("WTI-Hand or Pocket, During your Turns when you Play a Card, after Resolution, if said Card is not in Play: //(1) Uptick all #x and x# values on this Card by 1.")
        self.table = ["Chicken Coup"]
        ## self.bundle(throwCardFunction = self.duringPlay())

        ## self.triggers.append(r.reaction(self, True, self.trigger_1(self)))
