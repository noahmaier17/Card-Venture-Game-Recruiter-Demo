from Dinosaur_Venture import card as c
from Dinosaur_Venture import card_functions as cf
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.dino_cards_depot import general_dino_cards as gdc

'''
    Fallow Farmland
'''
class finalStraw(gdc.DinoShellCard):
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

class rustedScythe(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rusted Scythe"
        self.bodyText = c.bb("2R-notick / 2M. You may: Discard your Hand for +1 Card. //Then, +1 Card.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, cll.Rnotick()], 
                                                                               cll.Attackcons([2, cll.M()],
                                                                               'nil')),
                                                                               scriptedInput=scriptedInput)
            query = h.yesOrNo("Discard your Hand for +1 Card?", passedInVisuals=passedInVisuals, scriptedInput=scriptedInput)
            if query:
                cf.discardYourHand().func(card, caster, dino, enemies, passedInVisuals)
                dino.drawCard()
            dino.drawCard()

class cultivator(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cultivator"
        self.bodyText = c.bb("1M / 1M. Move this onto Draw.")
        self.publishPacking("Draw a Card to the Into-Hand mat.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, cll.M()],
                                                                               cll.Attackcons([1, cll.M()],
                                                                               'nil')),
                                                                               scriptedInput=scriptedInput)
            caster.moveMe(caster.play, card, caster.draw, position = 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class brassMuzzle(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Brass Muzzle"
        self.bodyText = c.bb("+1 Action. Pick an Enemy. To it: 2B / 2M; Discard a Card.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.plusActions(1)
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals, scriptedInput=scriptedInput)
            if index != -1:
                enemies[index].damage(caster, dino, enemies, cll.Attackcons([2, cll.B()], cll.Attackcons([2, cll.M()], 'nil')))
                if enemies[index].hand.length() > 0:
                    enemies[index].discardCard(enemies[index].hand, 0, dino, enemies, passedInVisuals)

class deadHarvestedGrass(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dead Harvested Grass"
        self.bodyText = c.bb("+1 Action. 3G. Then: 3L. //Draw until you have 1 Card in Hand.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, cll.G()], 'nil'), scriptedInput=scriptedInput)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, cll.L()], 'nil'), scriptedInput=scriptedInput)
            cf.drawUntilYouHaveXCardsInHand(1).func(card, caster, dino, enemies, passedInVisuals)

class gnawedCableCord(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Gnawed Cable Cord"
        self.bodyText = c.bb("+2 Actions. 2B-notick. Move this onto Draw.")
        self.publishPacking("Draw a Card to the Into-Hand mat.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.plusActions(2)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, cll.Bnotick()], 'nil'),
                                                                               scriptedInput=scriptedInput)
            caster.moveMe(caster.play, card, caster.draw, position = 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class rust(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Rust"
        ## self.bodyText = c.bb("~ When Looted, Enshell a Card as follows: //> Shell this. //> ... //> Draw until you have 3 Cards in Hand.")
        self.bodyText = c.bb("> Shell this. //> ... //> Draw until you have 3 Cards in Hand.")
        self.table = ["Fallow Farmland"]

    class customBelowTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.drawUntilYouHaveXCardsInHand(3).func(card, caster, dino, enemies, passedInVisuals)

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "RUSTED " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("{ HH } Shell this.", cf.foreverLingerShellThis()),
                                   belowThrowTextWrapper = cf.shellTextWrapper("Draw until you have 3 Cards in Hand.", self.customBelowTextFunction()))

class grasshopperCache(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Grasshopper Cache"
        self.bodyText = c.bb("Draw until you have 3 Cards in Hand.")
        self.publishPacking("2G-notick / 2M.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            cf.drawUntilYouHaveXCardsInHand(3).func(card, caster, dino, enemies, passedInVisuals)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, cll.Gnotick()], 
                                                                               cll.Attackcons([2, cll.M()],
                                                                               'nil')),
                                                                               scriptedInput=scriptedInput)

class trampledRodent(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trampled Rodent"
        self.bodyText = c.bb("+1 Action. 1R-notick / 1G-notick / 1B-notick / 1M. //Then, Discard an Arbitrary Card in Hand.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, cll.Rnotick()],
                                                                 cll.Attackcons([1, cll.Gnotick()],
                                                                 cll.Attackcons([1, cll.Bnotick()],
                                                                 cll.Attackcons([1, cll.M()],
                                                                 'nil')))), 
                                                                 scriptedInput=scriptedInput)
            cf.arbitrarilyDiscardCardFrom_Location(caster.hand, inputCard = True).func(card, caster, dino, enemies, passedInVisuals, scriptedInput=scriptedInput)

class twigRockScarecrow(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Twig-Rock Scarecrow"
        self.bodyText = c.bb("Plus 1 Action and Draw 1 More Card for your Next Turn. //Move this onto Draw.")
        self.publishPacking("1Random / 1Random.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.plusUpcomingPlusAction(0, 1)
            caster.plusUpcomingPlusCard(0, 1)
            caster.moveMe(caster.play, card, caster.draw, position = 0)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, cll.Random()],
                                                                               cll.Attackcons([1, cll.Random()],
                                                                               'nil')),
                                                                               scriptedInput=scriptedInput)

class mangledShrew(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Mangled Shrew"
        self.bodyText = c.bb("2R-notick / 1Notnil / 1Notnil / 1Notnil.")
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, cll.Rnotick()],
                                                                 cll.Attackcons([1, cll.Filled()],
                                                                 cll.Attackcons([1, cll.Filled()],
                                                                 cll.Attackcons([1, cll.Filled()],
                                                                 'nil')))),
                                                                 scriptedInput=scriptedInput)

class lastSeeds(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Last Seeds"
        self.bodyText = c.bb("+1 Action. 9L. +1 Card.")
        self.bodyText.lootingText("Gain a Copy of this.")
        self.publishInitialization(muck = True)
        self.table = ["Fallow Farmland"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals, scriptedInput=None):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([9, cll.L()],
                                                                               'nil'), 
                                                                               scriptedInput=scriptedInput)
            caster.drawCard()

    def onLooted(self, dino):
        dino.gainCopyOfCard(self, dino.deck)

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