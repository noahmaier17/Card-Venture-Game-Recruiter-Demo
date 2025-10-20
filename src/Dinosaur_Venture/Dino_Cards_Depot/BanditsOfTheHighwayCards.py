from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Bandits of the Highway Cards
'''
class coercionCultivator(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Coercion Cultivator"
        self.bodyText = c.bb("+1 Action. 1L; if non-Fatal, Pocket a ^Shovel^ Card.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)

            damageData = cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'L'],
                                                                                            'nil'))
            if not damageData.fatalDamage:
                h.splash("Dealt non-Fatal Damage: Pocket a ^Shovel^ Card.")
                caster.gainCard(gcbt.getCardByName("Shovel"), caster.pocket)

class carCasing(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Car Casing"
        self.bodyText = c.bb("0.67 Chance for: 2R-notick / 2G-notick / 2B-notick / 2M. //Otherwise: Pocket this.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            if cf.chance(0.67, onSuccess_printInsteadOfInput = True).func(card, caster, dino, enemies, passedInVisuals):
                cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'R-notick'],
                                                                     cll.Attackcons([2, 'G-notick'],
                                                                     cll.Attackcons([2, 'B-notick'],
                                                                     cll.Attackcons([2, 'M'],
                                                                     'nil')))))
            else:
                caster.moveMe(caster.play, card, caster.pocket)


class highwayGrassMedian(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Highway-Grass Median"
        self.bodyText = c.bb("2G-notick / 2B-notick. //You may Discard your Hand for: + Cantrip. //0.25 Chance for: + Cantrip.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'G-notick'],
                                                                 cll.Attackcons([2, 'B-notick'],
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

class hunkOfJunk(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.bodyText = c.bb("+1 Action. 1G / 1G-notick / 1R / 1R-notick. //You may: (+1 Card. 0.5 Chance for: Pocket a ^Rubbish^.).")
        self.name = "Hunk of Junk"
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'G'],
                                                                 cll.Attackcons([1, 'G-notick'],
                                                                 cll.Attackcons([1, 'R'],
                                                                 cll.Attackcons([1, 'R-notick'],
                                                                 'nil')))))
            query = h.yesOrNo("+1 Card and 0.5 Chance for: Pocket a Rubbish Card?", passedInVisuals = passedInVisuals)
            if query:
                caster.drawCard()
                if cf.chance(0.5).func(card, caster, dino, enemies, passedInVisuals):
                    caster.gainCard(gcbt.getCardByName("Rubbish"), dino.pocket)

class brakeCutters(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Brake Cutters"
        self.bodyText = c.bb("+1 Action. 1M / 1M / 1M. Gain a ^Rubbish^.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'M'], cll.Attackcons([1, 'M'], cll.Attackcons([1, 'M'], 'nil'))))
            caster.gainCard(gcbt.getCardByName("Rubbish"), dino.discard)

class wheelShrapnel(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Wheel Shrapnel"
        self.bodyText = c.bb("+1 Action. 2R-notick / 2M. Discard your Hand.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'R-notick'], cll.Attackcons([2, 'M'], 'nil')))
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)

class shamSpeedSign(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Sham Speed Sign"
        self.bodyText = c.bb("2B. +3 Cards.")
        self.publishPacking("Pocket this.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'B'], 'nil'))
            for i in range(3):
                caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.packingText_PocketThis().func(card, caster, dino, enemies, passedInVisuals)

class bandItBond(gdc.DinoCard):
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

class infiltratorInterrogators(gdc.DinoCard):
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
        caster.gainCard(gcbt.getCardByName("Rubbish"), caster.pocket)

class raccoonHeist(gdc.DinoCard):
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
            caster.gainCard(gcbt.getCardByName("Shovel"), dino.pocket)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'B'],
                                                                               cll.Attackcons([1, 'B'],
                                                                               'nil')))

class roadSignAugers(gdc.DinoCard):
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
        caster.gainCard(gcbt.getCardByName("Shovel"), caster.pocket)

class carFeigning(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Car Feigning"
        self.bodyText = c.bb("1G / 1R. If your Hand is Empty: + Cantrip; + Cantrip.")
        self.publishPacking("Pocket this.")
        self.table = ["Bandits of the Highway"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'G'], cll.Attackcons([1, 'R'], 'nil')))
            if dino.hand.length() == 0:
                h.splash("Hand is Empty, so: + Cantrip, + Cantrip.")
                for i in range(2):
                    caster.plusActions(1)
                    caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.packingText_PocketThis().func(card, caster, dino, enemies, passedInVisuals)

