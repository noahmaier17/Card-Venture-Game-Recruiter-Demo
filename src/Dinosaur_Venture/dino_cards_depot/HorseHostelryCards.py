import random
import re

from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import cardTokens as tk
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.dino_cards_depot import GeneralDinoCards as gdc

'''
    Horse Hostelry
'''
class bottleCaps(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bottle Caps"
        self.bodyText = c.bb("(1Notnil x3); //If Fatal or Broke a Band, Replace this with ^Broken Bottle^. //Otherwise, Discard this.")
        ## self.publishToken(tk.alliance())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            damageData = cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'Notnil'],
                                                                                            cll.Attackcons([1, 'Notnil'],
                                                                                            cll.Attackcons([1, 'Notnil'],
                                                                                            'nil'))))
            if damageData.fatalDamage:
                h.splash("Dealt Fatal Damage: Replacing this with ^Broken Bottle^.")
                card.mutateThis(gcbt.getCardByName("Broken Bottle"))
            elif damageData.brokeABand:
                h.splash("Broke a Band: Replacing this with ^Broken Bottle^.")
                card.mutateThis(gcbt.getCardByName("Broken Bottle"))
            else:
                caster.discardMe(caster.play, card, dino, enemies, passedInVisuals)

class cowboyDuelMantra(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cowboy Duel Mantra"
        self.bodyText = c.bb("Pick an Enemy. 3x, to it: //(1) If it has any Cards in Hand, Discard a Card; Otherwise 1Notnil. //Replace this with ^Broken Bottle^.")
        ## self.publishPacking("Draw a Card to the Into-Hand mat.")
        ## self.publishPacking("Gain 3 ^Broken Bottle^ Cards onto the Into-Hand mat.")
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
            if index != -1:
                enemy = enemies[index]
                for i in range(3):
                    if enemy.hand.length() > 0:
                        enemy.discardCard(enemy.hand, random.randint(0, enemy.hand.length() - 1), dino, enemies, passedInVisuals)
                    else:
                        enemy.damage(caster, dino, enemies, cll.Attackcons([1, 'Notnil'], 'nil'))
            card.mutateThis(gcbt.getCardByName("Broken Bottle"))

    ## def onPacking(self, caster, dino, enemies, passedInVisuals):
    ##     super().onPacking(caster, dino, enemies, passedInVisuals)
    ##     caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

    ## def onPacking(self, caster, dino, enemies, passedInVisuals):
    ##     super().onPacking(caster, dino, enemies, passedInVisuals)
    ##     for i in range(3):
    ##         caster.gainCard(brokenBottle(), caster.intoHand)

class trotTrot(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trot Trot"
        self.bodyText = c.bb("+1 Action. 1R-notick / 1R. +1 Card. //Replace this with ^Broken Bottle^.")
        self.publishToken(tk.feathery())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'R-notick'],
                                                                               cll.Attackcons([1, 'R'],
                                                                               'nil')))
            caster.drawCard()
            card.mutateThis(gcbt.getCardByName("Broken Bottle"))

class goodBadAndUgly(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Good Bad and Ugly"
        self.bodyText = c.bb("1M / 1L / 1Random. +1 Card. //Replace this with ^Broken Bottle^.")
        self.publishToken(tk.alliance())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'M'],
                                                                               cll.Attackcons([1, 'L'],
                                                                               cll.Attackcons([1, 'Random'],
                                                                               'nil'))))
            caster.drawCard()
            card.mutateThis(gcbt.getCardByName("Broken Bottle"))

