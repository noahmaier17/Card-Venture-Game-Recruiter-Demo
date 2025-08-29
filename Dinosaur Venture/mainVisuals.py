import math, random, os
from colorama import init, Fore, Back, Style
init(autoreset=True)
import helper as h

WIDTH = h.WIDTH

## Visualizes the map 
##  Returns an array of the locations enter-able in the order listed 
def visualizeMap(locations):
    os.system('cls')
    
    BOUND = h.normalize("% ", WIDTH, separator = "~ ") + "%"
    PAGE_1 = h.normalize("\\ ", WIDTH, separator = "` ") + "\\"
    PAGE_2 = h.normalize("/`", WIDTH, separator = " `") + "/"
    
    enterable = []
    
    print(BOUND)
    for i in range(9):
        print(PAGE_1)
        print(PAGE_2)
    print(BOUND)
    
    print(" | Available Clearings:")
    
    INDENT = 2 * (int)(WIDTH / 5)
    index = 1
    i = 0
    while i < len(locations):
        locale = locations[i]
        
        the = locale.the()
        prefixText = locale.getPrefixText()
        prefixInfoText = locale.getPrefixInfoText(INDENT)
        
        if locale.enterable and not locale.home:
            string = (" " + str(index) + ": " + the + Fore.CYAN + Style.BRIGHT + prefixText 
                + Fore.YELLOW + h.normalize(locale.name, INDENT - len(the + prefixText) - 4) 
                + Fore.WHITE + Style.NORMAL + prefixInfoText)
            
            print(string)
            
            index += 1
            enterable.append(locale)
        
        if locale.enterable:
            for child in locale.children:
                locations.append(child)
        
        i += 1
        
    return enterable

def rainbowColorizeFetcher(number):
    number = int(number)
    text = Style.BRIGHT
    if number == 0:
        text += Fore.BLACK
    elif number == 1:
        text += Fore.RED
    elif number == 2:
        text += Fore.YELLOW
    elif number == 3:
        text += Fore.GREEN
    else:
        text += Fore.BLUE

    return text


## Makes this number colored, and normalizes the text
##  number: the number (can be a number represented as a string)
##  length: how far to normalize
##  separator: what to add to the end of the text to normalize it
def rainbowNormalize(number, length, separator = " "):
    number = int(number)
    text = rainbowColorizeFetcher(number)

    return text + h.normalize(number, length, separator) + Style.NORMAL + Fore.WHITE

