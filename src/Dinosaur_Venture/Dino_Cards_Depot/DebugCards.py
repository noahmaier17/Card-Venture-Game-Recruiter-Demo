from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

''' 
    Debug/Testing Suite
'''
class draw6(gdc.DinoCard):
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

class drawAll(gdc.DinoCard):
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

class pocketTest(gdc.DinoCard):
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

class megaDamage(gdc.DinoCard):
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

class cantrip(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cantrip"
        self.bodyText = c.bb("+ Cantrip.")
        self.table = ["Debug"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()