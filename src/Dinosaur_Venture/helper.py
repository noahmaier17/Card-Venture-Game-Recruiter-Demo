import copy
import math
import os
import random
from typing import TYPE_CHECKING

from colorama import Back, Fore, Style, init

init(autoreset=True)
from Dinosaur_Venture.cards.mechanics import card_tokens as tk
from Dinosaur_Venture.cards.mechanics.card_initalization_zones import \
    INITIALIZATION_ZONES
from Dinosaur_Venture.cards.mechanics.card_location import CardLocation
from Dinosaur_Venture.logging import gameplay_logging as log
from Dinosaur_Venture.logging import log_entry

if TYPE_CHECKING:
    from Dinosaur_Venture import clearing as clr
    from Dinosaur_Venture import gameplay_scripted_input as scriptInput
    from Dinosaur_Venture import main_visuals as vis
    from Dinosaur_Venture.cards.mechanics import card as c
    from Dinosaur_Venture.entities import entity as e

WIDTH = 117 - 2

## Types of punctuation we splinterize, and that we do not want a new indent line to begin with
PUNCTUATION_TYPES = [' ', ',', '!', '.', '-', ':', ';', '?', '{', '}', '[', ']', '(', ')', '*', '`']
MULTIPLICATIVE_NUMERAL_TYPES = ["Nonce", "Once", "Twice", "Thrice", "Quarce", "Quince", "Sextce", "Spece", "Octce", "Nince", "Tence"]
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def selectCardFromHandAndPocket(
    choiceSet: list[int], 
    selectionText: str, 
    dino: "e.Entity", 
    enemies: list["e.Entity"], 
    roundCount: int, 
    clearing: "clr.Clearing", 
    event: str, 
    entityNames: dict, 
    cardNames: dict, 
    extraSuppressedTypes: list[str] = [],
    canPass: bool = False, 
    scriptedInput: "scriptInput.gameplayScriptInput" = None
) -> str | int:
    """
    Overhead for picking a card to play/reveal/etc from Hand/Pocket. 
    
    If passing, returns "pass". Otherwise returns the picked value."""
    from Dinosaur_Venture import main_visuals as vis

    while True:
        if scriptedInput: # Handles scripted input
            print(selectionText) # We still want to ensure the inputText string is valid, even though it is not useful to print it
            pick = scriptedInput.getNextValue()
        else: # Otherwise, we will pick via user input as normal
            pick = input(selectionText)

        try:
            # Is this pick an integer within our possible set of values?
            pick = int(pick)
            if pick not in choiceSet:
                print(vis.eventText(event) + "INVALID INPUT ")
            else:
                return pick

        except ValueError:
            # Are we trying to pass?
            if pick.lower() == "pass" and canPass:
                return "pass"
            
            # Did we input an entity name?
            elif pick.lower().strip() in entityNames.keys() and pick != "":
                splash(entityNames[pick.lower().strip()], printInsteadOfInput = True)

            # Did we input a card name?
            elif pick.lower().strip() in cardNames.keys() and pick != "":
                key = pick.lower().strip()
                print("    " + Back.CYAN + Style.BRIGHT + " " + cardNames[key].name + " ")
                print(normalize("", 3) + cardNames[key].prettyCardText(3, WIDTH, suppressedTypes = []))

            # Did we input "clear"?
            elif pick.lower() == "clear":
                vis.printDinoTurn(dino, enemies, roundCount, clearing, event, extraSuppressedTypes=extraSuppressedTypes)

            # If none of those are the case, we have invalid input
            else:
                print(vis.eventText(event) + "INVALID INPUT ")

