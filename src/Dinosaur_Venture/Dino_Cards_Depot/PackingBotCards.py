from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, react as r
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Packing Bot Cards
'''
class metalCrate(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Metal Crate"
        self.bodyText = c.bb("1M / 1M.")
        ## self.bodyText.heavinessText("{ HH }")
        ## self.bodyText.lootingText("When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            ## card.foreverLinger = True
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], h.acons([1, 'M'], 'nil')))

    '''
    def onReplacedWithLoot(self, dino, newCard):
        h.splash("Triggered On Replaced with Loot: +1 Looting.")
        dino.looting += 1
    '''

class packingPeanuts(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Packing Peanuts"
        self.bodyText = c.bb("1L. Then: 1L.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'], 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'L'], 'nil'))

'''
class shippingTape(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shipping Tape"
        self.bodyText = c.bb("2R.")
        ## self.bodyText.lootingText("WTID, when you Loot a Card, you may change its Initialization Location to: (1) Top; (2) Bottom; (3) Discard.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))
'''

class forkliftCertificate(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Forklift Certificate"
        self.bodyText = c.bb("+2 Actions. At Turn End, if you have 2+ ^Junk^ in Play: //(1) Move this onto the Into-Hand Mat.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(2)
            ## caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "2+ ^Junk^ in Play",
                                            "Move this onto the Into-Hand Mat")
            ##  --> Static because: the trigger is always 100% what it says it will be. 

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            detritusCount = 0
            ## Sees if Card is in desired Location
            if h.locateCardIndex(caster.play, card) >= 0:
                ## Sees if Card there exists a Detritus in Play
                for cardInPlay in caster.play.getArray():
                    if (cardInPlay.unmodifiedName == "Junk"):
                        detritusCount += 1
            return (detritusCount >= 2, self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            index = h.locateCardIndex(caster.play, card)
            if index >= 0:
                caster.moveCard(caster.play, index, caster.intoHand)
                h.splash(self.END_OF_DINO_TURN_RT.getText(), printInsteadOfInput = True)
            else:
                h.splash('FAIL_MOVE')

class newFreshAir(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "New Fresh Air"
        self.bodyText = c.bb("+1 Action. 1G-notick.")
        self.publishPacking("1G-notick.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

class stampGun(gdc.DinoCard):
    def __init__(self): 
        super().__init__()
        self.name = "Stamp Gun"
        self.bodyText = c.bb("1R-notick / 1B-notick.")
        self.publishPacking("Draw a Card to the Into-Hand mat.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                 h.acons([1, 'B-notick'],
                                                                 'nil')))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class warehouseHelmet(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Warehouse Helmet"
        self.bodyText = c.bb("+3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            for i in range(3):
                caster.drawCard()

class filledFile(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Filled File"
        self.bodyText = c.bb("1Notnil.")
        ## self.bodyText.push("looting", "When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Notnil'], 'nil'))

class potpourri(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Potpourri"
        self.bodyText = c.bb("1Random.")
        ## self.bodyText.push("looting", "When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'Random'], 'nil'))

