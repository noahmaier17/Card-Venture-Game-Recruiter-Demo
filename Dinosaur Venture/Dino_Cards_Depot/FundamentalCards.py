import math, random, os, copy
import card as c
import helper as h
import cardFunctions as cf
import cardModFunctions as cmf
import cardTokens as tk
import getCardsByTable as gcbt
import mainVisuals as vis
import re
import react as r
from Dino_Cards_Depot import GeneralDinoCards as gdc
from colorama import init, Fore, Back, Style
init(autoreset=True)

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
