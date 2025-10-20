from Dinosaur_Venture import card as c
from Dinosaur_Venture import cardFunctions as cf
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as gdc

'''
    Debuffs
'''
class lethargic(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Lethargic"
        self.bodyText = c.bb("> ... //> -1 Action.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "LETHARGIC " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("-1 Action.", cf.minusXActions(1)))

class dirty(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Dirty"
        self.bodyText = c.bb("> [ iMuck ] ...")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "DIRTY " + cardToEnshell.name
        cardToEnshell.publishInitialization(muck = True)

class misplaced(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Misplaced"
        self.bodyText = c.bb("> [ iDiscard ] ...")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "MISPLACED " + cardToEnshell.name
        cardToEnshell.publishInitialization(discard = True)

class heavy(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Heavy"
        self.bodyText = c.bb("> { HH } ...")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "HEAVY " + cardToEnshell.name
        cardToEnshell.bodyText.heavinessText("{ HH }")
        cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("", cf.foreverLinger()))

class inRuins(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// In-Ruins"
        self.bodyText = c.bb("> ... //> Gain a ^Junk^.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "IN-RUINS " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("Gain a ^Junk^.", cf.gainACard(gcbt.getCardByName("Junk"))))

class invigorating(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Invigorating"
        self.bodyText = c.bb("> ... //To an Arbitrary Enemy: +1 Action.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "INVIGORATING " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("To an Arbitrary Enemy: +1 Action.",
                                                                               cf.toBlankEnemy_Plus1Action(toArbitraryEnemy = True)))

class undercover(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Undercover"
        self.bodyText = c.bb("> ... //To an Arbitrary Enemy: Heal 1L.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "UNDERCOVER " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("To an Arbitrary Enemy: Heal 1Random.",
                                                                               cf.toBlankEnemy_Heal(cll.Attackcons([1, 'Random'], 'nil'),
                                                                               toArbitraryEnemy = True)))

class doubleAgent(gdc.DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Double-Agent"
        self.bodyText = c.bb("> ... //To an Arbitrary Enemy: Heal 2M.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        cardToEnshell.name = "DOUBLE-AGENT " + cardToEnshell.name
        cardToEnshell.publishShell(belowThrowTextWrapper = cf.shellTextWrapper("To an Arbitrary Enemy: Heal 2M.",
                                                                               cf.toBlankEnemy_Heal(cll.Attackcons([2, 'M'], 'nil'),
                                                                               toArbitraryEnemy = True)))

'''
class antitrust(DinoShellCard):
    def __init__(self):
        super().__init__()
        self.name = "//shell// Antitrust"
        self.bodyText = c.bb("~ Skip the Next Shop.")
        self.table = ["Debuffs"]

    def onLootedEnshelling(self, dino, cardToEnshell):
        dino.skipNextShop = True
'''