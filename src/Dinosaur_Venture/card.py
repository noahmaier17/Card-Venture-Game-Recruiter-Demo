import uuid
from typing import TYPE_CHECKING

from Dinosaur_Venture import cardTokens as tk
from Dinosaur_Venture import helper as h

if TYPE_CHECKING:
    from Dinosaur_Venture import cardFunctions as cf
    from Dinosaur_Venture import react as r
    from Dinosaur_Venture.entities import entity as e
    from Dinosaur_Venture import mainVisuals as vis

INITIALIZATION_ZONES = {
    "iBottom": "Bottom",
    "iTop": "Top",
    "iDiscard": "Discard",
    "iInto_Hand": "Into Hand",
    "iDraw": "Draw",
    "iMuck": "Muck",
    "iPocket": "Pocket"
}
REVERSED_INITIALIZATION_ZONES = {}  ## Has the keys and values in the other order
for key in INITIALIZATION_ZONES.keys():
    REVERSED_INITIALIZATION_ZONES.update({INITIALIZATION_ZONES[key]: key})

## Creates the bodyText, making it so we can truncate certain details if they are not useful currently.
##  Types of input:
##   "core": what is input though the constructor, it has the fundamental bodyText of the thing. 
## Ordered..:
##   "u": UNPacking Phase Text
##   "p": Packing Phase Text
##   "looting": important during looting
##   "{}": important bracket-level items
##   "[]": initialization information
class bb():
    """
    Creates the bodyText, wherein we can truncate certain details if not currently useful.
    
    Attributes:
        core (str): the core throw text.
        unpacking (str): unpacking text.
        packing (str): packing text.
        looting (str): looting text.
        heaviness (str): heaviness text (often looks like { 1H } or { HH }).
        initialization (str): initialization location text, should be key of INITIALIZATION_ZONES.
        reshuffle (str): reshuffle location text, should be key of INITIALIZATION_ZONES.
        roundStart (str): round start text.
        dollarTriggers (list[str]): $ triggers.
    """
    def __init__(self, text: str) -> None:
        """Initializer; expects throw text as the `text` parameter."""
        self.core = text
        self.unpacking = ""
        self.packing = ""
        self.looting = ""
        self.heaviness = ""
        self.initialization = ""
        self.reshuffle = ""
        self.roundStart = ""
        self.dollarTriggers = []

    def appendThrowText(self, text: str, excludeLineBreak: bool = False) -> None:
        """Mutates the end of this' Throw text."""
        separator = " //"
        if excludeLineBreak:
            separator = " "
        self.core += separator + text

    def prependThrowText(self, text: str, excludeLineBreak: bool = False) -> None:
        """Mutates the start of this' Throw text."""
        separator = " //"
        if excludeLineBreak:
            separator = " "
        self.core = text + separator + self.core

    def mutateThrowText(self, text: str) -> None:
        """
        Changes the ENTIRE Throw text based on the `text` parameter.
        Do not use for initialization; use __init__ instead.
        """
        self.core = text ## + " //"

    def mutatePackingText(self, text: str) -> None:
        """Changes the ENTIRE Packing text based on the `text` parameter."""
        self.packing = text

    def mutateRoundStartText(self, text: str) -> None:
        """Changes the ENTIRE Round Start text based on the `text` parameter."""
        self.roundStart = text

    def push(self, textType, text):
        """
        Deprecated (use a call to something like `unpackingText()` instead).
        
        Based on a textType (u, p, looting, {}, []), changes the corresponding text.        
        """
        if textType == "u":
            self.unpackingText(text)
        elif textType == "p":
            self.packingText(text)
        elif textType == "looting":
            self.lootingText(text)
        elif textType == "{}":
            self.heavinessText(text)
        elif textType == "[]":
            self.initializationText(text)
        else:
            input("ERROR: wrong type! textType: " + textType + " !!! ")
    
    def unpackingText(self, text: str) -> None:
        """Publish Unpacking text."""
        self.unpacking = text
            
    def packingText(self, text: str) -> None:
        """Publish Packing text."""
        self.packing = text

    def lootingText(self, text: str) -> None:
        """Publish Looting text."""
        self.looting = text
    
    def heavinessText(self, text: str) -> None:
        """
        Publish Heaviness text.
        Likely expecting something in the form "{ 1H }" or "{ HH }".
        """
        self.heaviness = text
    
    def initializationText(self, text: str) -> None:
        """
        Publish Initialization text.
        Likely expecting one of the keys of INITIALIZATION_ZONES.
        """
        self.initialization = text
    
    def reshuffleText(self, text: str) -> None:
        """
        Publish Reshuffle text.
        Likely expecting one of the keys of INITIALIZATION_ZONES.
        """ 
        self.reshuffle = text
        
    def roundStartText(self, text: str) -> None:
        """Publish Round Start text."""
        self.roundStart = text

    def addDollarTrigger(self, text: str) -> None:
        """Add a Dollar Trigger to this body text."""
        self.dollarTriggers.append(text)

    def getNiceBodyText(
        self, 
        leftIndent: int, 
        length: int, 
        suppressedTypes: list[str], 
        noColor: bool = False, 
        keepAsArray: bool = False
    ) -> list | str:
        """
        Returns the whole array that represents this body text for UI.
        Should only/mainly be called through the `Card.niceBodyText` call.
        """
        array = []

        ## Suppresses the types we want to suppress
        if (self.unpacking != "" and "u" not in suppressedTypes):
            array.append("| " + self.unpacking)

        prefix = False
        if (self.heaviness != "" and "{}" not in suppressedTypes):
            array.append(self.heaviness)
            prefix = True

        if (self.initialization != "" and self.initialization != "Draw" and "[]" not in suppressedTypes):
            codeLocation = "[ " + REVERSED_INITIALIZATION_ZONES.get(self.initialization) + " ]"
            if (prefix):
                array[len(array) - 1] += ", " + codeLocation
            else:
                prefix = True
                array.append(codeLocation)

        if (self.reshuffle != "" and self.initialization != "Draw" and "<>" not in suppressedTypes):
            codeLocation = "< " + REVERSED_INITIALIZATION_ZONES.get(self.reshuffle) + " >"
            if (prefix):
                array[len(array) - 1] += ", " + codeLocation
            else:
                prefix = True
                array.append(codeLocation)

        if (self.core != "" and (("core" not in suppressedTypes) or (self.packing != "" and "p" not in suppressedTypes))):
            if not(prefix):
                array.append(" " + self.core)
            else:
                array[len(array) - 1] += " " + self.core
        else:
            if len(array) == 0:
                array.append(" DAS ")
            else:
                array[len(array) - 1] += "  DAS "

        # (I can always add a "p2" flag for other ways to suppress types)
        if (self.packing != "" and "p" not in suppressedTypes):
            array.append("|>| " + self.packing)
        elif (self.packing != ""):
            array.append("|>|  ---")

        if (self.looting != "" and "looting" not in suppressedTypes):
            array.append("~ " + self.looting)

        if (self.roundStart != "" and "round start" not in suppressedTypes):
            array.append("@ " + self.roundStart)

        if (len(self.dollarTriggers) > 0 and "dollar triggers" not in suppressedTypes):
            for trigger in self.dollarTriggers:
                array.append("$ " + trigger)

        # converts array into text-based form
        textBodyText = ""
        for i in range(len(array)):
            textBodyText += array[i]
            if (i != len(array) - 1):
                textBodyText += "//"

        if keepAsArray:
            indentArray = h.trueIndent(textBodyText, 0, length - leftIndent, keepAsArray = True)
            returnArray = []
            for line in indentArray:
                if noColor:
                    returnArray.append(line)
                else:
                    returnArray.append(h.colorize(line))
            return returnArray

        indentedBodyText = h.trueIndent(textBodyText, leftIndent, length)
        if noColor:
            colorizedBodyText = indentedBodyText
        else:
            colorizedBodyText = h.colorize(indentedBodyText)
        return colorizedBodyText