## Makes a pretty-to-look-at display of the 4 core mats: Hand, Draw, Discard, Play
##  Hand: Green     Draw: Magenta         Discard: Red        Play: Cyan        
def niceFourMats(entity):
    text = ""
    matsAsArray = [entity.play.length(), entity.pocket.length(), entity.hand.length(), entity.draw.length(), entity.discard.length(), entity.intoHand.length(), entity.intoIntoHand.length()]
    
    if entity.enemy == True:
        text += Fore.RED
    else:
        text += Fore.CYAN
    if matsAsArray[0] > 0:
        text += h.normalize("", 2 * matsAsArray[0], separator = "P ")
        
        if matsAsArray[0] > 0 and sum(matsAsArray[1:len(matsAsArray)]) > 0:
            text += Fore.WHITE + "~ "
    else:
        pass
        text += Fore.WHITE + "~ "
        ## text += "/" + Fore.WHITE + " ~ "

    if matsAsArray[1] > 0:
        text += Fore.MAGENTA + h.normalize("", 2 * matsAsArray[1], separator = "p ")
        if sum(matsAsArray[2:len(matsAsArray)]) > 0:
            text += Fore.WHITE + "- "

    if matsAsArray[2] > 0:
        text += Fore.GREEN + h.normalize("", 2 * matsAsArray[2], separator = "H ")
        if sum(matsAsArray[3:len(matsAsArray)]) > 0:
            text += Fore.WHITE + "- "


    spacesUntilNextHandSize = entity.nextHandDrawCount(simplyObserve = True)
    text = text[:-1] + Fore.BLACK + Style.BRIGHT + "[" + Style.NORMAL + Fore.WHITE

    ## Edge case where our spacesUntilNextHandSize == 0
    if spacesUntilNextHandSize == 0:
        text += Fore.BLACK + Style.BRIGHT + "]" + Style.NORMAL + Fore.WHITE

    if spacesUntilNextHandSize > matsAsArray[3]:
        text += Fore.YELLOW + h.normalize("", 2 * matsAsArray[3], separator = "D ")
        spacesUntilNextHandSize -= matsAsArray[3]
    else:
        if spacesUntilNextHandSize > 0:
            text += Fore.YELLOW + h.normalize("", 2 * (spacesUntilNextHandSize), separator = "D ")
        if spacesUntilNextHandSize > 0:
            text = text[:-1] + Fore.BLACK + Style.BRIGHT + "]" + Style.NORMAL + Fore.WHITE
        text += Fore.YELLOW + h.normalize("", 2 * (matsAsArray[3] - spacesUntilNextHandSize), separator = "D ")
        spacesUntilNextHandSize -= matsAsArray[3]


    if matsAsArray[3] > 0 and sum(matsAsArray[4:len(matsAsArray)]) > 0:
        text += Fore.WHITE + "- "


    if spacesUntilNextHandSize > matsAsArray[4] or spacesUntilNextHandSize < 0:
        text += Fore.MAGENTA + h.normalize("", 2 * matsAsArray[4], separator = "d ")
        spacesUntilNextHandSize -= matsAsArray[4]
    else:
        if spacesUntilNextHandSize > 0:
            text += Fore.MAGENTA + h.normalize("", 2 * (spacesUntilNextHandSize), separator = "d ")
        if spacesUntilNextHandSize > 0:
            text = text[:-1] + Fore.BLACK + Style.BRIGHT + "]" + Style.NORMAL + Fore.WHITE
        text += Fore.MAGENTA + h.normalize("", 2 * (matsAsArray[4] - spacesUntilNextHandSize), separator = "d ")
        spacesUntilNextHandSize -= matsAsArray[4]

    if spacesUntilNextHandSize > 0:
        text = text[:-1] + Fore.BLACK + Style.BRIGHT + "+" + str(spacesUntilNextHandSize) + "]" + Style.NORMAL + Fore.WHITE

    if matsAsArray[4] > 0 and sum(matsAsArray[5:len(matsAsArray)]) > 0:
        text += Fore.WHITE + "~ "

    text += Fore.BLUE + h.normalize("", 2 * matsAsArray[5], separator = "I ")
    if matsAsArray[5] > 0 and sum(matsAsArray[6:len(matsAsArray)]) > 0:
        text += Fore.WHITE + "- "

    text += Style.BRIGHT + Fore.BLUE + h.normalize("", 2 * matsAsArray[6], separator = "i ") + Style.NORMAL
    
    
    return text

## Prints the zones, based on if we need to worry about it.
def niceImportantZones(dino, enemies):
    text = " | ENTITIES                      | HEALTH                  | " + Style.BRIGHT + Fore.CYAN + "Act" + Style.NORMAL + Fore.WHITE + ". | " + Fore.CYAN + "P" + Fore.WHITE + "lay ~ "

    emptyPockets = True
    for entity in [dino] + enemies:
        if entity.pocket.length() > 0:
            emptyPockets = False
    if not emptyPockets:
        text += Fore.MAGENTA + "p" + Fore.WHITE + "ocket - "

    text += Fore.GREEN + "H" + Fore.WHITE + "and - " + Fore.YELLOW + "D" + Fore.WHITE + "raw - " + Fore.MAGENTA + "d" + Fore.WHITE + "isc"

    trailing = [0, 0]
    for entity in [dino] + enemies:
        trailing[0] += entity.intoHand.length()
    for entity in [dino] + enemies:
        trailing[1] += entity.intoIntoHand.length()

    if sum(trailing[0:len(trailing)]) > 0:
        text += " ~ "
    if trailing[0] > 0:
        text += Fore.BLUE + "I" + Fore.WHITE + "nto H"

    if sum(trailing[0:1]) != 0 and sum(trailing[1:len(trailing)]) > 0:
        text += " - "
    if trailing[1] > 0:
        text += Style.BRIGHT + Fore.BLUE + "I" + Fore.WHITE + Style.NORMAL + "nto I H"

    return text

