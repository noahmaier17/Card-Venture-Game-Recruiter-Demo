## Allows for a nice way to display Cards

import os, random, re
from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import helper as h, mainVisuals as vis, getCardsByTable as gcbt

def code():
    PAD = 37
    ## Change distDisplay to view the distribution numbers when adding new cards*

    RANDOM_ORDERING = False
    ALL_TABLES = True           ## Overwrite on TABLES, but observes EXCLUDE_TABLE
    ONLY_SHELLS = False
    INCLUDE_CONDITIONS = True

    TABLES = []
    #TABLES.append("Fundamental")

    #TABLES.append("Fruit-Bearing Monks")
    #TABLES.append("Fallow Farmland")
    #TABLES.append("New Bear Order")
    #TABLES.append("Bandits of the Highway")
    #TABLES.append("Copper Croppers")
    #TABLES.append("Horse Hostelry")
    TABLES.append("Apple Orchard Hollow")
    #TABLES.append("Rubble-Dwellers")
    #TABLES.append("The Pier")
    #TABLES.append("Cattle Caste System")
    #TABLES.append("Shop")

    #TABLES.append("Packing Bot")
    #TABLES.append("Graverobber")

    #TABLES.append("Enemy")
    #TABLES.append("Enemy Card Pool")

    EXCLUDE_TABLES = []
    #EXCLUDE_TABLES.append("Enemy")
    #EXCLUDE_TABLES.append("Debug")
    #EXCLUDE_TABLES.append("Packing Bot")
    #EXCLUDE_TABLES.append("Graverobber")

    def anycase(text):
        anycase = ""
        for letter in text:
            anycase += "[" + letter.upper() + letter + "]"
        return anycase

    ## +X Card(s)
    textConditions = []
    #textConditions.append("\+(\\d)+ Card[(s)(\\W)]")
    #textConditions.append("Pocket this")
    #textConditions.append(anycase("Chance"))
    #textConditions.append("0.[0-9]+ Chance")
    ## +(2 through 9) Cards
    #textConditions.append("\+([2-9])+ Card[(s)(\\W)]")
    #textConditions.append("Copy")
    #textConditions.append("Subsequent")
    #textConditions.append("(@)|(Turn End)")
    #textConditions.append("\^")
    #textConditions.append(anycase("Break a Band"))
    #textConditions.append("~")
    #textConditions.append("1\+ Action")
    #textConditions.append("([0-9]+x)|(x[0-9]+)")
    textConditions.append(anycase("At Turn End"))

    nameConditions = []
    #nameConditions.append("In-Ruins")

    if not INCLUDE_CONDITIONS:
        textConditions = []
        nameConditions = []

    os.system('cls')
            
    text = "  Searched Locations:  "
    csv = ""
    if ALL_TABLES:
        text += "ALL TABLES"
    else:
        firstAdd = True
        for location in TABLES:
            if location not in EXCLUDE_TABLES:
                if not firstAdd:
                    text += ",  "
                firstAdd = False
                text += location
    
    print(text)
    string = text
    
    print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
    string = "-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n"
    
    ONLY_SPECIFIC_TABLES = not ALL_TABLES
    
    count = 0
    print("  " + h.normalize(" -- CARD NAME -- ", PAD - 3) + "|     -- TEXT --")
    
    string += "  " + h.normalize(" -- CARD NAME -- ", PAD - 3) + "|     -- TEXT --\n"
    
    allCards = []
    if ONLY_SHELLS:
        allCards = gcbt.getAllCards_includingWIP(excludeNonShells=True)
    else:
        allCards = gcbt.getAllCards_includingWIP()

    if RANDOM_ORDERING:
        random.shuffle(allCards)

    matchingCardsArray = []
    for child in allCards:
        if (any(i in child.table for i in TABLES) and not(any(i in child.table for i in EXCLUDE_TABLES))) or (not(ONLY_SPECIFIC_TABLES) and not(any(i in child.table for i in EXCLUDE_TABLES))):
            matchAllConditions = True
            for condition in textConditions:
                colorlessBodyText = child.niceBodyText(0, 99999, supressedTypes = [], noColor = True)
                if not re.search(condition, colorlessBodyText):
                    matchAllConditions = False
            for condition in nameConditions:
                if not re.search(condition, child.name):
                    matchAllConditions = False

            if not matchAllConditions:
                continue

            matchingCardsArray.append(child)
            '''
            print("  " + h.normalize(child().nameWithTokens(), PAD) + ":  " + child().niceBodyText(PAD + 5, h.WIDTH, supressedTypes = []))
            '''

            string += "  " + h.normalize(child.nameWithTokens(), PAD) + ":  " + child.niceBodyText(PAD + 5, h.WIDTH, supressedTypes = [], noColor = True) + "\n"
            
            count += 1
            
            text = "  " + h.normalize("", PAD) + "."
            '''
            print(text)
            '''
            string += text + "\n"
            
            csv += (child.name + ";;; " 
                    + child.niceBodyText(0, 99999, supressedTypes = [], noColor = True).replace("\n", "\n ;;; ") + ";;; "
                    + str(child.table)
                    + "\n")

    vis.printLocation(matchingCardsArray, 0, Back.CYAN, [], "None")

    print("")
    print(" > Number of valid matches:", count)

    # f = open("Files/Cards.txt", "w")
    # f.write(string + "\n > Number of valid matches: " + str(count))
    # f.close()

    # f = open("Files/CardsCSV.txt", "w")
    # f.write(csv)
    # f.close()

if __name__ == '__main__':
    code()