from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Fast-Food Mascots
'''

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

class straws(gdc.DinoCard):
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
