from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, getCardsByTable as gcbt, mainVisuals as vis, react as r
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Rubble Dwellers
'''

class rubbleReorganizers(gdc.DinoCard):
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
            dino.gainCard(gcbt.getCardByName("Rubble"))

class rubbleReclaimers(gdc.DinoCard):
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
            dino.gainCard(gcbt.getCardByName("Rubble"))

class rubbleRequesters(gdc.DinoCard):
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
            caster.gainCard(gcbt.getCardByName("Rubble"), caster.discard)

        def resetState_TurnEnd(self):
            self.reacted_1 = False

    def onLooted(self, dino):
        for i in range(1):
            dino.gainCard(gcbt.getCardByName("Rubble"))
