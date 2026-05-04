import random
from enum import Enum
from typing import TYPE_CHECKING

from Dinosaur_Venture.cards.mechanics import card_tokens as tk
from Dinosaur_Venture.cards.mechanics.card_initalization_zones import \
    CardInsertionPostion

if TYPE_CHECKING:
    from Dinosaur_Venture.cards.mechanics import card as c

class CardLocation():
    """Array-like container of Cards."""
    def __init__(self, name: str) -> None:
        assert isinstance(name, str), f"Expected str, got {type(name)}: {name}"
        self.name = name
        self.array: list["c.Card"] = []

    def niceName(self) -> str:
        """Returns a nicer version if this card location's name."""
        return self.name.title()

    def length(self) -> str:
        """Length of the card location."""
        return len(self.array)

    def lengthExcludingFeathery(self) -> str:
        """Length of the card location excluding <<feathery>> cards."""
        count = 0
        for card in self.array:
            if tk.checkTokensOnThis(card, [tk.feathery()]) == False:
                count += 1
        return count

    def getName(self) -> str:
        """Getter of the name of this card location."""
        return self.name
    
    def append(self, card: "c.Card") -> None:
        """Appends the input card to the end of this card location."""
        self.array.append(card)
        
    def clear(self) -> None:
        """Clears this card location."""
        self.array.clear()
    
    def isEmpty(self) -> bool:
        """Returns True if this card location contains no cards."""
        return (len(self.array) == 0)
    
    def _indexErrorHandler(self, index: int, functionName: str) -> bool:
        """Throws a runtime error if the input index for some function is out of bounds."""
        if (index > len(self.array)):
            text = " ERROR: " + self.name + " had an unchecked " 
            text += functionName + "() called---there are no Cards at index " + str(index) + "!!! "
            input(text)
            return False
        return True

    def pop(self, index: int = 0) -> "c.Card":
        """Pops Cards off of this card location; default behavior removes the Card at the top of this card location."""
        self._indexErrorHandler(index, "pop")
        return self.array.pop(index)
    
    def at(self, index: int) -> "c.Card":
        """Fetches and returns the Card at the passed-in index."""
        self._indexErrorHandler(index, "at")
        return self.array[index]
        
    def insert(self, index: int, card: "c.Card") -> None:
        """Inserts the given Card at the given index within this card location."""
        self.array.insert(index, card)
        
    def shuffle(self) -> None:
        """Shuffles the card location."""
        random.shuffle(self.array)

    def reverse(self) -> None:
        """Reverses the ordering of this card location's cards."""
        otherList = []
        while len(self.array) > 0:
            otherList.insert(0, self.array.pop())

        while len(otherList) > 0:
            self.array.append(otherList.pop())

    def getArray(self) -> list["c.Card"]:
        return self.array

    def logIdentity(self) -> dict:
        return {
            "name": self.name,
            "cards": self.array
        }
    
    def __eq__(self, otherCardLocation: "CardLocation") -> bool:
        """Returns True if both objects are the same object."""
        return (self is otherCardLocation)
        
## Hard-coded constants to compare for naming of card locations
class CardZoneName(str, Enum):
    DECK = "deck"
    HAND = "hand"
    DISCARD = "discard"
    DRAW = "draw"
    PLAY = "play"
    INTO_HAND = "into-hand"
    INTO_INTO_HAND = "into-into-hand"
    POCKET = "pocket"