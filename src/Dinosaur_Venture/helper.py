import math, random, os, copy
from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import card as c, cardTokens as tk

WIDTH = 117 - 2

## Types of punctuation we splinterize, and that we do not want a new indent line to begin with
PUNCTUATION_TYPES = [' ', ',', '!', '.', '-', ':', ';', '?', '{', '}', '[', ']', '(', ')', '*', '`']
MULTIPLICATIVE_NUMERAL_TYPES = ["Nonce", "Once", "Twice", "Thrice", "Quarce", "Quince", "Sextce", "Spece", "Octce", "Nince", "Tence"]
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

## Overhead for drafting a Card from a loot table
def selectCard(dino, clearingName, roundCount, lootTables, pullsTable, lootVacuously = False, canPass = False, activateAbilityOnPass = False):
    from mainVisuals import printLocation

    ## Currently not used; if we want to loot without seeing all card text
    supressedTypes = []

    for table in lootTables:
        table.shuffle()

    ## Are we even going to loot?
    if (lootVacuously == False and dino.looting <= 0):
        return

    ## Visuals
    lootingInstances = dino.looting
    if lootVacuously:
        lootingInstances = 1

    os.system('cls')
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
                + dino.deck.at(i).niceBodyText(41, WIDTH, supressedTypes = []))
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
    pulledFromLootTable = cardLocation("pulled loot table")
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
        holdingSpot = cardLocation("Card to Pick")

        ## print(" -- Drafting to <<" + holdingSpot.niceName() + ">> --")
        if pulledFromLootTable.length() == 0 or (pulledFromLootTable.length() == 0):
            print(pulledFromLootTable.length())
            input(" Attempted to draft cards, but Pulls: " + str(pulledFromLootTable.length()) + " and pulledFromLootTable: " + str(pulledFromLootTable))
            return
        
        draftPoolCopy = cardLocation("")
        for card in pulledFromLootTable.getArray():
            draftPoolCopy.append(copy.deepcopy(card))

        picks = cardLocation("")
        for i in range(pulledFromLootTable.length()):
            if draftPoolCopy.length() > 0:
                picks.append(draftPoolCopy.pop(random.randint(0, draftPoolCopy.length() -1)))
                '''
                print(" " + str(i + 1) + ". " 
                        + Back.CYAN + Style.BRIGHT + " " + picks.at(i).name + " "
                        + Back.RESET + Style.NORMAL 
                        + normalize("", 41 - 5 - len(str(i+1)) - len(picks.at(i).name) - 3) + ":  "
                        + picks.at(i).niceBodyText(41, WIDTH, supressedTypes))
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

## Checks for if a given card is found within an array of cards. 
##  Returns the index of that array if found, otherwise returning -1. 
def locateCardIndex(array, card):
    i = 0
    for crosscheckCard in array.getArray():
        if card.isEqual(crosscheckCard):
            return i
        i += 1
    return -1

## Allows user to pick a living enemy.
def pickLivingEnemy(text, enemies, preamble = [], passedInVisuals = "null"):
    excludingValues = []
    allDead = True
    for i in range(len(enemies)):
        if enemies[i].dead == True:
            excludingValues.append(i + 1)
        else:
            allDead = False
    
    if allDead == True:
        return -1
    
    return pickValue(text, range(1, len(enemies) + 1), preamble = preamble, passedInVisuals = passedInVisuals, excludingValues = excludingValues) - 1

## Gets index of the front-est living Enemy. Returns -1 if no enemy matches that criteria. 
def getFrontLivingEnemyIndex(enemies):
    for i in range(len(enemies)):
        if enemies[i].dead == False:
            return i
    return -1

## Gets index of the next living Enemy, given a position in the enemies list to start from. 
##  Returns -1 if no enemy matches that criteria. 
def getNextLivingEnemyIndex(enemies, relativeIndex):
    for i in range(relativeIndex + 1, len(enemies)):
        if enemies[i].dead == False:
            return i
    for i in range(0, relativeIndex + 1):
        if enemies[i].dead == False:
            return i
    return -1

## Returns a count of the number of dead enemies
def deadCount(enemies):
    deadCount = 0
    for enemy in enemies:
        if enemy.dead == True:
            deadCount += 1
    return deadCount

## Pick a number, unbounded* (capped at 99)
def pickNonNegativeNumber(text, preamble = [], passedInVisuals = "null", canPass = False):
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

## Returns a card picked from a location.
def fetchCardFromLocation(text, location):
    preamble = []
    index = 1
    for card in location.getArray():
        preamble.append(str(index) + ": ^" + card.name + "^.")
        index += 1

    pick = pickValue(text, range(1, index), preamble = preamble) - 1
    return location.at(pick)


## Helper method -- With some text prompt and set of values, waits for user input until the
##  input value is within the set. 
##  excludingValues are numbers which are not valid.
##  If user inputs 'pass' and canPass = True, returns -1.
## TIP for picking a value from an array: ' range(1, len(LIST) + 1) '
## TIP for picking a card index: pickValue("TEXT", range(1, len(LIST) + 1)) - 1
def pickValue(text, setOfValues, excludingValues = [], preamble = [], passedInVisuals = "null", canPass = False, intType = True):
    ## OBSERVE: Copy and pasted code from here into pickNonNegativeNumber

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

## With some text prompt and set of letters, lets the user pick one such letter, returning it.
##  Case-insensitive; returns the lowercase version of the letter.  
def pickLetter(text, setOfLetters, excludingValues = []):
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

## Sets a certain amount of 'separator' (meaning often white) space after a name. 
##  If the input length is too long, ends it with ".."
def normalize(text, spaces, separator = " ", cutFat = False) -> str:
    text = str(text)
    if spaces <= len(text) and len(text) < spaces + len(separator):
        if cutFat:
            text = text[0:spaces]
        
        return text
    elif len(text) > spaces:
        return text[0:max(spaces - 2, 0)] + ".."
    else:
        return normalize(text + separator, spaces, separator = separator, cutFat = cutFat)


## Indents each line of some given text. 
##  Has no trailing line break, nor include any lines that would be purely blank. 
##  text: the text we are giving an indent
##  leftIndent: how many blank spaces until this given text is to be situated
##  length: how long until we wrap around and indent
##  nextLineText: after X number of white spaces from the left indent, what else to print
def trueIndent(text, leftIndent, length, nextLineText = " ", keepAsArray = False):
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

## Truncates numbers to nearest thirds if in that form
def roundThird(number):
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
    
## Adds a plusValue to a dictionary, given a key. 
def plusDict(dictionary, key, plusValue):
    if key in dictionary.keys():
        dictionary.update({key: dictionary.get(key) + plusValue})
    else:
        dictionary.update({key: plusValue})

## Checks if the crosscompareValue is greater or equal to the dictionary key value. 
def dictContainsAtLeast(dictionary, key, crosscompareValue):
    if key in dictionary.keys():
        if crosscompareValue <= dictionary.get(key):
            return True
    return False

unlockConditions = {
    "Unlocked_Belly_Filled_Shrew": "3 or more 'Shrews' eliminated in one turn",
    "Unlocked_Hungry_Wolf": "You made it one turn" 
}

'''
## Updates the save value accordingly. 
##  saveFile: the save file name. 
##  key: the value on save. 
##  updatedValue: the new thing to make the key paired to. 
##  splashText: what to say if this variable got updated. 
def saveUpdate(saveFile, key, updatedValue, majorSplashText):
    minorSplashText = unlockConditions.get(key)
    newFile = ""
    file = open(str(saveFile), 'r')
    for line in file:
        keyValuePair = line.split(": ")
        if keyValuePair[0] == key and keyValuePair[1] != str(updatedValue) + "\n":
            splash(Fore.YELLOW + "Unlocked Achieved" + Fore.WHITE + ": "
                + majorSplashText, printInsteadOfInput = True)
            splash(" - Requirement: " + Fore.YELLOW + minorSplashText + ".", 
                printInsteadOfInput = True)
            yetToTypeYes = True
            while yetToTypeYes:
                yetToTypeYes = not yesOrNo("Type (Y)es to Continue.")
            newFile += keyValuePair[0] + ": " + str(updatedValue) + "\n"
        else:
            newFile += line

    file.close()
    file = open(str(saveFile), 'w+')
    file.write(newFile)
    file.close()