## Prints, with all indentation cared for, what is lingering for an Entity. 
##  Returns a boolean indicating if something was printed. 
def printNiceLingering(entity, prefix, suffix):
    if entity.play.length() > 0:
        text = [" |     Lingering: "]
        padding = len(text[0])
        length = padding - 1
        
        for i in range(entity.play.length()):
            card = entity.play.at(i)
            
            newText = ""
            plusLength = 0
            '''
            if card.foreverLinger:
                newText += Style.BRIGHT + "!" + Style.NORMAL + "-"
            else:
                newText += Style.BRIGHT + str(card.lingering) + Style.NORMAL + "-"
            '''
            if card.foreverLinger:
                newText += Style.DIM + "HH" + Style.NORMAL + "-"
            else:
                newText += Style.BRIGHT + str(card.lingering) + Style.DIM + "H" + Style.NORMAL + "-"

            newText += prefix + " " + card.nameWithTokens() + " " + suffix

            ##            HH  -   `   card name                    `
            plusLength += 2 + 1 + 1 + len(card.nameWithTokens()) + 1

            if i != entity.play.length() - 1:
                newText += ", "
                plusLength += 2
            
            if length + plusLength > h.WIDTH:
                text.append(h.normalize(" | ", padding))
                length = padding - 1
            
            text[len(text) - 1] += newText
            length += plusLength
            
        for row in text:
            print(row)
    
    elif entity.enemy == False:
        print(" |     empty, awaiting...")

class prefabPassedInVisuals():
    def __init__(self, entityNames, cardNames):
        self.entityNames = entityNames
        self.cardNames = cardNames

## Creates a way to easily pass into a function calls printDinoTurn
class prefabPrintDinoTurn(prefabPassedInVisuals):
    def __init__(self, dino, enemies, roundCount, clearing, entityNames, cardNames, event, extraSupressedTypes = []):
        super().__init__(entityNames, cardNames)
        self.storedDino = dino
        self.storedEnemies = enemies
        self.storedRoundCount = roundCount
        self.storedClearing = clearing
        self.event = event
        self.storedExtraSupressedTypes = extraSupressedTypes

    def display(self):
        printDinoTurn(self.storedDino, self.storedEnemies, self.storedRoundCount, self.storedClearing, self.event, extraSupressedTypes = self.storedExtraSupressedTypes)

## Creates a way to easily pass into a function calls printDinoTurn
class prefabPrintEnemyTurn(prefabPassedInVisuals):
    def __init__(self, enemy, dino, enemies, roundCount, clearing, enemyIndex, event, entityNames, cardNames):
        super().__init__(entityNames, cardNames)
        self.storedEnemy = enemy
        self.storedDino = dino
        self.storedEnemies = enemies
        self.storedRoundCount = roundCount
        self.storedClearing = clearing
        self.storedEnemyIndex = enemyIndex
        self.event = event

    def display(self):
        printEnemyTurn(self.storedEnemy, self.storedDino, self.storedEnemies, self.storedRoundCount, self.storedClearing, self.storedEnemyIndex, self.event)

class prefabEmpty(prefabPassedInVisuals):
    def __init__(self):
        pass

    def display(self):
        pass
        ## print("No visuals.")