class expiredMilk(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Expired Milk"
        self.bodyText = c.bb("+1 Action. Pick an Enemy. To it: //(1) 1G-notick / 1M. //(2) Replace an Arbitrary Card in Hand with ^Broken Bottle^.")
        self.publishToken(tk.alliance())
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
            if index != -1:
                enemy = enemies[index]
                h.splash("To '" + enemy.name + "': 1G-notick / 1M; Replace an Arbitrary Card in Hand with ^Broken Bottle^.", printInsteadOfInput = True)
                enemy.damage(caster, dino, enemies, cll.Attackcons([1, 'G-notick'],
                                                    cll.Attackcons([1, 'M'],
                                                    'nil')))

                if enemy.hand.length() > 0:
                    position = random.randint(0, enemy.hand.length() - 1)
                    enemy.hand.at(position).mutateThis(gcbt.getCardByName("Broken Bottle"))
                else:
                    h.splash('FAIL_PICK_CARD')

class cowboysInExile(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cowboys In Exile"
        self.bodyText = c.bb("+2 Actions.")
        self.publishPacking("Entoken all Cards in Play with <<feathery>>.")
        self.publishToken(tk.alliance())
        self.publishInitialization(muck = True)
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(2)

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            for card in caster.play.getArray():
                card.publishToken(tk.feathery())

class getawayHorse(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Getaway Horse"
        ## "Trainyard Rendezvous"
        self.bodyText = c.bb("Discard all ^Junk^ in Hand. +4 Cards.")
        self.publishToken(tk.alliance())
        self.publishInitialization(muck = True)
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.discardAll_names_fromLocation(caster.hand, ["Junk"]).func(card, caster, dino, enemies, passedInVisuals)

            for i in range(4):
                caster.drawCard()

class icelandicHorse(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Icelandic Horse"
        self.bodyText = c.bb("+ Cantrip. Mill, Unless a Card with '+1 Card', '+X Cards' or '+ Cantrip' in body-text is found; Move such a Card into Hand. Then, Immill.")
        ## self.publishPacking("1B / 1M.")
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

        ## self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def custom_checkClause(self, card):
            text = card.bodyText.unpacking + " " + card.bodyText.core + " " + card.bodyText.packing
            cardsMatchObject = re.search("(\\d)+ Card[(s)(\\W)]", text)
            cantripMatchObject = re.search("\\+ Cantrip", text)
            return (cardsMatchObject != None) or (cantripMatchObject != None)

        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

            millCardFunction = cf.mill(usingCheckClause = True, checkClause = self.custom_checkClause)

            matchingCard = millCardFunction.mill_func(card, caster, dino, enemies, passedInVisuals, inputMatchCard = True)
            if matchingCard != 'NO MATCHES':
                caster.moveMe(millCardFunction.toLocation, matchingCard, caster.hand, position = caster.hand.length())
            millCardFunction.immill_func(card, caster, dino, enemies, passedInVisuals)

class sheriffsBadge(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Sheriff's Badge"
        self.bodyText = c.bb("> Entoken this with: <<feathery>>, <<alliance>>.")
        self.table = ["Horse Hostelry"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "HONORED " + cardToEnshell.name
        cardToEnshell.publishToken(tk.feathery())
        cardToEnshell.publishToken(tk.alliance())

class timeInABottle(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Time in a Bottle"
        self.bodyText = c.bb("+ Cantrip.")
        ## self.publishPacking("Take a 2nd Turn. To every Enemy: Take a 2nd Turn. //    Replace this with ^Broken Bottle^.")
        self.publishPacking("{ HH } Take a 2nd Turn. To every Enemy: Take a 2nd Turn. //    Gain a ^Broken Bottle^.")
        self.publishInitialization(muck = True)
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay(), packingCardFunction = self.duringPacking())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()

    class duringPacking(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True

            success = caster.moveMe(caster.hand, card, caster.play)
            if not success:
                caster.moveMe(caster.pocket, card, caster.play)

            caster.plusExtraTurn()
            for enemy in enemies:
                enemy.plusExtraTurn()
            ## card.mutateThis(brokenBottle())
            caster.gainCard(gcbt.getCardByName("Broken Bottle"), caster.discard)

class smashedBottles(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Smashed Bottles"
        self.bodyText = c.bb("")
        self.table = ["Horse Hostelry"]
        ## self.bundle(throwCardFunction = self.duringPlay())

class fightOrFlight(gdc.DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fight or Flight"
        self.bodyText = c.bb("1G-notick / 1B-notick / 1G / 1B.")
        self.publishPacking("Entoken the top Card of Draw with <<feathery>>.")
        self.table = ["Horse Hostelry"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            cf.dealDamage().func(card, caster, dino, enemies, passedInVisuals, cll.Attackcons([1, 'G-notick'],
                                                                               cll.Attackcons([1, 'B-notick'],
                                                                               cll.Attackcons([1, 'G'],
                                                                               cll.Attackcons([1, 'B'],
                                                                               'nil')))))