'''

## Linked list implementation of damage strings, allowing for long attack strings to 
##  be created. 
class acons():
    def __init__(self, datum, tail): ## datum in the form [ damage, channel ]
        self.damage = datum[0]
        self.channel = datum[1]
        self.tail = tail

    def __str__(self):
        if self.tail == 'nil':
            return str(self.damage) + str(self.channel)
        else:
            return str(self.damage) + str(self.channel) + " / " + self.tail.__str__()

    ## Removes the -notick from this damage array
    def stripNotick(self):
        if self.tail == 'nil':
            return
        else:
            if self.channel[-len("-notick"):len(self.channel)] == '-notick':
                self.channel = self.channel[0:-len("-notick")]
            return self.tail.stripNotick()

## Adds colors to variables of a string, returning that newly colorized string
def colorize(text):
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
        elif word == "Notnil":
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
        elif word in c.INITIALIZATION_ZONES.keys():
            returnText += (Fore.BLACK + Style.BRIGHT + c.INITIALIZATION_ZONES.get(word) 
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

## Splits a string of text into an array, 
##  where each different word, number, punctuation, and grouping of spaces is separated.
##  Retains the same order as the original text. 
##  For example: "Hi, I am new!" --> ["Hi", ",", " ", "I", " ", "am", " ", "new", "!"]
def splinterize(text):
    text = str(text)
    returnArray = [""]
    __splinterize(text, returnArray)
    return returnArray
    
def __splinterize(text, returnArray):
    if len(text) == 0:
        return
    elif text[0:1] in (PUNCTUATION_TYPES) or text[0:1].isnumeric(): ## Case with punctuation or number
        returnArray.append(text[0:1])
        returnArray.append("")
        __splinterize(text[1:len(text)], returnArray)
    else:
        returnArray[len(returnArray) - 1] = returnArray[len(returnArray) - 1] + text[0:1]
        __splinterize(text[1:len(text)], returnArray)

## Allows for an input of yes (True) or no (False). 
##  text: the question to be asked. 
def yesOrNo(text, preamble = [], passedInVisuals = "null"):
    newPreamble = []
    for amble in preamble:
        newPreamble.append(amble)
    newPreamble.append(text)
    preamble = newPreamble
    for row in preamble:
        splash(row, printInsteadOfInput = True)

    while True:
        question = ""
        if passedInVisuals != "null":
            question += " > (Clear), [Input Noun], "
        question += Fore.YELLOW + "Y" + Fore.WHITE+  "es or " + Fore.RED + "N" + Fore.WHITE + "o: "
        
        pick = input(question).lower().strip()
        if pick in ["y", "yes"]:
            return True
        elif pick in ["n", "no"]:
            return False
        elif pick == "clear" and passedInVisuals != "null":
            passedInVisuals.display()
            print(" ~ Cleared ~ ")
            for row in preamble:
                splash(row, printInsteadOfInput = True)
        elif passedInVisuals != "null" and not printCheckProperNouns(pick, passedInVisuals.entityNames, passedInVisuals.cardNames):
            print(" INVALID INPUT ")

## Tries to print the name of a proper noun, returning True if it did. 
def printCheckProperNouns(string, entityNames, cardNames):
    string = string.lower().strip()
    if string in entityNames.keys() and string != "":
        splash(entityNames[string], printInsteadOfInput = True)
        return True
    elif string in cardNames.keys() and string != "":
        key = string
        splash("   ^" + cardNames[key].name + "^", printInsteadOfInput = True)
        print(normalize("", 3) + cardNames[key].niceBodyText(3, WIDTH, supressedTypes = []))
        return True
    return False

## Turns an array of cards into an array of card names, returned
## Of the same order as the original array
def cardsToCardNames(array):
    returnArray = []
    for card in array:
        returnArray.append(card.name)
    return returnArray

## Inputs, then colorizes the text. 
def splash(text, printInsteadOfInput = False, removePreline = False):
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
    
    if printInsteadOfInput:
        print(colorize(trueIndent(text + " ", 3, WIDTH)))
    else:
        input(colorize(trueIndent(text + " ", 3, WIDTH)))

## Makes a Clearing location
'''
class locale():
    def __init__(self, name, enterable, home = False):
        self.name = name
        self.enterable = enterable
        self.home = home
        
        self.children = []
        
        self.hillside = False
        self.renown = False
    
    def addPrefix(self, renown = False, hillside = False):
        self.renown = self.renown or renown
        self.hillside = self.hillside or hillside
    
    def getPrefixInfoText(self, indent):
        array = []
        if self.renown:
            array.append("+1 Looting when Entered.")
        if self.hillside:
            array.append("This Locale Reveals an extra, separated Clearing.")
        
        string = ""
        first = True
        for element in array:
            if not first:
                string += ("\n" 
                    + normalize("    ", indent, separator = " . ", cutFat = True) 
                    + element)
            else:
                string += element
                first = False
        return string
    
    def the(self):
        if len(self.getArrayOfPrefixes()) > 0:
            return "The "
        return ""
    
    def getArrayOfPrefixes(self):
        array = []
        if self.renown:
            array.append("Renown")
        if self.hillside:
            array.append("Hilly")
        return array
    
    def getPrefixText(self):
        array = self.getArrayOfPrefixes()
        
        if len(array) == 0:
            return ""
        
        string = ""
        first = True
        for element in array:
            if not first:
                string += ", " + element
            else:
                string += element
                first = False
        return string + " "
    
    def addChild(self, childLocale):
        self.children.append(childLocale)

    def removeChild(self, childLocale):
        newChildren = []
        for i in range(len(self.children)):
            if self.children[i].name != childLocale:
                newChildren.append(self.children[i])
        self.children = newChildren
