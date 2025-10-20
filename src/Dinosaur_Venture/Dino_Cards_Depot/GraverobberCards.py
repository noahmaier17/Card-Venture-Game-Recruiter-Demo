from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, cardTokens as tk, channel_linked_lists as cll
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Graverobber Cards
'''

class heirloom(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'M'],
                                                                 'nil'))

    # def onReplacedWithLoot(self, dino, newCard):
    #     h.splash("Triggered On Replaced with Loot: Changing Replacement Card with [ iTop ].")
    #     newCard.publishInitialization(top = True)

class emptyMantle(gdc.DinoCard):
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

class luggedCreature(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'B-notick'],
                                                                 'nil'))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.gainCard(holyShovel(), caster.pocket)

class faithfulHound(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Faithful Hound"
        self.bodyText = c.bb("1Notnil / 1Notnil.")
        self.publishRoundStart("Pocket a ^Friendly Bark^ Card.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'Notnil'],
                                                                 cll.Attackcons([1, 'Notnil'],
                                                                 'nil')))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        caster.gainCard(friendlyBark(), caster.pocket)

class spareSpade(gdc.DinoCard):
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

class stowaway(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Stowaway"
        self.bodyText = c.bb("+1 Action. 3G.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'G'],
                                                                 'nil'))

class willOWisps(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Will-o-Wisps"
        self.bodyText = c.bb("2x, to an Arbitrary Enemy: 1L.")
        # self.bodyText.lootingText("When Replaced with Loot: Change Replacement Card with [ iTop ].")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.numberX_toArbitraryEnemy_dealDamage(2, cll.Attackcons([1, 'L'], 'nil')).func(card, caster, dino, enemies, passedInVisuals)

    # def onReplacedWithLoot(self, dino, newCard):
    #     h.splash("Triggered On Replaced with Loot: Changing Replacement Card with [ iTop ].")
    #     newCard.publishInitialization(top = True)

class flickeringLantern(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Flickering Lantern"
        self.bodyText = c.bb("+1 Action. 1R-notick.")
        self.table = ["Graverobber"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'R-notick'],
                                                                 'nil'))

    '''
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.discardBottomCardOfDraw().func(self, caster, dino, enemies, passedInVisuals)

        success = caster.moveMe(caster.hand, self, caster.draw, position = caster.draw.length(), supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, self, caster.draw, position = caster.draw.length())
    '''

class courageBuilding(gdc.DinoCard):
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
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'B-notick'],
                                                                 cll.Attackcons([1, 'R'],
                                                                 'nil')))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.gainCard(trip(), caster.pocket)

class trip(gdc.DinoCard):
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

class friendlyBark(gdc.DinoCard):
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

class holyShovel(gdc.DinoCard):
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
