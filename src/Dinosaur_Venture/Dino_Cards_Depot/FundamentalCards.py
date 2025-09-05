import math, random, os, copy, re
from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import card as c, helper as h, cardFunctions as cf, cardModFunctions as cmf, cardTokens as tk, getCardsByTable as gcbt, mainVisuals as vis, react as r
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

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
