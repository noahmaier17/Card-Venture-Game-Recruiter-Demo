from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, mainVisuals as vis, channel_linked_lists as cll
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Fruit-Bearing Monks Cards
    Long lost at see, they have finally made landfall, and wish to spread their fruits upon the foreign land. 
'''

class missionary(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'R'], 'nil'))
    
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

class rowers(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'Notnil'], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 or self.turnsLingering == 2):
            ## h.splash("From ^" + self.name + "^: +1 Card.")
            caster.drawCard(printCard = True) 

class diligentDeckhand(gdc.DinoCard):
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
       
class castaway(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Castaway"
        self.bodyText = c.bb("6R.")
        self.publishPacking("Move a Card from Hand onto Draw.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([6, 'R'], 'nil'))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.moveACardFromHandOntoDraw().func(card, caster, dino, enemies, passedInVisuals)

class rescuedPlankwalker(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'B'], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 2):
            ## h.splash("")
            caster.discardMe(caster.play, self, dino, enemies, vis.prefabEmpty)

            while caster.draw.length() > 0:
                caster.discardCard(caster.draw, 0, dino, enemies, vis.prefabEmpty)

class anchorperson(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Anchorman"
        self.bodyText = c.bb("3M. From Hand, Pick a Card to Save, Discarding all others.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'M'], 'nil'))

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

class headCaptain(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Navigator"
        self.bodyText = c.bb("3G. Look at the top 3 Card of Draw; you may Discard them.")
        self.publishPacking("{ 2H } Play this.")
        self.table = ["Fruit-Bearing Monks"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'G'], 'nil'))
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