class Card():
    """
    Implementation of a Card.

    Attributes:
        ## --- Identification ---
        likelihood (int): likelihood of this card being picked to play (see entity.cardIntellect)
        damageDist (int): how much damage this card deals (see devtools/enemyCardMappings.py)
        siftDist (int): how much sifting this card has.
        name (str): the current name of this card.
        unmodifiedName (str): the original name of this card prior to any modifications.
        uniqueID (int): uuid4 of this card for testing equality.
        
        ## --- Card State ---
        lingering (int): how many turns this card has been in play.
        foreverLinger (bool): if this will never be discarded from play during Tidying.
        turnsLingering (int): how many turns this card has been in play.
            (contrast to `lingering`, which can be sometimes modified by other effects)
        shelled (bool): if the Card is shelled, meaning it cannot be moved from play.

        ## --- Play/Packing/Unpacking Functionality ---
        hasUnpackingAbility (bool): if this has any Unpacking text/ability.
        hasPackingAbility (bool): if this has any Packing text/ability.
        revealed (bool): if this card has been revealed during Packing/Unpacking already.
        throwTextCardFunctions (list[cf.cardFunctions]): ordered list of events when
            this card is played.
        packingTextCardFunctions (list[cf.cardFunctions]): ordered list of events when
            this card is packed.

        ## --- Other Moments Functionality ---
        hasRoundStartAbility (bool): if this has any Round Start text/ability.
        cmfDepot list[cmf.card_mod_function]): list of things that modify card_functions.
        tokens (list[tk.tokens]): list of tokens on this card.
        triggers (list[r.responseAndTrigger]): list of triggers that relate to this card.  
            
        ## --- Card Location Information ---
        intialization (str): intialization location; should be INTIALIZATION_ZONES value.
        reshuffleLocation (str): intialization location; should be INTIALIZATION_ZONES value.
                
        ## --- Looting Information ---
        destructable (bool): if this card is destructable.
        mustDestroyCardWhenLooted (bool): if, when looted, another card must be destroyed.
        mustEnshellCardWhenLooted (bool): if this card Enshells when looted.

        ## --- Card Types ---
        isShellCard (bool): True if a shell card.
        isGainedCard (bool): True if the card is gained to Deck.
        isConfidant (bool): True if a confidant card.

        ## --- Special Stored Values ---
        custom1 (int): stored information about this card.
        bool1 (bool): stored information about this card.
        bool2 (bool): stored information about this card.
    """
    def __init__(self, likelihood: int = 0.5, damageDist: int = 0.5, siftDist: int = 0.5) -> None:
        # Chance the enemy picks that card, tends to scale with power.
        #   So, higher likelihood values means more likely to be picked and not skipped.
        #   A value from 0 to 100 (although, normally at value 0.5).
        self.likelihood = likelihood 

        # A value from 0 to 100 representing to what extent this card does damage. 
        self.damageDist = damageDist
        # Similarly, a value from 0 to 100 representing to what extent this card sifts.
        #   Sifting includes +Actions and +Cards. Imagine it as an inverse to 'stiffness.'
        self.siftDist = siftDist

        # Name and original name of the card
        self.name = ""
        self.unmodifiedName = ""

        # Card Handler Functions, which allow the overriding of cardFunctions functionality
        #   Similar to Tokens, except alter what happens on play
        self.cmfDepot = []

        # Non-negative number of turns a card is staying out. At 0, it is discarded from play. 
        self.lingering = 0
        # If true, no matter the lingering value, this is not discarded from play during Tidying. 
        self.foreverLinger = False
        # Tracks the number of turns a Card has been out; lingering can sometimes change b.c. of other Cards
        self.turnsLingering = 0
        
        # The location the card is initialized. Includes: "Draw", "Into Hand", "Top of Draw", "Bottom of Draw", "Discard", "Muck" 
        #   Check roundStart of the entity file to ensure this is implemented correctly. 
        #   Check colorize in helper file to ensure that we color in the text correctly. 
        self.initialized = "Draw"
        self.reshuffleLocation = "Draw"

        # The check for other phases
        self.hasUnpackingAbility = False
        self.hasPackingAbility = False
        self.hasRoundStartAbility = False
        
        # Checks if the Card has been revealed or not
        self.revealed = False

        # If the Card is shelled, meaning it cannot be moved
        self.shelled = False

        # Parameters for looting
        self.destructable = True
        self.mustDestroyCardWhenLooted = True

        # If the Card is Enshells something when looted
        self.mustEnshellCardWhenLooted = False

        # The type of Card
        self.isShellCard = False
        self.isGainedCard = True
        self.isConfidant = False

        # List of tokens
        self.tokens = []

        # List of triggers 
        self.triggers = []

        # Allows for special stored values
        self.custom1 = 0
        self.bool1 = False
        self.bool2 = False

        # Arrays for cardFunctions
        self.throwTextCardFunctions = []
        self.packingTextCardFunctions = []

        # Creates a copy-resistant identifier of this card using uuid
        self.uniqueID = uuid.uuid4()

    def bundle(
        self,
        throwCardFunction: "cf.cardFunction" = None,
        packingCardFunction: "cf.cardFunction" = None
    ) -> None:
        """Initializes elements of this card after the __init__() call."""
        # Sets the unmodified card name
        self.unmodifiedName = self.name

        # Sets the throw card function
        if throwCardFunction != None:
            self.throwTextCardFunctions.append(throwCardFunction)

        # Sets the packing card function
        if packingCardFunction != None:
            self.packingTextCardFunctions.append(packingCardFunction)

    def niceBodyText(
        self, 
        leftIndent: int, 
        length: int, 
        suppressedTypes: list[str] = [], 
        noColor: bool = False, 
        keepAsArray: bool = False
    ) -> None:
        """
        Displays the body text in a nice-to-read manner.

        Arguments:
            leftIndent: how much whitespace to have to the left of this text.
            length: maximum line length before a line break.
            suppressedTypes: types to omit from display. 
            noColor: if the string values should be colored with colorama.
            keepAsArray: instead of returning a string, returns an array.

        Notes:
            suppressedTypes is very clunky and should be changed in favor of 
                hard-coded omitted values. Look to calls to this method/in this method
                for what possible suppressedTypes are possible.
        """
        ## --- The body text ---
        bodyText = self.bodyText.getNiceBodyText(leftIndent,
                                                 length,
                                                 suppressedTypes,
                                                 noColor = noColor,
                                                 keepAsArray = keepAsArray)

        ## --- Gets preamble/postamble throw text information ---
        bodyTextPreamble = []

        bodyTextPostamble = []
        for token in self.tokens:
            if token.displayWithThrowText:
                text = token.getThrowText()
                if not noColor:
                    text = h.colorize(text)
                bodyTextPostamble.append(text)

        
        ## --- Calculates (as an array or otherwise) ---
        finishedBodyText = None
        if keepAsArray:
            finishedBodyText = []
            for line in bodyTextPreamble + bodyText + bodyTextPostamble:
                finishedBodyText.append(line)
            bodyText = finishedBodyText
        else:
            finishedBodyText = ""
            for line in bodyTextPreamble + [bodyText] + bodyTextPostamble:
                finishedBodyText += line
            bodyText = finishedBodyText

        finishedBodyText = bodyText
        return finishedBodyText

    def nameWithTokens(self) -> str:
        """Gets this card name including its pertinent tokens."""
        text = self.name
        first = True
        for token in self.tokens:
            if token.displayByName:
                if first:
                    text += " <<" + token.name + ">>"
                    first = False
                else:
                    text += ", <<" + token.name + ">>"
        return text


    def isEqual(self, otherCard: "Card") -> bool:
        """Returns True if two cards are equal."""
        return self == otherCard

    def monotonicLingering(self, newLingering: int) -> None:
        """Strictly increases this Card's linering amount."""
        self.lingering = max(newLingering, self.lingering)

    def reduceLingering(self, newLingering: int) -> None:
        """
        Reduces this Card's lingering amount.
        Changes its lingering to the new value, and no longer forever lingers.
        """
        self.foreverLinger = False
        self.lingering = newLingering

    def publishReshuffle(
        self, 
        top: bool = False, 
        intoHand: bool = False, 
        muck: bool = False, 
        discard: bool = False, 
        pocket: bool = False
    ) -> None:
        """Publishes a Reshuffle location; only one True value is expected."""
        location = self.__publishedLocationFetcher(top = top,
                                                   intoHand = intoHand,
                                                   muck = muck,
                                                   discard = discard,
                                                   pocket = pocket)
        self.bodyText.reshuffleText(location)
        self.reshuffleLocation = location

    def publishInitialization(
        self, 
        top: bool = False, 
        intoHand: bool = False, 
        muck: bool = False, 
        discard: bool = False, 
        pocket: bool = False
    ) -> None:
        """Publishes an Intialization location; only one True value is expected."""
        location = self.__publishedLocationFetcher(top = top,
                                                   intoHand = intoHand,
                                                   muck = muck,
                                                   discard = discard,
                                                   pocket = pocket)
        self.bodyText.initializationText(location)
        self.initialized = location

    def __publishedLocationFetcher(
        self, 
        top: bool = False, 
        intoHand: bool = False, 
        muck: bool = False, 
        discard: bool = False, 
        pocket: bool = False
    ) -> None:
        """
        Gets the location name based on which of the parameters == True
        Only one True value is expected.
        """
        trueCount = 0
        location = ""
        if top and "Top" in REVERSED_INITIALIZATION_ZONES:
            trueCount += 1
            location = "Top"
        if intoHand and "Into Hand" in REVERSED_INITIALIZATION_ZONES: 
            trueCount += 1
            location = "Into Hand"
        if muck and "Muck" in REVERSED_INITIALIZATION_ZONES:
            trueCount += 1
            location = "Muck"
        if discard and "Discard" in REVERSED_INITIALIZATION_ZONES:
            trueCount += 1 
            location = "Discard"
        if pocket and "Pocket" in REVERSED_INITIALIZATION_ZONES:
            trueCount += 1
            location = "Pocket"

        if (trueCount != 1):
            input("ERROR! __publishedLocationFetcher has multiple parameters for card: " + self.name)
        return location

    def publishDollarTrigger(self, text: str) -> None:
        """Publishes a Dollar Trigger based on the input `text` value."""
        self.bodyText.addDollarTrigger(text)

    def removeDollarTrigger(
        self, 
        trigger: "r.responseAndTrigger", 
        caster: "e.Entity", 
        dino: "e.Entity", 
        enemies: list["e.Entity"], 
        triggerText: str
    ) -> None:
        """Removes the $ trigger with the matching trigger text; if no match is found, does nothing."""
        for index, currTrigger in enumerate(self.triggers):
            if currTrigger.responseAndTrigger == trigger:
                self.triggers.pop(index)
                if triggerText in self.bodyText.dollarTriggers:
                    self.bodyText.dollarTriggers.remove(triggerText)


    def removeToken(self, token: "tk.token") -> None:
        """Removes the passed in token from this."""
        tk.removeToken(self, token)

    def publishToken(self, token: "tk.token") -> None:
        """Publishes the passed in token from this."""
        tk.publishTokenOnThis(self, token)

    def publishUnpacking(self, text: str) -> None:
        """Publishes the passed in Unpacking text."""
        self.hasUnpackingAbility = True
        self.bodyText.unpackingText(text)

    def publishPacking(self, text: str) -> None:
        """Publishes the passed in Packing text."""
        self.hasPackingAbility = True
        self.bodyText.packingText(text)

    def publishRoundStart(self, text: str) -> None:
        """Publishes the passed in Round Start text."""
        self.hasRoundStartAbility = True
        self.bodyText.roundStartText(text)

    def publishShell(
        self,
        aboveThrowTextWrapper: "cf.shellTextWrapper" = None,
        belowThrowTextWrapper: "cf.shellTextWrapper" = None,
        abovePackingTextWrapper: "cf.shellTextWrapper" = None,
        belowPackingTextWrapper: "cf.shellTextWrapper" = None
    ) -> None:
        """Puts a shell around this Card."""
        # Above Throw Text Resolve
        if (aboveThrowTextWrapper != None):
            if aboveThrowTextWrapper.text != "":
                self.bodyText.prependThrowText(aboveThrowTextWrapper.text, aboveThrowTextWrapper.excludeLineBreak)
            self.throwTextCardFunctions.insert(0, aboveThrowTextWrapper.cardFunction)

        # Below Throw Text Resolve
        if (belowThrowTextWrapper != None):
            if belowThrowTextWrapper.text != "":
                self.bodyText.appendThrowText(belowThrowTextWrapper.text, belowThrowTextWrapper.excludeLineBreak)
            self.throwTextCardFunctions.append(belowThrowTextWrapper.cardFunction)

        # Above Packing Text Resolve
        if (abovePackingTextWrapper != None):
            self.hasPackingAbility = True
            if abovePackingTextWrapper.text != "":
                self.bodyText.prependThrowText(abovePackingTextWrapper.text, abovePackingTextWrapper.excludeLineBreak)
            self.packingTextCardFunctions.insert(0, abovePackingTextWrapper.cardFunction)

        # Below Packing Text Resolve
        if (belowPackingTextWrapper != None):
            self.hasPackingAbility = True
            if belowPackingTextWrapper.text != "":
                self.bodyText.appendThrowText(belowPackingTextWrapper.text, belowPackingTextWrapper.excludeLineBreak)
            self.packingTextCardFunctions.append(belowPackingTextWrapper.cardFunction)

    def purgeThrowText(self, throwTextWrapper: "cf.shellTextWrapper"):
        """Purges the current Throw text, replacing it."""
        self.throwTextCardFunctions = []
        self.bodyText.heavinessText("")
        self.bodyText.mutateThrowText(throwTextWrapper.text)
        self.throwTextCardFunctions.append(throwTextWrapper.cardFunction)

    def purgePackingText(self, throwTextWrapper: "cf.shellTextWrapper"):
        """Purges the current Packing text, replacing it."""
        self.hasPackingAbility = True
        self.packingTextCardFunctions = []
        self.bodyText.mutatePackingText(throwTextWrapper.text)
        self.packingTextCardFunctions.append(throwTextWrapper.cardFunction)

    def onPlay(self, caster: "e.Entity", dino: "e.Entity", enemies: list["e.Entity"], passedInVisuals: "vis.prefabPassedInVisuals"):
        """Plays this Card!"""
        # Boiler plate onPlay functionality.
        caster.minusActions(1)

        # Visualizations
        teamCode = "^"
        if caster.enemy:
            teamCode = "%"
        h.splash(" Resolving: " + teamCode + self.name + teamCode, printInsteadOfInput = True, removePreline = True)
        print(h.normalize("  > ", 4) + self.niceBodyText(4, h.WIDTH, suppressedTypes = ["looting", "round start"]))
        if caster.enemy == False:
            print(" ... ")

        # Does throw text shell function calls
        for cardFunction in self.throwTextCardFunctions:
            cardFunction.func(self, caster, dino, enemies, passedInVisuals)

    def onPacking(self, caster: "e.Entity", dino: "e.Entity", enemies: list["e.Entity"], passedInVisuals: "vis.prefabPassedInVisuals"):
        """Performs the Packing text of a Card!"""
        # Boiler plate onPacking functionality.
        self.revealed = True

        # Visualizations
        teamCode = "^"
        if caster.enemy:
            teamCode = "%"
        h.splash(" Packing up: " + teamCode + self.name + teamCode, printInsteadOfInput = True, removePreline = True)
        print(h.normalize("  > ", 4) + self.niceBodyText(4, h.WIDTH, suppressedTypes = ["looting", "round start"]))
        if caster.enemy == False:
            print(" ... ")

        # Does throw text shell function calls
        for cardFunction in self.packingTextCardFunctions:
            cardFunction.func(self, caster, dino, enemies, passedInVisuals)

    def mutateThis(self, mutationCard: "Card") -> None:
        """
        Changes one Card into another Card via keyword 'mutation.'
        Currently slightly buggy.
        """
        # Changes name
        self.name = mutationCard.name
        self.unmodifiedName = mutationCard.name

        # Changes Heaviness
        self.monotonicLingering(mutationCard.lingering)
        if mutationCard.foreverLinger:
            self.foreverLinger = True

        # Publishes tokens from the other Card
        for token in mutationCard.tokens:
            self.publishToken(token)
        # Adds a 'Mutated' Token
        self.publishToken(tk.mutated())

        # Changes Packing Text
        self.bodyText.mutateThrowText(mutationCard.bodyText.core)
        self.duringPlay = mutationCard.duringPlay

    """
    The following on-blank or at-blank should all be replaced with `r.responseAndTrigger` eventually.
    """
    def onLooted(self, dino): ## Used
        pass

    def onLootedEnshelling(self, dino, cardToEnshell): ## Used
        pass

    def onReplacedWithLoot(self, dino, newCard): ## Used
        pass
    
    def atTriggerTurnStart(self, caster, dino, enemies): ## Used
        pass
    
    def atTriggerRoundStart(self, caster, dino, enemies, passedInVisuals): ## Used
        pass
    
    def atTriggerTurnEnd(self, caster, dino, enemies):
        pass

    def atTriggerEndOfRestStop(self, caster): ## Caster is basically only 'Dino'; Used
        pass

    def resetCardState_TurnEnd(self):
        """Resets the state of this Card at the very end of Turn End."""
        # We need to reset every trigger
        for trigger in self.triggers:
            trigger.responseAndTrigger.resetState_TurnEnd()

    def resetCardState_AfterAnyCardResolves(self):
        """Resets the state of this Card after a card resolves."""
        # We need to reset every trigger
        for trigger in self.triggers:
            trigger.responseAndTrigger.resetState_AfterAnyCardResolves()

    def resetCardState_AfterAfterEntityAttacked(self):
        """Resets the state of this Card after an entity is attacked."""
        # We need to reset every trigger
        for trigger in self.triggers:
            trigger.responseAndTrigger.resetState_AfterAfterEntityAttacked()

    """
    Not currently used, and should be changed to be more like how Throw Text and Packing Text works.
    def onUnpacking(self, caster, dino, enemies):
        self.revealed = True
    """