from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.dino_cards_depot import GeneralDinoCards as gdc

'''
    Muck Cards
'''
class junk(gdc.DinoCard):
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

class miscellany(gdc.DinoCard):
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
class shovel(gdc.DinoCard):
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

class rubbish(gdc.DinoCard):
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

class twigExclamation(gdc.DinoCard):
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

class brokenBottle(gdc.DinoCard):
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

class plastic(gdc.DinoCard):
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

class fish(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'L'],
                                                                               'nil'))
            caster.drawCard()
            cf.destroyThis().func(card, caster, dino, enemies, passedInVisuals)

class rubble(gdc.DinoCard):
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