## Prints the display on Dino's Turns
def printDinoTurn(dino, enemies, roundCount, clearing, event, extraSupressedTypes = []):
    supressedTypes = extraSupressedTypes

    os.system('cls')

    ## ----- DISPLAY CODE -----
    print(" | [Round: " + str(roundCount + 1) + " % 2] [Turn: " + str(dino.turn) + "] Scavenging Through: "             + Fore.YELLOW + Style.BRIGHT + clearing.table[0])   
    print(h.normalize("-X-", WIDTH + 2, separator = "-"))
    print(niceImportantZones(dino, enemies))

    print(" " + Fore.GREEN + ">" + Fore.WHITE + " a. " 
        + Fore.GREEN + h.normalize(dino.getDisplayName(), 26) + Fore.WHITE + " | " 
        + dino.hp.displayHealth(23) + " | " 
        + rainbowNormalize(dino.actions, 1) + "->" + rainbowNormalize(dino.nextTurnActionCount(simplyObserve = True), 1) + " | " + niceFourMats(dino))

    printNiceLingering(dino, Back.CYAN + Style.BRIGHT, Back.BLACK + Style.NORMAL)

    ## print(h.normalize(" | ` ` [ In Between Phases ] ` ` | ` ` ` ` ` ` ` ` ` ` ` ` | ` ` | ` ", WIDTH + 2, separator = "` "))
    index = 1
    for enemy in enemies:
        if enemy.dead == False:
            print(" | " + str(index) + ". " + h.normalize(enemy.getDisplayName(), 27) + "| " 
                + enemy.hp.displayHealth(23) + " | " 
                + rainbowNormalize(enemy.actions, 1) + "->" + rainbowNormalize(enemy.nextTurnActionCount(simplyObserve = True), 1) + " | " + niceFourMats(enemy))
            
            printNiceLingering(enemy, Fore.BLACK + Back.RED, Fore.WHITE + Back.BLACK)
        
        else:
            print(" | " + str(index) + ". Carcass                                              | null | null")
        index += 1
    
    printDinoHand(dino, enemies, roundCount, clearing, supressedTypes, event)
    print("")

## Helper Function. Prints the Cards in Dino's Hand.
def printDinoHand(dino, enemies, roundCount, clearing, supressedTypes, event):
    print(h.normalize("-X-", WIDTH + 2, separator = "-"))

    removeBetweenLineSpaces = False
    smushedText = ""
    if dino.pocket.length() + dino.hand.length() > 7:
        removeBetweenLineSpaces = True
        smushedText = " (smushed)"

    if (dino.pocket.length() > 0):
        ## print(eventText(event) + Fore.GREEN + "Cards" + Fore.WHITE + " in " + dino.name + "'s Pocket:")
        print(eventText(event) + dino.name + "'s Pocket" + smushedText + ":")
        printLocation(dino.pocket.getArray(), 0, Back.MAGENTA, supressedTypes, event, removeBetweenLineSpaces = removeBetweenLineSpaces)

    ## print(eventText(event) + Fore.GREEN + "Cards" + Fore.WHITE + " in " + dino.name + "'s Hand:")
    print(eventText(event) + dino.name + "'s Hand" + smushedText + ":")
    if (dino.hand.length() == 0):
        print(eventText(event) + "  Nothing but flies...")
    else:
        printLocation(dino.hand.getArray(), dino.pocket.length(), Back.CYAN, supressedTypes, event, removeBetweenLineSpaces = removeBetweenLineSpaces)

