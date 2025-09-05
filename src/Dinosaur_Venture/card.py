import math, random, os
from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import cardTokens as tk, helper as h, gameplayLogging as log

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
    ## Creates the core bodyText
    def __init__(self, text):
        self.unpacking = ""
        self.packing = ""
        self.looting = ""
        self.heaviness = ""
        self.initialization = ""
        self.reshuffle = ""
        self.roundStart = ""
        self.dollarTriggers = []
        self.core = text

    ## Allows mutation to the end of the bodyText.
    def appendThrowText(self, text, excludeLineBreak = False):
        separator = " //"
        if excludeLineBreak:
            separator = " "
        self.core += separator + text

    def prependThrowText(self, text, excludeLineBreak = False):
        separator = " //"
        if excludeLineBreak:
            separator = " "
        self.core = text + separator + self.core

    ## Changes the ENTIRE Throw text. Do not use for initialization; use __init__ instead
    def mutateThrowText(self, text):
        self.core = text ## + " //"

    ## Changes the ENTIRE Packing text.
    def mutatePackingText(self, text):
        self.packing = text

    ## Changes the ENTIRE Round Start text.
    def mutateRoundStartText(self, text):
        self.roundStart = text

    ## Allows adding more to the bodyText
    ##  STILL FUNCTIONAL BUT DO NOT USE
    def push(self, textType, text):
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
    
    def unpackingText(self, text):
        self.unpacking = text
            
    def packingText(self, text):
        self.packing = text

    def lootingText(self, text):
        self.looting = text
    
    def heavinessText(self, text):
        self.heaviness = text
    
    def initializationText(self, text):
        self.initialization = text
    
    def reshuffleText(self, text): 
        self.reshuffle = text
        
    def roundStartText(self, text):
        self.roundStart = text

    def addDollarTrigger(self, text):
        self.dollarTriggers.append(text)

    ## Returns the whole array for printing
    ##  keepAsArray does not do the coloring
    def getNiceBodyText(self, leftIndent, length, suppressedTypes, noColor = False, keepAsArray = False):
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

        ## (I can always add a "p2" flag for other ways to suppress types)
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

        ## converts array into text-based form
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
    def __init__(self, likelihood = 0.5, damageDist = 0.5, siftDist = 0.5, alure = 1):
        ## Chance the enemy picks that card, tends to scale with power.
        ##  So, higher likelihood values means more likely to be picked and not skipped.
        ##  A value from 0 to 100 (although, normally at value 0.5).
        self.likelihood = likelihood 

        ## A value from 0 to 100 representing to what extent this card does damage. 
        self.damageDist = damageDist
        ## Similarly, a value from 0 to 100 representing to what extent this card sifts.
        ##  Sifting includes +Actions and +Cards. Imagine it as an inverse to 'stiffness.'
        self.siftDist = siftDist
        self.alure = alure

        ## Name and original name of the card
        self.name = ""
        self.unmodifiedName = ""

        ## Card Handler Functions, which allow the overriding of cardFunctions functionality
        ## Similar to Tokens, except alter what happens on play
        self.cmfDepot = []

        ## Non-negative number of turns a card is staying out. At 0, it is discarded from play. 
        self.lingering = 0
        ## If true, no matter the lingering value, this is not discarded from play during Tidying. 
        self.foreverLinger = False
        ## Tracks the number of turns a Card has been out; lingering can sometimes change b.c. of other Cards
        self.turnsLingering = 0
        
        ## The location the card is initialized. Includes: "Draw", "Into Hand", "Top of Draw", "Bottom of Draw", "Discard", "Muck" 
        ##  Check roundStart of the entity file to ensure this is implemented correctly. 
        ##  Check colorize in helper file to ensure that we color in the text correctly. 
        self.initialized = "Draw"
        self.reshuffleLocation = "Draw"

        ## The check for other phases
        self.hasUnpackingAbility = False
        self.hasPackingAbility = False
        self.hasRoundStartAbility = False
        
        ## Checks if the card is currently in its 'on play' state, meaning that triggers read off of its Throw Text are currently valid 
        self.existingOnPlay = False

        ## Checks if the Card has been revealed or not
        self.revealed = False

        ## If the Card is shelled, meaning it cannot be moved
        self.shelled = False

        ## Parameters for looting
        self.destructable = True
        self.mustDestroyCardWhenLooted = True

        ## If the Card is Enshells something when looted
        self.mustEnshellCardWhenLooted = False

        ## The type of Card
        self.isShellCard = False
        self.isGainedCard = True
        self.isConfidant = False

        ## List of tokens
        self.tokens = []

        ## List of triggers 
        self.triggers = []

        ## Allows for special stored values
        self.custom1 = 0
        self.reacted_1 = False
        self.bool1 = False
        self.bool2 = False

        ## Arrays for cardFunctions
        self.throwTextCardFunctions = []
        self.packingTextCardFunctions = []

    def bundle(self, throwCardFunction = None, packingCardFunction = None):
        ## Sets the unmodified card name
        self.unmodifiedName = self.name

        ## Sets the throw card function
        if throwCardFunction != None:
            self.throwTextCardFunctions.append(throwCardFunction)

        ## Sets the packing card function
        if packingCardFunction != None:
            self.packingTextCardFunctions.append(packingCardFunction)

    ## Displays the body text in a nice-to-read manner
    def niceBodyText(self, leftIndent, length, supressedTypes = [], noColor = False, keepAsArray = False):
        ## --- The body text ---
        bodyText = self.bodyText.getNiceBodyText(leftIndent,
                                                 length,
                                                 supressedTypes,
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

    def nameWithTokens(self):
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


    ## For all variables of a card, checks if they match. If they match, returns true, otherwise false. 
    def isEqual(self, otherCard):
        return self == otherCard
        ## return self.name == otherCard.name and self.bodyText == otherCard.bodyText and self.table == otherCard.table and self.likelihood == otherCard.likelihood and self.damageDist == otherCard.damageDist and self.siftDist == otherCard.siftDist and self.alure == otherCard.alure and self.lingering == otherCard.lingering

    def publishReshuffle(self, top = False, intoHand = False, muck = False, discard = False, pocket = False):
        location = self.__publishedLocationFetcher(top = top,
                                                   intoHand = intoHand,
                                                   muck = muck,
                                                   discard = discard,
                                                   pocket = pocket)
        self.bodyText.reshuffleText(location)
        self.reshuffleLocation = location

    ## Helper method that takes care of all of what must be done when changing initialization
    def publishInitialization(self, top = False, intoHand = False, muck = False, discard = False, pocket = False):
        location = self.__publishedLocationFetcher(top = top,
                                                   intoHand = intoHand,
                                                   muck = muck,
                                                   discard = discard,
                                                   pocket = pocket)
        self.bodyText.initializationText(location)
        self.initialized = location

    ## Gets the location as a name
    def __publishedLocationFetcher(self, top = False, intoHand = False, muck = False, discard = False, pocket = False):
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
            input("BUG! ...")
            input("BUG! trueCount equals " + str(trueCount) + " for card: " + self.name)
            print(0/0)
        return location

    def publishDollarTrigger(self, text):
        self.bodyText.addDollarTrigger(text)

    def removeDollarTrigger(self, trigger, caster, dino, enemies, triggerText):
        for index, currTrigger in enumerate(self.triggers):
            if currTrigger.responseAndTrigger == trigger:
                self.triggers.pop(index)
                if triggerText in self.bodyText.dollarTriggers:
                    self.bodyText.dollarTriggers.remove(triggerText)


    def removeToken(self, token):
        tk.removeToken(self, token)

    def publishToken(self, token):
        tk.publishTokenOnThis(self, token)

    def publishUnpacking(self, text):
        self.hasUnpackingAbility = True
        self.bodyText.unpackingText(text)

    def publishPacking(self, text):
        self.hasPackingAbility = True
        self.bodyText.packingText(text)

    def publishRoundStart(self, text):
        self.hasRoundStartAbility = True
        self.bodyText.roundStartText(text)

    ## Puts a shell around this Card. Each parameter is expected to be a shellTextWrapper
    def publishShell(self, aboveThrowTextWrapper = None,
                           belowThrowTextWrapper = None,
                           abovePackingTextWrapper = None,
                           belowPackingTextWrapper = None):

        ## Above Throw Text Resolve
        if (aboveThrowTextWrapper != None):
            if aboveThrowTextWrapper.text != "":
                self.bodyText.prependThrowText(aboveThrowTextWrapper.text, aboveThrowTextWrapper.excludeLineBreak)
            self.throwTextCardFunctions.insert(0, aboveThrowTextWrapper.cardFunction)

        ## Below Throw Text Resolve
        if (belowThrowTextWrapper != None):
            if belowThrowTextWrapper.text != "":
                self.bodyText.appendThrowText(belowThrowTextWrapper.text, belowThrowTextWrapper.excludeLineBreak)
            self.throwTextCardFunctions.append(belowThrowTextWrapper.cardFunction)

        ## Above Packing Text Resolve
        if (abovePackingTextWrapper != None):
            self.hasPackingAbility = True
            if abovePackingTextWrapper.text != "":
                self.bodyText.prependThrowText(abovePackingTextWrapper.text, abovePackingTextWrapper.excludeLineBreak)
            self.packingTextCardFunctions.insert(0, abovePackingTextWrapper.cardFunction)

        ## Below Packing Text Resolve
        if (belowPackingTextWrapper != None):
            self.hasPackingAbility = True
            if belowPackingTextWrapper.text != "":
                self.bodyText.appendThrowText(belowPackingTextWrapper.text, belowPackingTextWrapper.excludeLineBreak)
            self.packingTextCardFunctions.append(belowPackingTextWrapper.cardFunction)

    ## Purges the current Throw text, replacing it with something
    def purgeThrowText(self, throwTextWrapper):
        self.throwTextCardFunctions = []
        self.bodyText.heavinessText("")
        self.bodyText.mutateThrowText(throwTextWrapper.text)
        self.throwTextCardFunctions.append(throwTextWrapper.cardFunction)

    ## Purges the current Packing text, replacing it with something
    def purgePackingText(self, throwTextWrapper):
        self.hasPackingAbility = True
        self.packingTextCardFunctions = []
        self.bodyText.mutatePackingText(throwTextWrapper.text)
        self.packingTextCardFunctions.append(throwTextWrapper.cardFunction)

    ## Plays the Card!
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        ## Boiler plate onPlay functionality.
        caster.minusActions(1)
        self.existingOnPlay = True

        ## Visualizations
        teamCode = "^"
        if caster.enemy:
            teamCode = "%"
        h.splash(" Resolving: " + teamCode + self.name + teamCode, printInsteadOfInput = True, removePreline = True)
        print(h.normalize("  > ", 4) + self.niceBodyText(4, h.WIDTH, supressedTypes = ["looting", "round start"]))
        if caster.enemy == False:
            print(" ... ")

        ## Does throw text shell function calls.
        for cardFunction in self.throwTextCardFunctions:
            cardFunction.func(self, caster, dino, enemies, passedInVisuals)

    ## Performs the packing text of a Card!
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        ## Boiler plate onPacking functionality.
        self.revealed = True

        ## Visualizations
        teamCode = "^"
        if caster.enemy:
            teamCode = "%"
        h.splash(" Packing up: " + teamCode + self.name + teamCode, printInsteadOfInput = True, removePreline = True)
        print(h.normalize("  > ", 4) + self.niceBodyText(4, h.WIDTH, supressedTypes = ["looting", "round start"]))
        if caster.enemy == False:
            print(" ... ")

        ## Does throw text shell function calls.
        for cardFunction in self.packingTextCardFunctions:
            cardFunction.func(self, caster, dino, enemies, passedInVisuals)

    ## After doing the onPlay, resolves the duringPlay text.
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        pass

    def onDestroy(self):
        pass

    ## Changes one Card into another Card
    def mutateThis(self, mutationCard):
        ## Changes name
        self.name = mutationCard.name
        self.unmodifiedName = mutationCard.name

        ## Changes Heaviness
        self.monotonicLingering(mutationCard.lingering)
        if mutationCard.foreverLinger:
            self.foreverLinger = True

        ## Publishes tokens from the other Card
        for token in mutationCard.tokens:
            self.publishToken(token)
        ## --> Adds a 'Mutated' Token
        self.publishToken(tk.mutated())

        ## Changes Packing Text
        self.bodyText.mutateThrowText(mutationCard.bodyText.core)
        self.duringPlay = mutationCard.duringPlay

    def endOfMyTurnCondition(self, caster, dino, enemies):
        pass

    def endOfDinoTurnTriggered(self, caster, dino, enemies):
        pass

    ## -----------------------

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

    ## Only use this to reset the state of the Card
    def resetCardState_TurnEnd(self):
        ## We need to reset every trigger
        for trigger in self.triggers:
            trigger.responseAndTrigger.resetState_TurnEnd()

    def resetCardState_AfterAnyCardResolves(self):
        ## We need to reset every trigger
        for trigger in self.triggers:
            trigger.responseAndTrigger.resetState_AfterAnyCardResolves()

    def resetCardState_AfterAfterEntityAttacked(self):
        ## We need to reset every trigger
        for trigger in self.triggers:
            trigger.responseAndTrigger.resetState_AfterAfterEntityAttacked()

    def atTriggerEndOfRestStop(self, caster): ## Caster is basically only 'Dino'; Used
        pass

    def onUnpacking(self, caster, dino, enemies):
        self.revealed = True
    
    # def onPacking(self, caster, dino, enemies, passedInVisuals):
    #     self.revealed = True

    def monotonicLingering(self, newLingering):
        self.lingering = max(newLingering, self.lingering)

    def reduceLingering(self, newLingering):
        self.foreverLinger = False
        self.lingering = newLingering