"""
    channel_linked_lists.py

    Implements damage and HP objects that store health. 
    Additionally includes the hard-coded values for different types of damage. 
"""

from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import helper as h

class acons():
    """
    Implementation of attack damage linked list chains.

    Attributes:
        damage (int): the amount of damage this deals.
        channel (str): the damage channel type (R, G, B, L, M, Notnil, Random).
        tail (acons | 'nil'): the next attack node; 'nil' if none.
    """

    def __init__(self, datum: tuple[int, str], tail: "acons | 'nil'") -> None:
        """
        Initializer.
        
        Arguments:
            datum (damage: int, channel: channel_linked_lists.channel): damage and of what type.
            tail (acons | channel_linked_lists.nilcons): represents the next element of damage.
        """
        self.damage = datum[0]
        self.channel = datum[1]
        self.tail = tail

    def __str__(self) -> str:
        """Returns string representation, used for UI."""
        if self.tail == 'nil':
            return str(self.damage) + str(self.channel)
        else:
            return str(self.damage) + str(self.channel) + " / " + self.tail.__str__()

    def stripNotick(self) -> None:
        """Removes all instances of -notick from this damage chain."""
        if self.tail == 'nil':
            return
        else:
            if self.channel[-len("-notick"):len(self.channel)] == '-notick':
                self.channel = self.channel[0:-len("-notick")]
            return self.tail.stripNotick()


class healthcons():
    """
    Implementation of health strings for an entity.

    Attributes:
        r (int): R-channel value.    
        g (int): G-channel value.    
        b (int): B-channel value.
        tail (healthcons | None): the next band of health. 
        isDeadHealthcons (bool): If the entity is dead. 
        onBreakDiscardHand (bool): When this band is broken, 
            if the entity will discard their hand.
        onBreakSpecial (bool): When this band is broken,
            if the entity will have some special mechanic once that happens.

    Notes:
        If onBreakDiscardHand == True, onBreakSpecial can be True or False.
    """
    def __init__(self, r: int, g: int, b: int, tail: "healthcons | 'nil'") -> None:
        self.r = r
        self.g = g
        self.b = b
        self.tail = tail
        self.isDeathHealthcons = False
        self.onBreakDiscardHand = False
        self.onBreakSpecial = False

    def append(self, otherHealthcons: "healthcons") -> None:
        """Places at the tail-end of this healthcons the other healthcons."""
        if self.tail == "nil":
            self.tail = otherHealthcons
        else:
            self.tail.append(otherHealthcons)

    def equals(self, otherHealthcons: "healthcons") -> bool:
        """Checks if two healthcons are equivalent."""
        # Are both dead?
        if self.isDeathHealthcons != otherHealthcons.isDeathHealthcons:
            return False

        # Do both have equal r, g, and b values for this band?
        if self.r != otherHealthcons.r or self.g != otherHealthcons.g or self.b != otherHealthcons.b:
            return False

        # Do we both have tails?
        if (self.tail == "nil") != (otherHealthcons.tail == "nil"):
            return False

        # Recurses if we have tails
        if (self.tail != "nil") and (otherHealthcons.tail != "nil"):
            return self.tail.equals(otherHealthcons.tail)
        
        # Otherwise, return True
        return True

    def getBands(self) -> int:
        """Returns the number of bands of this healthcons."""
        if self.tail == "nil":
            return 1
        else:  
            return 1 + self.tail.getBands()
    
    def publishBandBreak(self, number: int, discardHand: bool, special: bool) -> None:
        """
        Healthcons bands can break and cause specific triggers. This adds visuals for that.
        ONLY CALL THIS FROM THE ENTITY FUNCTION OF THE SAME NAME.
        """
        self.__publishBandBreak(number - 1, discardHand, special)
        
    def __publishBandBreak(self, number: int, discardHand: bool, special: bool) -> None:
        if number == 0:
            self.onBreakDiscardHand = discardHand
            self.onBreakSpecial = special
        elif self.tail == 'nil' or number < 0:
            raise ValueError("There is not a band that exists where we can publish a band break!")
        else:
            self.tail.__publishBandBreak(number - 1, discardHand, special)
    
    def displayHealth(self, normalizeValue: int) -> list[list]:
        """
        Converts this data structure into a nested array structure and colors each channel with colorama.
        
        Arguments:
            normalizeValue (int): the length of this string value. 
        """
        returnArray = self.toArray()
        returnText = ""
        for i in range(len(returnArray)):
            if i == 0:
                returnText += "["
                returnText += Fore.RED + str(returnArray[i][0]) + Fore.WHITE + ", "
                returnText += Fore.GREEN + str(returnArray[i][1]) + Fore.WHITE + ", "
                returnText += Fore.BLUE + str(returnArray[i][2]) + Fore.WHITE + "]"
                normalizeValue += 30
            
            if i >= 1:
                if self.onBreakDiscardHand:
                    returnText += " x "
                elif self.onBreakSpecial:
                    returnText += " * "
                else:
                    returnText += " - "
                
                total = str(sum(returnArray[i]))
                returnText += total + "?"

        return h.normalize(returnText, normalizeValue)
    
    def toArray(self) -> list[list]:
        """
        Converts this healthcons into a nested array structure.
        Example format with 2 bands: [ [1, 0, 0], [2, 0, 0] ]
        """
        if self.getBands() == 0:
            return [[0, 0, 0]]
        else:
            returnArray = []
            self.__toArray(returnArray)
            return returnArray
        
    def __toArray(self, returnArray: list) -> list[list]:
        returnArray.append([self.r, self.g, self.b])
        if self.tail != "nil":
            self.tail.__toArray(returnArray)

    def replaceBand(self, index: int, array: list) -> None:
        """
        Replaces the ith band with this new band of HP.
        Expects index < number of bands.

        Arguments:
            index (int): which band to replace.
            array (list | tuple): the new HP of form [#, #, #].
        """
        if (index == 0):
            self.r = array[0]
            self.g = array[1]
            self.b = array[2]
            return
        else:
            self.tail.replaceBand(index - 1, array)

    def __str__(self) -> str:
        """
        Creates a string representation of the health counts.
        MOSTLY FOR DEBUGGING; for UI, use displayHealth.
        """
        if self.tail == "nil":
            return "["+str(self.r)+", "+str(self.g)+", "+str(self.b)+"]"
        else: 
            return "["+str(self.r)+", "+str(self.g)+", "+str(self.b)+"] - "+self.tail.__str__()

class deadHealthcons(healthcons):
    """
    A special type of healthcons when the entity is dead and all HP values should be 0.

    Notes:
        isDeathHealthcons = True in this case.
    """
    def __init__(self) -> None:
        super().__init__(0, 0, 0, 'nil')
        # The above does not matter at all
        self.isDeathHealthcons = True
    
    def getBands(self) -> int:
        # Entity is dead, so zero bands
        return 0
    
    def publishBandBreak(self) -> None:
        # Cannot publish a band break on this
        pass
    
    def displayHealth(self, normalizeValue: int) -> str:
        return h.normalize("[^, ^, ^]", normalizeValue)