## Helper Function. Gets, line-by-line, the name of the Card + tokens.
def getLineByLineCardName(card, length, prefix = ""):
    ## ----- Initialization -----
    TOKEN_PREFIX = "<<"
    TOKEN_SUFFIX = ">>"
    lines = [" "]
    includeCommas = False

    ## --- Displays Card Name ---
    nextBloc = ""
    cardName = prefix + card.name
    for index, word in enumerate(h.splinterize(cardName)):
        nextBloc += word        
        ## If we only have spaces or nothing in this nextBloc, we do not care about it yet
        if nextBloc.isspace() or nextBloc == "":
            continue

        if len(lines[-1]) + len(nextBloc) + len("  ") > length:
            ## Depending on the number of preceeding spaces, we must append a padded number of spaces
            leadingSpaces = 0
            for char in nextBloc:
                if char == " ":
                    leadingSpaces += 1
                else:
                    break

            if leadingSpaces == 0:
                lines.append("  ")
            if leadingSpaces == 1:
                lines.append(" ")
            if leadingSpaces == 2:
                lines.append("")

        lines[-1] += nextBloc
        nextBloc = ""

    ## Adds all the trailing double spaces (AND/OR, the double space before tokens)
    for i in range(len(lines)):
        lines[i] += "  "

    ## --- Displays Tokens ---
    hadAnyTokensDisplayed = False
    firstToken = True
    startingTokenLine = len(lines) - 1

    for index, token in enumerate(card.tokens):
        if token.displayByName:
            hadAnyTokensDisplayed = True
            nextBloc = TOKEN_PREFIX + token.name + TOKEN_SUFFIX
            if index != len(card.tokens) - 1:
                nextBloc += ","

            if len(lines[-1]) + len(nextBloc) + len("  ") > length:
                if firstToken:
                    startingTokenLine += 1

                ## Depending on the number of preceeding spaces, we must append a padded number of spaces
                leadingSpaces = 0
                for char in nextBloc:
                    if char == " ":
                        leadingSpaces += 1
                    else:
                        break

                if leadingSpaces == 0:
                    lines.append("  ")
                if leadingSpaces == 1:
                    lines.append(" ")
                if leadingSpaces == 2:
                    lines.append("")

            lines[-1] += nextBloc
            firstToken = False

    ## Adds all the trailing double spaces
    if hadAnyTokensDisplayed:
        for i in range(startingTokenLine, len(lines)):
            lines[i] += "  "

    return lines

## Helper Function. Prints cards of a given location.
def printLocation(location, index, color, supressedTypes, event, nameFore = Fore.WHITE, removeBetweenLineSpaces = False):
    firstPass = True

    for card in location:
        ## ----- Does suppression for "Revealed" Cards -----
        supressedTypesPlusExtra = []
        for singleType in supressedTypes:
            supressedTypesPlusExtra.append(singleType)
        if card.revealed == True and "revealed" in supressedTypes:
            supressedTypesPlusExtra.append("p")

        ## ----- Initialization -----
        arrayIndex = 0
        nameTokensTextArray = getLineByLineCardName(card, 28, prefix = " ")
        bodyTextArray = card.niceBodyText(43, WIDTH, supressedTypes = supressedTypesPlusExtra, keepAsArray = True)
        if len(bodyTextArray) == 0:
            bodyTextArray.append("")

        ## ----- Prints -----
        if not firstPass and not removeBetweenLineSpaces:
            print(eventText(event) + " ")

        while arrayIndex < len(nameTokensTextArray) or arrayIndex < len(bodyTextArray):
            if len(nameTokensTextArray) == arrayIndex:  ## Not enough nameTokensTextArray length
                nameTokensTextArray.append("")
            if len(bodyTextArray) == arrayIndex:        ## Not enough bodyTextArray length
                bodyTextArray.append("")

            if arrayIndex == 0:                         ## First row
                print(eventText(event) + " " + Style.BRIGHT + h.normalize("", max(28 - len(nameTokensTextArray[arrayIndex]), 0))
                    + color + nameFore + nameTokensTextArray[arrayIndex] + Back.BLACK + Fore.WHITE + Style.NORMAL + " "
                    + " < " + str(index + 1) + " >" + (3 - len(str(index + 1))) * " "
                    + bodyTextArray[arrayIndex])
            else:
                ## If the card is not a shell, we add the single-space indent
                indentation = "         "
                if not card.isShellCard:
                    indentation += " "
                print(eventText(event) + " " + Style.BRIGHT + h.normalize("", max(28 - len(nameTokensTextArray[arrayIndex]), 0))
                    + color + nameFore + nameTokensTextArray[arrayIndex] + Back.BLACK + Fore.WHITE + Style.NORMAL + indentation
                    + bodyTextArray[arrayIndex])

            arrayIndex += 1

        index += 1
        firstPass = False