'''

## Health functionality
class healthcons():
    def __init__(self, r, g, b, tail):
        self.r = r
        self.g = g
        self.b = b
        self.tail = tail
        self.isDeathHealthcons = False
        self.onBreakDiscardHand = False
        self.onBreakSpecial = False
        ## RI: getBands = number of bands this health entity has

    ## Returns the count of bands
    def getBands(self):
        if self.tail == "nil":
            return 1
        else:  
            return 1 + self.tail.getBands()
    
    ## Certain bands can break and cause specific triggers. This adds visuals for that. 
    ##  ONLY CALL THIS FROM THE ENTITY FUNCTION OF THE SAME NAME
    def publishBandBreak(self, number, discardHand, special):
        self.__publishBandBreak(number - 1, discardHand, special)
        
    def __publishBandBreak(self, number, discardHand, special):
        if number == 0:
            self.onBreakDiscardHand = discardHand
            self.onBreakSpecial = special
        elif self.tail == 'nil' or number < 0:
            print("ERROR!!! There is not a band that exists where we can publish a band break!")
            print(0/0)
        else:
            self.tail.__publishBandBreak(number - 1, discardHand, special)
    
    ## Converts this data structure into a nested array structure, but also colors in each channel
    def displayHealth(self, normalizeValue):
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

        return normalize(returnText, normalizeValue)
    
    ## Converts healthcons into a nested array structure
    def toArray(self):
        if self.getBands() == 0:
            return [[0, 0, 0]]
        else:
            returnArray = []
            self.__toArray(returnArray)
            return returnArray
        
    def __toArray(self, returnArray):
        returnArray.append([self.r, self.g, self.b])
        if self.tail != "nil":
            self.tail.__toArray(returnArray)

    ## Replaces the ith band with this new band of HP.
    ##      Make sure that the index < number of bands.
    def replaceBand(self, index, array):
        if (index == 0):
            self.r = array[0]
            self.g = array[1]
            self.b = array[2]
            return
        else:
            self.tail.replaceBand(index - 1, array)

    ## Creates a string representation of the health counts, MOSTLY FOR DEBUGGING
    def __str__(self):
        if self.tail == "nil":
            return "["+str(self.r)+", "+str(self.g)+", "+str(self.b)+"]"
        else: 
            return "["+str(self.r)+", "+str(self.g)+", "+str(self.b)+"] - "+self.tail.__str__()

class deadHealthcons(healthcons):
    def __init__(self):
        super().__init__(0, 0, 0, 'nil')
        ## The above does not matter at all
        self.isDeathHealthcons = True
        
    def getBands(self):
        ## Entity is dead, so zero bands
        return 0
    
    def publishBandBreak(self):
        ## Cannot publish a band break on this
        pass
    
    def displayHealth(self, normalizeValue):
        return normalize("[^, ^, ^]", normalizeValue)

## A Card Location! 
class cardLocation():
    def __init__(self, name):
        self.name = name
        self.array = []

    def niceName(self):
        return self.name.title()

    def length(self):
        return len(self.array)

    def lengthExcludingFeathery(self):
        count = 0
        for card in self.array:
            if tk.checkTokensOnThis(card, [tk.feathery()]) == False:
                count += 1
        return count

    def getName(self):
        return self.name
    
    def append(self, item):
        self.array.append(item)
        
    def clear(self):
        self.array.clear()
    
    def isEmpty(self):
        return (len(self.array) == 0)
    
    def indexErrorHandler(self, index, functionName):
        if (index > len(self.array)):
            text = " ERROR: " + self.name + " had an unchecked " 
            text += functionName + "() called---there are no Cards at index " + str(index) + "!!! "
            input(text)
            return False
        return True

    ## Pops Cards (default behavior removes the Card at the TOP of the location)
    def pop(self, index = 0):
        self.indexErrorHandler(index, "pop")
        return self.array.pop(index)
    
    def at(self, index):
        self.indexErrorHandler(index, "at")
        return self.array[index]
        
    def insert(self, index, card):
        self.array.insert(index, card)
        
    def shuffle(self):
        random.shuffle(self.array)

    def reverse(self):
        otherList = []
        while len(self.array) > 0:
            otherList.insert(0, self.array.pop())

        while len(otherList) > 0:
            self.array.append(otherList.pop())

    def shuffleTriggeredByDraw(self):
        topDraw = cardLocation("")
        unsetDraw = cardLocation("")
        bottomDraw = cardLocation("")
        muck = cardLocation("")

        self.shuffle()

        for card in self.array:
            if card.reshuffleLocation == "Draw":
                unsetDraw.append(card)
            elif card.reshuffleLocation == "Top":
                topDraw.append(card)
            elif card.reshuffleLocation == "Bottom":
                bottomDraw.append(card)
            elif card.reshuffleLocation == "Muck":
                muck.append(card)
            elif card.reshuffleLocation == "Into Hand":
                self.intoHand.append(card)
            elif card.reshuffleLocation == "Discard":
                self.discard.append(card)
            else:
                input("ERROR!")
                input(str(card.name) + " has no valid reshuffle location!")

        self.array.clear()

        ## Adds Cards to deck
        for card in topDraw.getArray():
            self.array.append(card)
        for card in unsetDraw.getArray():
            self.array.append(card)
        for card in muck.getArray():
            self.array.append(card)
        for card in bottomDraw.getArray():
            self.array.append(card)

    def getArray(self):
        return self.array

## Combines two card locations into a new one
def unionCardLocations(location1, location2, name = 'DEFAULT'):
    if name == 'DEFAULT':
        name = location1.name + " and " + location2.name

    unionCardLocation = cardLocation(name)
    for card in location1.array + location2.array:
        unionCardLocation.append(card)

    return unionCardLocation
