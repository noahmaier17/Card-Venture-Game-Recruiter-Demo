from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, channel_linked_lists as cll
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    New Bear Order Cards
'''
class bearBeret(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Beret"
        self.bodyText = c.bb("# <-- a Non-Negative Number. #x, 0.67 Chance for a Success. //On all Successes: +# Actions. //Otherwise, +2 Actions.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            number = h.pickNonNegativeNumber("Pick a Non-Negative Number", passedInVisuals = passedInVisuals)
            text = ""
            onlySuccesses = True
            for i in range(number):
                if i != 0:
                    text += ", "

                if cf.chance(0.67, onSuccess_noOutput = True, onFailure_noOutput = True).func(card, caster, dino, enemies, passedInVisuals):
                    text += "Success"
                else:
                    text += "Failure"
                    onlySuccesses = False

            if text == "":
                text += "..."

            h.splash(text, printInsteadOfInput = True)
            if onlySuccesses:
                h.splash("Only Successes; +" + str(number) + " Action(s).")
                ## card.foreverLinger = True
                caster.plusActions(number)
            else:
                h.splash("Had a Failure; +2 Actions.")
                caster.plusActions(2)

            # caster.drawCard()

class playDead(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Play Dead"
        self.bodyText = c.bb("+4 Actions. Discard your Hand. +1 Card.")
        self.publishPacking("+4 Actions. 1B-notick.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(4)
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(4)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'B-notick'],
                                                                 'nil'))

class reveredBearSkull(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Revered Bear Skull"
        self.bodyText = c.bb("(1R-notick x8).")
        self.publishPacking("{ HH } Per Remaining Action, to that many Subsequent Turns: //    (1) Plus 1 Action.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(self, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                cll.Attackcons([1, 'R-notick'],
                                                                'nil')))))))))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            for i in range(caster.actions):
                caster.plusUpcomingPlusAction(i, 1)

class torchBearing(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Torch Bearing"
        self.bodyText = c.bb("+2 Actions.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

'''
class recyclingBin(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Recycling Bin"
        self.bodyText = c.bb("1B / 1B / 1B / 1G / 1G. //+1 Card. Discard the Bottom Card of Draw.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'B'],
                                                                 cll.Attackcons([1, 'B'],
                                                                 cll.Attackcons([1, 'B'],
                                                                 cll.Attackcons([1, 'G'],
                                                                 cll.Attackcons([1, 'G'],
                                                                 'nil'))))))

            caster.drawCard()
            cf.discardBottomCardOfDraw().func(card, caster, dino, enemies, passedInVisuals)
'''

'''
class boneGnaw(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bone-Gnaw"
        self.bodyText = c.bb("+1 Card. (1M x4).")
        self.publishRoundStart("Arbitrarily Discard 4 Cards of Draw.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard(printCard = True)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'M'],
                                                                 cll.Attackcons([1, 'M'],
                                                                 cll.Attackcons([1, 'M'],
                                                                 cll.Attackcons([1, 'M'],
                                                                 'nil')))))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        for i in range(4):
            cf.arbitrarilyDiscardCardFromDraw().func(self, caster, dino, enemies, passedInVisuals)
'''

class reclaimedApexPredation(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Reclaimed Apex Predation"
        self.bodyText = c.bb("> [ iTop ], < iTop > Shell this. //> ...")
        self.table = ["New Bear Order"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "APEX " + cardToEnshell.name
        cardToEnshell.publishInitialization(top = True)
        cardToEnshell.publishReshuffle(top = True)
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Shell this.", cf.shellThis()))

class shoulderHump(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shoulder Hump"
        self.bodyText = c.bb("5Notnil / 4Notnil.")
        self.publishPacking("{ 1H } Next Turn, +1 Action.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([5, 'Notnil'],
                                                                 cll.Attackcons([4, 'Notnil'],
                                                                 'nil')))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

            success = caster.moveMe(caster.hand, card, caster.play, supressFailText = True)
            if not success:
                success = caster.moveMe(caster.pocket, card, caster.play)

            card.custom1 = True

    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 and self.custom1 == True):
            caster.plusActions(1)
            self.custom1 = False

class honeyPot(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Honey Pot"
        self.bodyText = c.bb("Discard your Hand. //Next Turn, +2 Actions.")
        self.bodyText.heavinessText("{ 1H }")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            caster.plusActions(2)

class hibernation(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hibernation"
        self.bodyText = c.bb("To each Enemy that has yet to take a Turn: //(1) Discard their Hand. //Discard your Hand.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for enemy in enemies:
                if enemy.turn == 0:
                    h.splash("To '" + enemy.name + "': Discarding their Hand.", printInsteadOfInput = True)
                    while enemy.hand.length() > 0:
                        enemy.discardCard(enemy.hand, 0, dino, enemies, passedInVisuals)

            while caster.hand.length() > 0:
                caster.discardCard(caster.hand, 0, dino, enemies, passedInVisuals)

'''
class bearClaws(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Claws"
        self.bodyText = c.bb("3R. Then: 2B.")
        self.bodyText.heavinessText("{ HH }")
        self.publishPacking("Discard your Draw.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([3, 'R'],
                                                                 'nil'))
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([2, 'B'],
                                                                 'nil'))

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.discardYourDraw().func(self, caster, dino, enemies, passedInVisuals)
'''

class backScratcher(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Back Scratcher"
        self.bodyText = c.bb("+1 Action. (1L x6). +1 Card.")
        self.publishInitialization(discard = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'L'],
                                                                 cll.Attackcons([1, 'L'],
                                                                 cll.Attackcons([1, 'L'],
                                                                 cll.Attackcons([1, 'L'],
                                                                 cll.Attackcons([1, 'L'],
                                                                 cll.Attackcons([1, 'L'],
                                                                 'nil')))))))
            caster.drawCard()

class beesNest(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bees Nest"
        self.bodyText = c.bb("3x, to an Arbitrary Enemy: 1L. //Next Turn, +1 Action.")
        self.bodyText.heavinessText("{ 1H }")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            cf.numberX_toArbitraryEnemy_dealDamage(3, cll.Attackcons([1, 'L'], 'nil')).func(card, caster, dino, enemies, passedInVisuals)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            caster.plusActions(1)

class leaveNoTraceMantra(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Leave No Trace Mantra"
        self.bodyText = c.bb("+2 Actions. Move an Arbitrary non-^Muck^ Card from Discard into Hand.")
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

            caster.discard.shuffle()
            index = 0
            match = False
            while match == False and index < caster.discard.length():
                if "Muck" not in caster.discard.getArray()[index].table:
                    match = True
                    caster.moveCard(caster.discard, index, caster.hand, position = caster.hand.length())
                index += 1
            if match == False:
                h.splash("FAIL_MOVE")

class chaseUntilExhaustion(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Chase Until Exhaustion"
        self.bodyText = c.bb("+1 Action. 1Notnil. //Discard your Draw. 0.67 Chance for: { HH }.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'Notnil'],
                                                                 'nil'))
            cf.discardYourDraw().func(card, caster, dino, enemies, passedInVisuals)

            if cf.chance(0.67).func(card, caster, dino, enemies, passedInVisuals):
                card.foreverLinger = True
