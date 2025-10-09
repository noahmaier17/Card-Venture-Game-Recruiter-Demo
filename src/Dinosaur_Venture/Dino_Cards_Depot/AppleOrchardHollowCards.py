from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, cardTokens as tk, mainVisuals as vis, react as r
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Apple Orchard Hollow
'''
class orchardTree(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Orchard Tree"
        self.bodyText = c.bb("6G-notick / 1Random-notick. Move this into Hand.")
        self.publishPacking("2x, 'Plow' Draw.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([6, 'G-notick'],
                                                                               h.acons([1, 'Random-notick'],
                                                                               'nil')))
            success = caster.moveMe(caster.play, card, caster.hand, position = caster.hand.length(), supressFailText = True)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.plow(6, caster.draw).func(card, caster, dino, enemies, passedInVisuals)

class barnWood(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Barn Wood"
        self.bodyText = c.bb("+2 Cards. Entoken this with <<prepared>>.")
        self.publishPacking("Play this.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for i in range(2):
                caster.drawCard()
            card.publishToken(tk.prepare())

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            success = caster.playMe(caster.hand, card, caster, dino, enemies, passedInVisuals, supressFailText = False)
            if not success:
                caster.playMe(caster.pocket, card, caster, dino, enemies, passedInVisuals)

class grainCart(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Grain Cart"
        self.bodyText = c.bb("1R-notick / 1G-notick / 1B-notick.")
        self.publishPacking("Entoken this with <<prepared>>.")
        self.publishRoundStart("Entoken this with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                                               h.acons([1, 'G-notick'],
                                                                               h.acons([1, 'B-notick'],
                                                                               'nil'))))

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.publishToken(tk.prepare())

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        self.publishToken(tk.prepare())

'''
class disperseAppleSeeds(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Disperse Apple Seeds"
        self.bodyText = c.bb("3x, 'Plow' Hand.")
        self.publishPacking("3x, 'Plow' Draw.")
        self.bodyText.lootingText("Gain a ^Twig!^.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.plow(3, caster.hand).func(card, caster, dino, enemies, passedInVisuals)

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.plow(3, caster.draw).func(self, caster, dino, enemies, passedInVisuals)

    def onLooted(self, dino):
        dino.gainCard(twigExclamation(), dino.deck)
'''

class treeTrellis(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Tree Trellis"
        self.bodyText = c.bb("> Shell this, and Entoken it with <<prepared>>. //> ...")
        self.table = ["Apple Orchard Hollow"]

    class customTextFunction(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.shellThis().func(card, caster, dino, enemies, passedInVisuals)
            card.publishToken(tk.prepare())

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "TRELLIS OF " + cardToEnshell.name
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("Shell this, and Entoken it with <<prepared>>.", self.customTextFunction()))


class ripeMantra(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Ripe Mantra"
        self.bodyText = c.bb("+1 Action. 1R. +1 Card. //Mill, Unless a ^Junk^ is found; Discard such a Card. Then, Immill. //9x, 'Plow' Discard.")
        self.publishInitialization(top = True)
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def custom_checkClause(self, card):
            return (card.unmodifiedName == "Junk")

        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R'],
                                                                               'nil'))
            caster.drawCard()

            millCardFunction = cf.mill(usingCheckClause = True, checkClause = self.custom_checkClause)

            matchingCard = millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals, inputMatchCard = True)
            if matchingCard != 'NO MATCHES':
                caster.discardMe(millCardFunction.toLocation, matchingCard, dino, enemies, passedInVisuals)
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

            cf.plow(9, caster.discard).func(card, caster, dino, enemies, passedInVisuals)

class bobbingForApples(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bobbing For Apples"
        self.bodyText = c.bb("-1 Action. 2x, to an Arbitrary Card in Draw: //(1) Entoken it with <<prepared>>. //(2) Move it into Hand.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.minusActions(1)
            for i in range(2):
                card, success = cf.getter_toArbitraryCardInLocation(caster.draw).func(card, caster, dino, enemies, passedInVisuals)
                if success:
                    card.publishToken(tk.prepare())
                    caster.moveMe(caster.draw, card, caster.hand, position = caster.hand.length())

class prepareToHarvestApples(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Prepare To Harvest Apples"
        ## self.bodyText = c.bb("1R-notick / 1G-notick. //Next Turn, to Cards you Play, After Resolution: //(1) If in Play, Entoken it with <<prepared>>.")
        ## self.bodyText = c.bb("Next Turn, to Cards you Play, After Resolution: //(1) If in Play, Entoken it with <<prepared>>.")
        self.bodyText = c.bb("At the End of Next Turn, to all Cards in Play: //(1) Entoken it with <<prepared>>.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

        self.triggers.append(r.reaction(self, False, self.trigger_1(self)))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            ## cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
            ##                                                                    h.acons([1, 'G-notick'],
            ##                                                                    'nil')))

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                "^" + card.name + "^", "End of the Next Turn",
                                "<<prepared>> all Cards in Play")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if (not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments)
                or card.turnsLingering != 1):
                return (False, r.EMPTY_RT)

            ## Is this Card in Play?
            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            for card in caster.play.getArray():
                card.publishToken(tk.prepare())

        def resetState_TurnEnd(self):
            self.reacted_1 = False

    '''
    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.cardThatWasResolved = None

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if (not r.moments_isLeftInRight([r.AfterCardPlayResolution], moments)
                or card.turnsLingering != 1):
                return (False, r.EMPTY_RT)

            ## Fetches the Card
            moment_afterCardPlayResolution = r.moments_fetchInRight([r.AfterCardPlayResolution], moments)
            if moment_afterCardPlayResolution == None:
                return (False, r.EMPTY_RT)

            self.cardThatWasResolved = moment_afterCardPlayResolution.cardThatWasResolved

            ## Is the Card still in Play?
            if h.locateCardIndex(caster.play, self.cardThatWasResolved) == -1:
                return (False, r.EMPTY_RT)

            ## Success, unless reacted
            CARD_AFTER_PLAY_RESOLUTION = r.rt(False,
                                              "^" + card.name + "^",
                                              "^" + self.cardThatWasResolved.name + "^ is in Play after Resolve",
                                              "Entoken it with <<prepared>>")
            return (not self.reacted_1, CARD_AFTER_PLAY_RESOLUTION)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            self.cardThatWasResolved.publishToken(tk.prepare())
            self.cardThatWasResolved = None

        def resetState_AfterAnyCardResolves(self):
            self.reacted_1 = False
    '''

class cornucopia(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cornucopia"
        self.bodyText = c.bb("5x, 'Plow' Play.")
        self.publishPacking("{ HH } 1R / 1G / 1B / 1M / 1Random / 1L / 1Notnil.")
        self.publishRoundStart("Entoken this with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.plow(5, caster.play).func(card, caster, dino, enemies, passedInVisuals)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([1, 'R'],
                                                                               h.acons([1, 'G'],
                                                                               h.acons([1, 'B'],
                                                                               h.acons([1, 'M'],
                                                                               h.acons([1, 'Random'],
                                                                               h.acons([1, 'L'],
                                                                               h.acons([1, 'Notnil'],
                                                                               'nil'))))))))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        self.publishToken(tk.prepare())


'''
class fruitsOfLabor(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fruits of Labor"
        ## self.name = "Fruits of Labor"
        ## self.bodyText = c.bb("4x, 'Plow' Play. Discard the Bottom Card of Draw.")
        self.bodyText = c.bb("+1 Action. Discard the Bottom Card of Draw. //4x, 'Plow' Play.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.discardBottomCardOfDraw().func(card, caster, dino, enemies, passedInVisuals)
            cf.plow(4, caster.play).func(card, caster, dino, enemies, passedInVisuals)
'''

'''
class callousedHands(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Calloused Hands"
        self.bodyText = c.bb("+1 Action. At Turn End, if you have 3+ Cards in Hand: //(1) Per Card in Hand minus 3, 'Plow' Draw. ") 
        ## //(2) To an Arbitrary Enemy, 1R-notick.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        self.triggers.append(r.reaction(self, True, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            pass

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            cardsInHandIgnoring3 = str(caster.hand.length() - 3)
            self.end_of_dino_turn_rt = r.rt(True,
                                            "^" + card.name + "^", "Cards in Hand > 3",
                                            cardsInHandIgnoring3 + "x: 'Plow' Draw")
                                            ## cardsInHandIgnoring3 + "x: 'Plow' Hand; Arbitrary 1R-notick")

            return (h.locateCardIndex(caster.play, card) >= 0 
                and (caster.hand.length() - 3) > 0
                and card.reacted_1 == False,
                    self.end_of_dino_turn_rt)

        def trigger(self, card, caster, dino, enemies):
            card.reacted_1 = True
            ## Max is for weird edge cases / bug prevention
            cf.plow(max(caster.hand.length() - 3, 0), caster.draw).func(card, caster, dino, enemies, vis.prefabEmpty)
            """
            for i in range(3, max(3, caster.hand.length())):
                cf.plow(4, caster.hand).func(card, caster, dino, enemies, vis.prefabEmpty)
                cf.numberX_toArbitraryEnemy_dealDamage(1, h.acons([1, 'R-notick'], 'nil')).func(card, caster, dino, enemies, vis.prefabEmpty)
            """

    ## BUGGY
    def resetCardStateTurnEnd(self):
        self.reacted_1 = False
'''

class appleWorm(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Apple Worm"
        self.bodyText = c.bb("+1 Action. 4B. //To the Previous Card in Play, Entoken it with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([4, 'B'],
                                                                               'nil'))

            previousCard, success = cf.getter_toPreviousCardInPlay().func(card, caster, dino, enemies, passedInVisuals)
            if success:
                previousCard.publishToken(tk.prepare())

class compostBin(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Compost Bin"
        self.bodyText = c.bb("2G-notick / 2B-notick.")
        self.publishRoundStart("Invisibly, to every [ iMuck ] Card: //(1) 0.33 Chance to Entoken it with <<prepared>>.")
        self.publishInitialization(muck = True)
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'G-notick'],
                                                                               h.acons([2, 'B-notick'],
                                                                               'nil')))

    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
        locations = caster.getLocations()
        for card in locations:
            if card.initialized == "Muck" and cf.chance(0.33, onSuccess_noOutput = True,
                                                              onFailure_noOutput = True).func(card, caster, dino, enemies, passedInVisuals):
                card.publishToken(tk.prepare())

'''
class callousedHands(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Calloused Hands"
        self.bodyText = c.bb("+ Cantrip. At Turn End, if you have no Cards in Hand: 2x, 'Plow' Draw.") 
        self.publishPacking("6R-notick.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        cf.dealDamage().func(self, caster, dino, enemies, passedInVisuals, h.acons([6, 'R-notick'],
                                                                           'nil'))
        

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "Empty Hand",
                                            "2x: 'Plow' Draw")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and caster.hand.length() == 0
                and card.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            card.reacted_1 = True
            cf.plow(2, caster.draw).func(card, caster, dino, enemies, vis.prefabEmpty)

    ## BUGGY
    def resetCardStateTurnEnd(self):
        self.reacted_1 = False
'''

class cherryBlossoms(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cherry Blossoms"
        self.bodyText = c.bb("+1 Card. At Turn End, to the Previous and Subsequent Card in Play: //(1) Entoken it with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.drawCard()

    class trigger_1(r.card_responseAndTrigger):
        def __init__(self, card):
            super().__init__()
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^", "",
                                            "<<prepared>> on prior/next Card")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.AtTurnEnd, r.DinoTurn], moments):
                return (False, r.EMPTY_RT)

            return (h.locateCardIndex(caster.play, card) >= 0 
                and self.reacted_1 == False,
                    self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            self.reacted_1 = True
            previousCard, success1 = cf.getter_toPreviousCardInPlay().func(card, caster, dino, enemies, vis.prefabEmpty)
            if success1:
                previousCard.publishToken(tk.prepare())
            subsequentCard, success2 = cf.getter_toSubsequentCardInPlay().func(card, caster, dino, enemies, vis.prefabEmpty)
            if success2:
                subsequentCard.publishToken(tk.prepare())

        def resetState_TurnEnd(self):
            self.reacted_1 = False

'''
class plantSeedsForSummertime(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Plant Seeds For Summertime"
        self.bodyText = c.bb("6x, 'Plow' Hand. Then, Discard Hand. //Take a 2nd Turn, wherein you Retain Action Count.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())
        ## self.triggers.append(r.reaction(self, False, self.trigger_1(self), endOfDinoTurn = True))

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()
'''

class dullOrchardAxe(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dull Orchard Axe"
        self.bodyText = c.bb("2R-notick / 2M; if non-Fatal, Entoken this with <<prepared>>.")
        ## self.publishRoundStart("Entoken this with <<prepared>>.")
        self.table = ["Apple Orchard Hollow"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            damageData = cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'],
                                                                                            h.acons([2, 'M'],
                                                                                            'nil')))
            if not damageData.fatalDamage:
                h.splash("Dealt non-Fatal Damage: Entoken this with <<prepared>>.")
                card.publishToken(tk.prepare())

    ## def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals):
    ##     self.publishToken(tk.prepare())