## Prints the display on Enemy's Turns
def printEnemyTurn(enemy, dino, enemies, roundCount, clearing, enemyIndex, event):
    os.system('cls')
    ## ----- DISPLAY CODE -----
    print(" | [Round: " + str(roundCount + 1) + " % 2] [Turn: " + str(enemy.turn) + "] Scavenging Through: " 
        + Fore.YELLOW + Style.BRIGHT + clearing.name)
    print(h.normalize("-X-", WIDTH + 2, separator = "-"))
    
    print(niceImportantZones(dino, enemies))
    
    print(" | a. " + h.normalize(dino.name, 26) + " | " 
        + dino.hp.displayHealth(23) + " | " 
        + rainbowNormalize(dino.actions, 1) + "->" + rainbowNormalize(dino.nextTurnActionCount(simplyObserve = True), 1) + " | " + niceFourMats(dino))

    printNiceLingering(dino, Back.CYAN + Style.BRIGHT, Back.BLACK + Style.NORMAL)

    ## print(h.normalize(" | ` ` [ In Between Phases ] ` ` | ` ` ` ` ` ` ` ` ` ` ` ` | ` ` | ` ", WIDTH + 2, separator = "` "))
    index = 0
    for subEnemy in enemies:
        barOrArrow = " | "
        greenOrWhite = Fore.WHITE
        if enemyIndex == index:
            barOrArrow = Fore.GREEN + " > " + Fore.WHITE
            greenOrWhite = Fore.GREEN
        
        if subEnemy.dead == False:
            print(barOrArrow + str(index + 1) + ". " + greenOrWhite 
                + h.normalize(subEnemy.getDisplayName(), 27) + Fore.WHITE + "| " 
                + subEnemy.hp.displayHealth(23) + " | " 
                + rainbowNormalize(subEnemy.actions, 1) + "->" + rainbowNormalize(subEnemy.nextTurnActionCount(simplyObserve = True), 1) + " | " + niceFourMats(subEnemy))
            
            printNiceLingering(subEnemy, Fore.BLACK + Back.RED, Fore.WHITE + Back.BLACK)

        else:
            print(barOrArrow + str(index + 1) + ". " + greenOrWhite + "Carcass" + Fore.WHITE +"                                              | null | null")
        index += 1
    print(h.normalize("-X-", WIDTH + 2, separator = "-"))
    

def wildernessMap(dino, roundCount, allNeckOfTheWoods):
    count = 1
    for notw in allNeckOfTheWoods:
        print(" | " + str(count) + ": the " + Fore.MAGENTA + notw + Fore.WHITE + ".")
        count += 1
    print(" | " + str(count) + ": an Arbitrary Direction.")

## Gets the color of the header depending on the current event value
def eventText(event):
    eventText = " | "
    if event == "Dino Play Card":
        eventText = " " + Fore.GREEN + Style.BRIGHT + "|" + Fore.WHITE + Style.NORMAL + " "
    elif event == "Dino Turn End":
        eventText = " " + Fore.BLUE + Style.BRIGHT + "|" + Fore.WHITE + Style.NORMAL + " "
    return eventText






'''
KEEPING BECAUSE ANNOYING TO TYPE
h.normalize(len(dino.hand), 3) 
        + " | " + h.normalize(len(dino.draw), 3) 
        + " | " + h.normalize(len(dino.discard), 3) 
        + " | " + h.normalize(len(dino.play), 3))
'''