def selectCard(
    dino: "e.Entity", 
    clearingName: "clr.Clearing", 
    roundCount: int, 
    lootTables: list[CardLocation], 
    pullsTable: list[int],
    lootVacuously: bool = False, 
    canPass: bool = False, 
    activateAbilityOnPass: bool = False
) -> None:
    """Drafts a Card from a loot table."""
    from Dinosaur_Venture.main_visuals import printLocation

    ## Currently not used; if we want to loot without seeing all card text
    suppressedTypes = []

    for table in lootTables:
        table.shuffle()

    ## Are we even going to loot?
    if (lootVacuously == False and dino.looting <= 0):
        return

    ## Visuals
    lootingInstances = dino.looting
    if lootVacuously:
        lootingInstances = 1

    clear_screen()
    splash("[Round: " + str(roundCount) + "] [Looting: '" + clearingName + "'] [Number of times to Loot: " + MULTIPLICATIVE_NUMERAL_TYPES[lootingInstances] + "]", printInsteadOfInput = True)
    middleText = "[ All Destructable Cards in Deck ]"
    print(normalize("-X-", (WIDTH + 2 - len(middleText) - 3) // 2 + 1, separator = "-") + middleText + normalize("", (WIDTH + 2 - len(middleText)) // 2 + 1, separator = "-"))

    ## Gets the cards in deck that can be replaced
    i = 0
    picksTable = []
    confidantPicksTable = []
    incrementTable = []
    confidantIncrementsTable = []
    count = 0
    confidantCount = 0
    nonDestructableDeckTable = []
    for card in dino.deck.getArray():
        if (card.destructable == True):
            '''
            print(" " + str(count + 1) + ". " 
                + Back.CYAN + Style.BRIGHT + " " + dino.deck.at(i).name + " "
                + Back.RESET + Style.NORMAL 
                + normalize("", 41 - 5 - len(str(count + 1)) - len(dino.deck.at(i).name) - 3) + ":  "
                + dino.deck.at(i).prettyCardText(41, WIDTH, suppressedTypes = []))
            # '''
            count += 1
            picksTable.append(count)
            incrementTable.append(0)
            nonDestructableDeckTable.append(card)

            if not tk.checkTokensOnThis(card, [tk.confidant()]):
                confidantCount += 1
                confidantPicksTable.append(confidantCount)
                confidantIncrementsTable.append(0)
            else:
                confidantIncrementsTable.append(1)
        else:
            incrementTable.append(1)
        i += 1

    printLocation(nonDestructableDeckTable, 0, Back.CYAN, [], "None", removeBetweenLineSpaces = True)
    splash("", printInsteadOfInput = True)
    print(normalize(" | ", WIDTH + 2, separator = "` "))

    ## Picks Cards from the lootTable
    pulledFromLootTable = CardLocation("pulled loot table")
    for index in range(len(pullsTable)):
        pulls = pullsTable[index]
        table = lootTables[index]
        while pulls > 0:
            pulls -= 1
            if table.length() > 0:
                pulledFromLootTable.append(table.pop())
            else:
                pass

    ## We will only draft if we have a non-zero number of picks.
    if (pulledFromLootTable.length() == 0):
        splash(" There is no available Loot! ")
        return
    else:
        ## Drafts!
        holdingSpot = CardLocation("Card to Pick")

        ## print(" -- Drafting to <<" + holdingSpot.niceName() + ">> --")
        if pulledFromLootTable.length() == 0 or (pulledFromLootTable.length() == 0):
            print(pulledFromLootTable.length())
            input(" Attempted to draft cards, but Pulls: " + str(pulledFromLootTable.length()) + " and pulledFromLootTable: " + str(pulledFromLootTable))
            return
        
        draftPoolCopy = CardLocation("")
        for card in pulledFromLootTable.getArray():
            draftPoolCopy.append(copy.deepcopy(card))

        picks = CardLocation("")
        for i in range(pulledFromLootTable.length()):
            if draftPoolCopy.length() > 0:
                picks.append(draftPoolCopy.pop(random.randint(0, draftPoolCopy.length() -1)))
                '''
                print(" " + str(i + 1) + ". " 
                        + Back.CYAN + Style.BRIGHT + " " + picks.at(i).name + " "
                        + Back.RESET + Style.NORMAL 
                        + normalize("", 41 - 5 - len(str(i+1)) - len(picks.at(i).name) - 3) + ":  "
                        + picks.at(i).prettyCardText(41, WIDTH, suppressedTypes))
                print(normalize("", 41 - 3) + ".")
                '''
        printLocation(picks.getArray(), 0, Back.WHITE, [], "None", nameFore = Fore.BLACK)
        splash("", printInsteadOfInput = True)
        print(normalize(" | ", WIDTH + 2, separator = "` "))


        ## Shows our pass ability if applicable
        if activateAbilityOnPass:
            splash(dino.passedLootingInfoText, printInsteadOfInput = True)

        ## Picks the Card
        index = pickValue("Pick a Card", range(1, picks.length() + 1), canPass = canPass) - 1

        if lootVacuously == False:
            dino.looting -= 1

        ## If we did not pass
        if index != -2:
            draftedCard = picks.pop(index)
            holdingSpot.append(draftedCard)

            '''
                Above this, drafts the Card.
                Below this, resolves the Card that was drafted.
            '''

            ## If the Card destroys another Card when looted.
            ##  The case with practically all Dino Cards.
            if draftedCard.isGainedCard:
                ## Adds the drafted Card to dino deck
                draftedCard.onLooted(dino)
                dino.deck.append(draftedCard)

                ## splash("Hopefully the ^" + draftedCard.name + "^ makes for a more admirable keepsake than ^" + pickedCard.name + "^...")
                splash("Hopefully the ^" + draftedCard.name + "^ makes for an admirable keepsake...")

            ## Otherwise, if the Card should be shell-modifying another Card.
            ##  The case with practically all Dino Shell Cards.
            elif draftedCard.isShellCard and draftedCard.mustEnshellCardWhenLooted:
                ## If a confidant, we cannot pick a card already with a <<confidant>>
                if draftedCard.isConfidant:
                    picksTable = confidantPicksTable
                    incrementTable = confidantIncrementsTable

                pickedValue = pickValue("Pick a Card to Change", picksTable) - 1

                offset = 0
                priorOffset = -1
                while offset != priorOffset:
                    priorOffset = offset
                    offset = sum(incrementTable[0:picksTable[pickedValue] + offset])

                ## Resolves the Enshelling
                pickedCard = dino.deck.at(pickedValue + offset)
                formerName = pickedCard.name
                draftedCard.onLootedEnshelling(dino, pickedCard)

                splash("Hopefully the ^" + pickedCard.name + "^ fares better than ^" + formerName + "^...")

            ## This Card is neither gained nor shells (EG a rune)
            else:
                ## Resolves onLooted
                draftedCard.onLooted(dino)

                splash("Hopefully the ^" + draftedCard.name + "^ did not lead you astray...")
        ## If we did pass, and we are able to trigger something special because of it
        elif activateAbilityOnPass:
            dino.passedLooting(clearingName, roundCount, lootTables, pullsTable, picksTable, incrementTable)

    ## Do we need to loot another time?
    ## If we are looting vacuously, we loot once
    if lootVacuously or dino.looting <= 0:
        return
    else:
        selectCard(dino, clearingName, roundCount, lootTables, pulls = pulls, lootVacuously = lootVacuously)

def locateCardIndex(array: CardLocation, card: "c.Card"):
    """
    Checks for if a given card is found within an array of cards. 
    
    Returns the index of that array if found, otherwise returning -1.
    """
    i = 0
    for crosscheckCard in array.getArray():
        if card.__eq__(crosscheckCard):
            return i
        i += 1
    return -1

def pickLivingEnemy(
    text: str, 
    enemies: list["e.Enemies"], 
    preamble: list[str] = [], 
    passedInVisuals: "vis.prefabPassedInVisuals" = "null",
    scriptedInput: "scriptInput.gameplayScriptInput" = None
) -> int:
    """Allows the user to pick a living enemy. If there is no possible target, returns -1."""
    # Logging
    log.write_to_log(log_entry.HelperLogEntry.PickLivingEnemy(text, enemies, preamble, passedInVisuals))

    excludingValues = []
    allDead = True
    for i in range(len(enemies)):
        if enemies[i].dead == True:
            excludingValues.append(i + 1)
        else:
            allDead = False
    
    if allDead == True:
        return -1
    
    return pickValue(text, range(1, len(enemies) + 1), 
                     preamble=preamble,
                     passedInVisuals=passedInVisuals,
                     excludingValues=excludingValues,
                     scriptedInput=scriptedInput) - 1
 
def getFrontLivingEnemyIndex(enemies: list["e.Entity"]) -> int:
    """Gets index of the front-est living Enemy. Returns -1 if no enemy matches that criteria."""
    for i in range(len(enemies)):
        if enemies[i].dead == False:
            return i
    return -1

def getNextLivingEnemyIndex(enemies: list["e.Entity"], relativeIndex: int) -> int:
    """
    Gets index of the next living Enemy, given a position in the enemies list to start from. 
    Loops around the end of the list like a circular array.
    
    Returns -1 if no enemy matches that criteria.
    """
    for i in range(relativeIndex + 1, len(enemies)):
        if enemies[i].dead == False:
            return i
    for i in range(0, relativeIndex + 1):
        if enemies[i].dead == False:
            return i
    return -1

def deadCount(enemies: list["e.Entity"]) -> int:
    """Returns a count of the number of dead enemies.."""
    deadCount = 0
    for enemy in enemies:
        if enemy.dead == True:
            deadCount += 1
    return deadCount

def pickNonNegativeNumber(
    text: str, 
    preamble: list[str] = [], 
    passedInVisuals: "vis.prefabPassedInVisuals" = "null",
    canPass: bool = False
) -> int:
    """Pick a number, unbounded* (capped at 99)."""
    ## OBSERVE: Copy and pasted code from pickValue into here

    pick = 0
    passText = ""

    if passedInVisuals != "null":
        if canPass:
            passText += "(Pass), "
        text = " > (Clear), " + passText + "[Input Noun], or " + text + ": "
    else:
        if canPass:
            passText += "(Pass) or "
        text = " > " + passText + text + ": "

    for row in preamble:
        splash(row, printInsteadOfInput = True)

    while True:
        pick = input(colorize(text))
        try:
            pick = int(pick.strip())
            if pick >= 0:
                if pick >= 99:
                    splash("FAILURE Number rounded down to 2 digits for being excessively large.", printInsteadOfInput = True)
                return min(pick, 99)
            else:
                splash(" INVALID INPUT ")

        except ValueError:
            pick = pick.lower().strip()
            if pick ==  "clear" and passedInVisuals != "null":
                passedInVisuals.display()
                print(" ~ Cleared ~ ")
                for row in preamble:
                    splash(row, printInsteadOfInput = True)

            elif pick == "pass" and canPass:
                return -1

            elif passedInVisuals == "null" or not printCheckProperNouns(pick, passedInVisuals.entityNames, passedInVisuals.cardNames):
                print(" INVALID INPUT ")

def fetchCardFromLocation(text: str, location: "CardLocation"):
    """Returns a card picked from a location."""
    preamble = []
    index = 1
    for card in location.getArray():
        preamble.append(str(index) + ": ^" + card.name + "^.")
        index += 1

    pick = pickValue(text, range(1, index), preamble = preamble) - 1
    return location.at(pick)

def pickValue(
    text: str,
    setOfValues: list[int],
    excludingValues: list[int] = [], 
    preamble: list[str] = [],
    passedInVisuals: "vis.prefabPassedInVisuals" = "null", 
    canPass: bool = False, 
    intType: bool = True,
    scriptedInput: "scriptInput.gameplayScriptInput" = None):
    """
    With a text prompt and set of values, waits for user input until the input value is within the set of values.

    If the user inputs "pass" while canPass == True, returns -1. Otherwise, returns the index picked.

    Key Arguments:
        excludingValues (list[int]): values within the set of values which are not valid. 

    Use Cases:
        For picking a value from an array: 'range(1, len(LIST) + 1)'
        For picking a Card index: 'pickValue("TEXT", range(1, len(LIST) + 1)) - 1'
    """
    ## OBSERVE: Copy and pasted code from here into pickNonNegativeNumber

    ## Prepares UI for pickValue
    passText = ""
    if passedInVisuals != "null":
        if canPass:
            passText += "(Pass), "
        text = " > (Clear), " + passText + "[Input Noun], or " + text + ": "
    else:
        if canPass:
            passText += "(Pass) or "
        text = " > " + passText + text + ": "

    ## Prints preamble
    for row in preamble:
        splash(row, printInsteadOfInput = True)

    ## Continuously asks for a value
    while True:
        ## If we have scriptedInput, uses that instead
        if scriptedInput != None:
            pick = scriptedInput.getNextValue()
        else:
            pick = input(colorize(text))

        try:
            if intType:
                pick = int(pick.strip())
            else:
                pick = float(pick.strip())
            if not(pick in setOfValues) or (pick in excludingValues):
                print(" INVALID PICK ")
            else:
                return pick
        except ValueError:
            pick = pick.lower().strip()
            if pick ==  "clear" and passedInVisuals != "null":
                passedInVisuals.display()
                print(" ~ Cleared ~ ")
                for row in preamble:
                    splash(row, printInsteadOfInput = True)

            elif pick == "pass" and canPass:
                return -1

            elif passedInVisuals == "null" or not printCheckProperNouns(pick, passedInVisuals.entityNames, passedInVisuals.cardNames):
                print(" INVALID INPUT ")

def pickLetter(text: str, setOfLetters: list[str], excludingValues: list[str] = []) -> str:
    """
    With some text prompt and set of letters, lets the user pick one such letter, returning it.
    Case-insensitive; returns the lowercase version of the letter.  
    """
    lowercaseSetOfLetters = []
    for letter in setOfLetters:
        lowercaseSetOfLetters.append(letter.lower())
    
    lowercaseExcludingValues = []
    for letter in excludingValues:
        lowercaseExcludingValues.append(letter.lower())
    
    pick = ''
    while True:
        pick = input(text + ": ").lower()
        if not(pick in lowercaseSetOfLetters) or (pick in lowercaseExcludingValues):
            print(" INVALID PICK ")
        else:
            return pick.lower()

def normalize(text: str, spaces: int, separator: str = " ", cutFat: bool = False) -> str:
    """
    Sets a certain amount of 'separator' (meaning often white) space after a name. 
    If the input length is too long, ends it with ".."
    """
    text = str(text)
    if spaces <= len(text) and len(text) < spaces + len(separator):
        if cutFat:
            text = text[0:spaces]
        
        return text
    elif len(text) > spaces:
        return text[0:max(spaces - 2, 0)] + ".."
    else:
        return normalize(text + separator, spaces, separator = separator, cutFat = cutFat)

def trueIndent(text: str, leftIndent: int, length: int, nextLineText: str = " ", keepAsArray: bool = False) -> str | list[str]:
    """
    Indents each line of some given text. Does not contain trailing line breaks, nor include any lines that would be purely blank. 

    Arguments:
        text (str): the text we are giving an indent.
        leftIndent (int): how many blank spaces to indent by.
        length (int): how long until we wrap around and begin a new line.
        nextLineText (str): after the leftIndent-number of white spaces, what to print before printing the text. 
        keepAsArray (bool): if True, returns an list[str]; otherwise returns a str using \n for line breaks.
    """
    ## Goes through all words, adding them to an array 
    splinterizedText = splinterize(text)
    newTextArray = [""]

    ## On lines after the first, our indent is also padded by the size of the nextLineText
    nextLineTextBuffer = 0
    for i in range(len(splinterizedText)):
        ## Sets nextLineTextBuffer to the length of the nextLineText if we have more than 1 line 
        if nextLineTextBuffer == 0 and len(newTextArray) > 1:
            nextLineTextBuffer = len(nextLineText)

        ## Adds the word
        word = splinterizedText[i]
        if len(word) >= 2 and word[0:2] == "//":    ## Specially input 'next line' case
            newTextArray.append(word[2:len(word)])
        elif len(newTextArray[len(newTextArray) - 1] + word) > length - leftIndent - nextLineTextBuffer and word not in PUNCTUATION_TYPES:               ## If out of space (and not adding who-cares punctuation-related items), makes new line
            newTextArray.append(word)
        else:
            newTextArray[len(newTextArray) - 1] += word

    ## Adds to all lines except the first the indent
    for i in range(len(newTextArray)):
        if i != 0:
            newTextArray[i] = normalize("", leftIndent) + nextLineText + newTextArray[i]

    worthlessLine = normalize("", leftIndent) + nextLineText
    ## skippedFirstIndent = False

    ## Adds all words from the array implementation that are not wordless
    returnTextArray = []
    for element in newTextArray:
        if element != worthlessLine and element != worthlessLine + " ":
            ## if not skippedFirstIndent:
            ##     skippedFirstIndent = True
            ##     returnText += element
            ## else:
            ##     returnText += "\n" + element
            returnTextArray.append(element)

    ## Returns as array if that is what is requested, otherwise turns it into a massive string
    if keepAsArray:
        return returnTextArray
    else:
        returnText = ""
        for index in range(len(returnTextArray)):
            if index != len(returnTextArray) - 1:
                returnText += returnTextArray[index] + "\n"
            else:
                returnText += returnTextArray[index]
        return returnText

    '''
    ## Adds all words from the array implementation UNLESS they are a text-less indent
    returnText = ""
    for element in newTextArray:
        if element != worthlessLine and element != worthlessLine + " ":
            if skippedFirstIndent == False:
                skippedFirstIndent = True
                returnText += element
            else:
                returnText += "\n" + element
    return returnText
    '''

def roundThird(number: int) -> int:
    """Truncates numbers to nearest third."""
    floor = math.floor(number)
    if number - floor > 0.9:
        floor += 1
    numberMod = round(number * 3)
    
    if numberMod % 3 == 0:
        return floor
    if numberMod % 3 == 1:
        return floor + 0.3
    if numberMod % 3 == 2:
        return floor + 0.6

def clear_screen() -> None:
    """Clears the terminal; works with Windows, Linux, and MacOS."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def colorize(text: str) -> str:
    """Adds colors to certain key words/phrases in a string, returning that newly-colorized string."""
    returnText = ""
    splinterizedText = splinterize(text)

    for word in splinterizedText:
        # print(word)
        if word == "DAS":
            returnText += Style.BRIGHT + "---" + Style.NORMAL
        elif word == "`":
            returnText += ""
        elif word == "~":
            returnText += Fore.GREEN + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word == "@":
            returnText += Fore.BLACK + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word == "$":
            returnText += Fore.CYAN + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word == "Random":
            # R = Back.RED
            # G = Back.GREEN
            # B = Back.BLUE
            # R = Fore.RED
            # G = Fore.GREEN
            # B = Fore.BLUE
            # returnText += R + "R" + G + "a" + B + "n" + R + "d" + G + "o" + B + "m" + Fore.WHITE
            # best? returnText += Style.DIM + R + "Ra" + G + "nd" + B + "om" + Fore.WHITE + Back.RESET + Style.NORMAL
            returnText += Fore.MAGENTA + word + Fore.WHITE
        elif word == "Row":
            returnText += Style.BRIGHT + Back.RED + "R" + Back.GREEN + "o" + Back.BLUE + "w" + Style.NORMAL + Back.RESET
        elif word == "Notnil" or word == "Filled":
            returnText += Style.BRIGHT + Fore.BLACK + "Filled" + Style.NORMAL + Fore.WHITE
            # returnText += Fore.MAGENTA + "Nonzero" + Fore.WHITE
        elif word == "R":
            returnText += Fore.RED + word + Fore.WHITE
        elif word == "G":
            returnText += Fore.GREEN + word + Fore.WHITE
        elif word == "B":
            returnText += Fore.BLUE + word + Fore.WHITE
        elif word == "L":
            returnText += Fore.YELLOW + word + Fore.WHITE   
        elif word in ["otherwise", "Otherwise", "may", "May", "+", "-", "Replace", "Mill", "Milling", "Immill", "Then", "Unless", "Turn"]:
            returnText += Style.BRIGHT + word + Style.NORMAL
        elif word in ["Move", "Number", "number", "not", "?"]:
            returnText += Style.BRIGHT + word + Style.NORMAL
        elif word in ["Success", "Successes"]:
            returnText += Fore.GREEN + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word in ["Failure"]:
            returnText += Fore.RED + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word in ["Card", "Cards"]:
            returnText += Fore.GREEN + word + Fore.WHITE
        elif word == "Card(s)":
            returnText += Fore.GREEN + "Card" + Fore.WHITE + "(" + Fore.GREEN + "s" + Fore.WHITE + ")"
        elif word == "Action" or word == "Actions":
            returnText += Style.BRIGHT + Fore.CYAN + word + Style.NORMAL + Fore.WHITE
        elif word in ["Discard", "Discarding"]:
            returnText += Fore.MAGENTA + word + Fore.WHITE
            ## returnText += Fore.MAGENTA + word + Fore.WHITE
        elif word == "Hand":
            returnText += word
            ## returnText += Fore.GREEN + word + Fore.WHITE
        elif word == "FAILURE":
            returnText += Style.BRIGHT + Fore.RED + "[ FAILURE ]" + Fore.WHITE + Style.NORMAL
        elif word == "Cantrip":
            C = Style.NORMAL + Fore.GREEN
            A = Style.BRIGHT + Fore.CYAN
            returnText += C + "C" + A + "a" + C + "n" + A + "t" + C + "r" + A + "i" + C + "p" + Fore.WHITE + Style.NORMAL
        elif word == "Chance":
            returnText += Fore.YELLOW + word + Fore.WHITE
        elif word == "M":
            returnText += Back.WHITE + Style.BRIGHT + Fore.BLACK + word + Style.NORMAL + Fore.WHITE + Back.RESET
        elif word in ["H", "HH"]:
            returnText += Fore.BLACK + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word in ["Enemy", "Enemies", "Carcass"]:
            returnText += Back.RED + word + Back.RESET
        elif word == "Enemy's":
            returnText += Back.RED + "Enemy" + Back.RESET + "'s"
        elif word in ["Band", "Bands", "EXCEPT"]:
            returnText += Fore.RED + Style.BRIGHT + word + Fore.WHITE + Style.NORMAL
        elif word in ["Triggered", "Special", "Gimmick"]:
            returnText += Fore.YELLOW + word + Fore.WHITE
        elif word == "Temporary":
            returnText += Style.DIM + word + Style.NORMAL 
        elif word.isnumeric():
            returnText += Style.BRIGHT + word + Style.NORMAL
        elif word == "#x":
            returnText += Style.BRIGHT + "#" + Style.NORMAL + "x"
        elif word == "x#":
            returnText += "x" + Style.BRIGHT + "#" + Style.NORMAL
        elif word in INITIALIZATION_ZONES.keys():
            returnText += (Fore.BLACK + Style.BRIGHT + INITIALIZATION_ZONES.get(word) 
                            + Fore.WHITE + Style.NORMAL)
        elif word in ["notick"]:
            returnText += "nt"
        elif word in ["Fatal"]:
            returnText += Back.RED + "Fatal" + Back.RESET
        elif word == "FoG":
            returnText += Fore.GREEN
        elif word == "FoW":
            returnText += Fore.WHITE
        elif word == "FoR":
            returnText += Fore.RED
        elif word == "FoY":
            returnText += Fore.YELLOW
        elif word == "ARR":
            returnText += Style.DIM + "-->" + Style.NORMAL
        else:
            if len(word) > 0:
                if word[0:1] == "'" and word[len(word) - 1:len(word)] == "'":                       ## Contains 'text' phrase
                    returnText += Style.BRIGHT + Fore.YELLOW + word + Style.NORMAL + Fore.WHITE
                elif word[0:1] == "'":                                                              ## Starts with '
                    returnText += Style.BRIGHT + Fore.YELLOW + word
                elif word[len(word) - 1:len(word)] == "'":                                          ## Ends with '
                    returnText += Style.BRIGHT + Fore.YELLOW + word + Style.NORMAL + Fore.WHITE
                elif word[0:1] == "^" and word[len(word) - 1:len(word)] == "^":                     ## Contains ^text^ phrase
                    returnText += (Style.BRIGHT + Back.CYAN + " " + word[1:len(word) - 1] + " " 
                                    + Style.NORMAL + Back.RESET)
                elif word[0:1] == "^":                                                              ## Starts with ^
                    returnText += Style.BRIGHT + Back.CYAN + " " + word[1:len(word)]
                elif word[len(word) - 1:len(word)] == "^":                                          ## Ends with ^
                    returnText += (Style.BRIGHT + Back.CYAN + word[0:len(word) - 1] + " " 
                                    + Style.NORMAL + Back.RESET)
                elif word[0:1] == "%" and word[len(word) - 1:len(word)] == "%":                     ## Contains %text% phrase
                    returnText += (Fore.BLACK + Back.RED + " " + word[1:len(word) - 1] + " " 
                                    + Fore.WHITE + Back.RESET)
                elif word[0:1] == "%":                                                              ## Starts with %
                    returnText += Fore.BLACK + Back.RED + " " + word[1:len(word)]
                elif word[len(word) - 1:len(word)] == "%":                                          ## Ends with %
                    returnText += (Fore.BLACK + Back.RED + word[0:len(word) - 1] + " " 
                                    + Fore.WHITE + Back.RESET)
                else:
                    returnText += word

                # elif len(word) > 3:
                #     if word[0:3] == "WTI":
                #         returnText += Style.BRIGHT + word + Style.NORMAL


    return returnText

def splinterize(text: str) -> list[str]:
    """
    Splits a string of text into an array, where each different word, number, punctuation, and grouping of spaces is separated.
    Retains the same order as the original text.

    Example: `splinterize("Hi, I am new!")` returns `["Hi", ",", " ", "I", " ", "am", " ", "new", "!"]`.
    """
    text = str(text)
    returnArray = [""]
    __splinterize(text, returnArray)
    return returnArray
    
def __splinterize(text: str, returnArray: list[str]) -> None:
    if len(text) == 0:
        return
    elif text[0:1] in (PUNCTUATION_TYPES) or text[0:1].isnumeric(): ## Case with punctuation or number
        returnArray.append(text[0:1])
        returnArray.append("")
        __splinterize(text[1:len(text)], returnArray)
    else:
        returnArray[len(returnArray) - 1] = returnArray[len(returnArray) - 1] + text[0:1]
        __splinterize(text[1:len(text)], returnArray)

def yesOrNo(
    text: str,
    preamble: list[str]=[],
    passedInVisuals: "vis.prefabPassedInVisuals"=None,
    scriptedInput: "scriptInput.gameplayScriptInput" = None
) -> bool:
    """
    Allows for an input of yes (True) or no (False). 

    Arguments:
        text (str): the question prompt.
        preamble (list[str]): text that comes before this prompt.
        passedInVisuals (vis.prefabPassedInVisuals): visuals to present if CLEAR is input.
            CLEAR can only be input if this parameter is given.
        scriptedInput (scriptInput.gameplayScriptInput): forced input; mostly for testing.
    """
    # Logging
    log.write_to_log(log_entry.HelperLogEntry.YesOrNo(text, preamble, passedInVisuals))

    newPreamble = []
    for amble in preamble:
        newPreamble.append(amble)
    newPreamble.append(text)
    preamble = newPreamble
    for row in preamble:
        splash(row, printInsteadOfInput = True)

    while True:
        question = ""
        if passedInVisuals != None:
            question += " > (Clear), [Input Noun], "
        question += Fore.YELLOW + "Y" + Fore.WHITE+  "es or " + Fore.RED + "N" + Fore.WHITE + "o: "
        
        if scriptedInput:
            pick = scriptedInput.getNextValue()
        else:
            pick = input(question).lower().strip()

        if pick in ["y", "yes"]:
            return True
        elif pick in ["n", "no"]:
            return False
        elif pick == "clear" and passedInVisuals != None:
            passedInVisuals.display()
            print(" ~ Cleared ~ ")
            for row in preamble:
                splash(row, printInsteadOfInput = True)
        elif passedInVisuals != None and not printCheckProperNouns(pick, passedInVisuals.entityNames, passedInVisuals.cardNames):
            print(" INVALID INPUT ")

def printCheckProperNouns(string: str, entityNames: dict, cardNames: dict) -> bool:
    """Tries to print the name of a proper noun, returning True if it did."""
    string = string.lower().strip()
    if string in entityNames.keys() and string != "":
        splash(entityNames[string], printInsteadOfInput = True)
        return True
    elif string in cardNames.keys() and string != "":
        key = string
        splash("   ^" + cardNames[key].name + "^", printInsteadOfInput = True)
        print(normalize("", 3) + cardNames[key].prettyCardText(3, WIDTH, suppressedTypes = []))
        return True
    return False

def splash(
    text: str, 
    printInsteadOfInput: bool = False, 
    removePreline: bool = False, 
    scriptedInput: "scriptInput.gameplayScriptInput" = None
) -> None:
    """
    Inputs (using `input()`) text for the player using the color-encoding defined in `colorize`.
    Contains special all-caps, underscore-separated key phrases which print specific text. Most commonly used for 'Failure' cases.
    
    Arguments:
        text (str): the text to be colorized and then input.
        printInsteadOfInput (bool): if, instead of waiting for user input after showing this text, it is preferred to `print()` it,
            does so.
        removePreline (bool): if False, includes the " | " before the line.
        scriptedInput (scriptInput.gameplayScriptInput): user-defined scripted input.

    Notes:
        If the scriptedInput.splashOverride_printInsteadOfInput == True, this method acts as if printInsteadOfInput == True.
    """
    ## Special key phrases 
    if text == 'FAIL_MOVE':
        text = "FAILURE Could not Move some Card; there exists no available Card in that expected place."
    if text == 'FAIL_FIND_CARD':
        text = "FAILURE Could not Find some Card; there does not exist that Card in that expected place."
    if text == 'FAIL_PICK_CARD':
        text = "FAILURE Could not Pick a Card; there exists no Card in that expected place that can be picked."
    if text == 'FAIL_DESTROY':
        text = "FAILURE Could not Destroy some Card; there exists no available Card in the expected place."
    elif text == 'FAIL_FIND_ENEMY':
        text = "FAILURE No available Enemy; could not find an Enemy fitting that criteria."
    elif text == 'FAIL_EXTRA_TURN':
        text = "FAILURE Cannot take a 2nd Turn; Entity is already taking and/or to-take a 2nd Turn."
    elif text == 'FAIL_NUMBER':
        text = "FAILURE That number is out of the bounds of possible numbers."
    elif text == 'FAIL_NO_BANDS':
        text = "FAILURE The target entity does not have any band."
    elif text == 'FAIL_ATTEMPT_PLAY_INOPERABLE':
        text = "FAILURE Cannot spend an Action to play an <<inoperable>> Card from Hand nor Pocket."
    if removePreline == False:
        text = " | " + text
    
    ## Does not do input if we want to print OR if we have scripted input
    if printInsteadOfInput or (scriptedInput != None and scriptedInput.splashOverride_printInsteadOfInput):
        print(colorize(trueIndent(text + " ", 3, WIDTH)))
    else:
        input(colorize(trueIndent(text + " ", 3, WIDTH)))

def unionCardLocations(location1: CardLocation, location2: CardLocation, name: str = 'DEFAULT') -> CardLocation:
    """
    Combines two card locations into a new one.
    
    If name == 'DEFAULT', this new clearing will be named `${location1.name} + and ${location2.name}`
    """
    if name == 'DEFAULT':
        name = location1.name + " and " + location2.name

    unionCardLocation = CardLocation(name)
    for card in location1.array + location2.array:
        unionCardLocation.append(card)

    return unionCardLocation
