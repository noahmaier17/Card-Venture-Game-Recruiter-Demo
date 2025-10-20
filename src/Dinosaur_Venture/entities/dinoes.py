"""
dinoes.py

Includes all the playable 'dino' characters, as well as the class by which they all inherit.
"""

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.entities import entity as e


class Dinosaur(e.Entity):
    """The main dinosaur class."""
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dinosaur"
        self.hp = cll.Healthcons(3, 3, 3, 'nil')
        self.enemy = False
        self.deckDraw = 4
        self.actions = 2
        self.upkeepActions = 2

        self.looting = 0
        self.uptickLooting = 1

        self.healR = 1
        self.healG = 1
        self.healB = 1

        self.resetR = 4 - self.healR
        self.resetG = 4 - self.healG
        self.resetB = 4 - self.healB

        # Text explaining what happens when you pass on looting
        self.passedLootingInfoText = "When passing on Looting or a Shop, you may: Destroy a Card from Deck."

    def passedLooting(
        self,
        clearingName: str, 
        roundCount: int,
        lootTables: list,
        pullsTable: list,
        picksTable: list,
        incrementTable: list
    ) -> None:
        """Handles functionality when this entity passes on looting at a Reset Stop."""
        # h.splash("When passing as '" + self.name + "', you may: Destroy a Card from Deck.", printInsteadOfInput = True)
        query = h.yesOrNo("Destroy a Card from Deck?")
        if query:
            pickedValue = h.pickValue("Destroy a Card", picksTable) - 1

            offset = 0
            priorOffset = -1
            while offset != priorOffset:
                priorOffset = offset
                offset = sum(incrementTable[0:picksTable[pickedValue] + offset])

            removedCard = self.deck.at(pickedValue + offset)
            self.deck.pop(pickedValue + offset)

            h.splash("Hopefully the ^" + removedCard.name + "^ is best left forgotten...")

        else:
            h.splash("Hopefully all is well with your deck...")

class Rover(Dinosaur):
    """The Rover character; very basic and vanilla character."""
    def __init__(self):
        super().__init__()
        self.text = "It has been left in the package for a decade, only now free to roam the cruel, changing, crying world. "
        ## "//Special Gimmick: At Turn Start, pockets a 'Petrol Mantra' [+1 Action. All Damage arrays you deal this turn are now the M channel.]"
        self.name = "Rover"

        cards = gcbt.getCardsByTable(["Packing Bot"])
        for card in cards.getArray():
            self.deck.append(card)
        for i in range(4):
            self.deck.append(gcbt.getCardByName("Junk"))

class Graverobber(Dinosaur):
    """
    The Graverobber Character.
    
    Starts with a hand size of 0, where their hand size increases by 1 every turn.
    """
    def __init__(self):
        super().__init__()
        self.text = "As a scrappy dinosaur, maybe there is something out in the beyond that can sedate its wandering soul."
        self.name = "Graverobber"

        cards = gcbt.getCardsByTable(["Graverobber"])
        for card in cards.getArray():
            self.deck.append(card)
        for i in range(2):
            self.deck.append(gcbt.getCardByName("Junk"))
        self.deckDraw = 0
        # self.deck.append(gcbt.getCardByName("miscellany"))

    def turnEndTidying(self, dino, enemies, passedInVisuals):
        for i in range(24):
            self.plusUpcomingPlusCard(i, 1)
        super().turnEndTidying(dino, enemies, passedInVisuals)

class Shepherd(Dinosaur):
    """Work-in-progress Shepherd Character."""
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Shepherd"

        cards = gcbt.getCardsByTable(["Shepherd"])
        for card in cards.getArray():
            self.deck.append(card)
        for i in range(3):
            self.deck.append(gcbt.getCardByName("Junk"))

'''
class HungryWolf(Dinosaur):
    def __init__(self):
        super().__init__()
        self.name = "Hungry Wolf"
    
    def roundStart(self):
        self.plusUpcomingPlusCard(0, 1)
        super().roundStart()
    
class Weewarrasaurus(Dinosaur):
    def __init__(self):
        super().__init__()
        self.name = "Weewarrasaurus"
        
    def atTriggerTurnStart(self, dino, enemies):    
        self.didOnceATurnAtTriggerTurnStart = True
        h.splash("Triggered innate turn start ability:", printInsteadOfInput = True)
        query = h.yesOrNo("Discard Hand for +3 Cards?")
        if query == True:
            size = len(dino.hand)
            for i in range(size):
                dino.discardCard(dino.hand, 0, dino, enemies, passedInVisuals)
            for i in range(3):
                dino.drawCard() 
'''
