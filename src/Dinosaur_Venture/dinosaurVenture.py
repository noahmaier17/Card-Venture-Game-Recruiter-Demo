import math, random, os, webbrowser
from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import entity as e, helper as h, mainVisuals as vis, clearing as clr, getCardsByTable as gcbt, react as r, gameplayLogging as log
## from Dino_Cards_Depot import GeneralDinoCards as gdc

## STARTING VARIABLES FOR NEW GAME
event = "Initialize Round"
skipRoundZeroRestStop = True
roundCount = -1
enemies = []
possibleClearings = []
clearing = None
roundDifficultyCreep = 3.50 + 0.5 - 0.5 - 0.25 + 2.10 + 1.10 + 0.75 - 0.75
lootTable = h.cardLocation("loot table")
difficulty = 10 + 8 - roundDifficultyCreep

DIFFICULTY_DEBUG_BONUS = 0
NUMBER_OF_CARDS_TO_LOOT = 4

setOfAllWoods = []
for neck in clr.NeckOfTheWoods.__subclasses__():
    if neck().include:
        setOfAllWoods.append(neck())

neckOfTheWoods = None
clearingsAvailable = []

WIDTH = h.WIDTH

## webbrowser.open('https://www.youtube.com/watch?v=xNN7iTA57jM&t=291s&ab_channel=TheGuildofAmbience')

## ----- PICK PLAYER -----
characters = [
    e.Rover(),
    e.Graverobber()
]

preamble = []
preamble.append(" WELCOME TO THE DINSAUR VENTURE")

for i in range(len(characters)):
    character = characters[i]
    preamble.append(str(i + 1) + ": '" + character.name + "'")
value = h.pickValue("Pick a Character", range(1, len(characters) + 1), preamble = preamble) - 1

dino = characters[value]

## -- Does intensive remaining set up --

shopLocation = gcbt.getCardsByTable(["Shop"], locationName = "Shop Cards")
randomTier1Location = gcbt.getCardsByTable(gcbt.TIER_1_TABLES, locationName = "Tier 1 Cards")
allDebuffs = gcbt.getCardsByTable(["Debuffs"], locationName = "Debuffs")

for card in randomTier1Location.getArray():
    if not card.isShellCard:
        for i in range(2):
            debuff = allDebuffs.at(random.randint(0, allDebuffs.length() - 1))
            debuff.onLootedEnshelling(dino, card)

cardNames = gcbt.getMapOfCardNames()
entityNames = {}
for child in e.Entity.__subclasses__():
    for subChild in child.__subclasses__():
        entityNames.update({subChild().name.lower(): subChild().text})



DEBUG_TRUE = True
DEBUG_FALSE = False
## ----- DEBUGGING -----
DO_ROUND_1_LOOTING = False
NUKE_DINO_DECK = False
DEBUG_DINO_DECK = False
##              --> Nukes Dino Deck anyways
SKIP_SHOP_DEBUG = False
LOOT_SHELLS_ONLY = False

SKIP_PICKING_CLEARINGS = False
#DIFFICULTY_DEBUG_BONUS = -1000
#NUMBER_OF_CARDS_TO_LOOT = 999
#setOfAllWoods = [clr.ThePier()]
#shopLocation = h.cardLocation("")
#for card in [gcbt.getCardByName("Bolster")]: shopLocation.append(card)

possible_heirlooms = ["Shop"]

## -----


if NUKE_DINO_DECK or DEBUG_DINO_DECK:
    dino.deck = h.cardLocation("deck")
if DEBUG_DINO_DECK:
    '''
    testCard = gcbt.getCardByName("Forklift Certificate")
    testCard.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("+2 Actions.", cf.plusXActions(2)),
                          belowThrowTextWrapper = cf.shellTextWrapper("+2 Actions.", cf.plusXActions(2)))
    dino.deck.append(testCard)
    '''
    dino.deck.append(gcbt.getCardByName("Junk"))

difficulty += DIFFICULTY_DEBUG_BONUS
if difficulty <= 0:
    print(Fore.RED + " CLEARING DIFFICULTY IS A NEGATIVE VALUE!")
    print(Fore.RED + " CLEARING DIFFICULTY IS A NEGATIVE VALUE!")
    print(Fore.RED + " CLEARING DIFFICULTY IS A NEGATIVE VALUE!")
    input(" ... ")

difficulty += DIFFICULTY_DEBUG_BONUS

if DO_ROUND_1_LOOTING:
    skipRoundZeroRestStop = False

## h.selectCard(dino, "Hierloom", 0, [randomTier1Location], [4], lootVacuously = True, canPass = True, activateAbilityOnPass = True)
notFirstNeckOfTheWoods = True
guarenteedClearing = None
if not SKIP_PICKING_CLEARINGS:
    woodsPreamble = []
    for index, wood in enumerate(setOfAllWoods):
        woodsPreamble.append(str(index + 1) + ": '" + wood.name + "'")
    print("")
    guarenteedClearingIndex = h.pickValue("Pick a guarenteed Neck of the Woods", range(1, len(setOfAllWoods) + 1), preamble = woodsPreamble) - 1
    guarenteedClearing = setOfAllWoods.pop(guarenteedClearingIndex)

## Creates a new log file instance
log.newLogFile()

while True:
    log.currentEventLog(event)

    if event == "Initialize Round":
        ## Uptick difficulty 
        difficulty += roundDifficultyCreep
        
        ## ----- DISPLAY CODE -----
        os.system('cls')
        roundCount += 1
                    
        ## ----- Rest Stop -----
        if roundCount % 2 == 0:
            ## Upticks reset values
            dino.resetR += dino.uptickResetR
            dino.resetG += dino.uptickResetG
            dino.resetB += dino.uptickResetB
        
            ## Heals back to values
            if dino.hp.isDeathHealthcons == True:
                dino.hp = ""
                dino.hp = h.healthcons(dino.healR, dino.healG, dino.healB, 'nil')
                dino.dead = False
            
            dino.hp.r = dino.resetR
            dino.hp.g = dino.resetG
            dino.hp.b = dino.resetB
        
            if not skipRoundZeroRestStop:
                ## Looting of Clearing
                h.selectCard(dino, clearing.name, roundCount, [lootTable], [NUMBER_OF_CARDS_TO_LOOT], canPass = True, activateAbilityOnPass = True)

            skipRoundZeroRestStop = False

            if not SKIP_SHOP_DEBUG and roundCount % 4 == 0:
                ## Looting of Shop
                if dino.skipNextShop:
                    h.splash("'" + dino.name + "' must skip this shop...")
                    dino.skipNextShop = False
                else:
                    h.selectCard(dino, "Shop", 0, [shopLocation, randomTier1Location], [4, 0], lootVacuously = True, canPass = True, activateAbilityOnPass = True)

            ## ----- End of Rest Stop Triggers -----
            for card in dino.deck.getArray():
                card.atTriggerEndOfRestStop(dino)

            ## Clears screen
            os.system('cls')

            ## Sets dino looting back to as it should be
            dino.looting += dino.uptickLooting

        ## ----- New Neck of the Woods -----
        if roundCount % 4 == 0:
            ## ----- Pick Neck of the Woods Clearing -----
            ## print(" The Wilderness beckons towards... ")

            while len(clearingsAvailable) < 2 and len(setOfAllWoods) > 0:
                if notFirstNeckOfTheWoods and guarenteedClearing != None:
                    clearingsAvailable.append(guarenteedClearing)
                    notFirstNeckOfTheWoods = False

                random.shuffle(setOfAllWoods)
                clearingsAvailable.append(setOfAllWoods.pop())

            clr.printClearings(clearingsAvailable, roundCount)

            if SKIP_PICKING_CLEARINGS:
                pick = 0
            else:
                pick = h.pickValue("Pick a Direction", range(1, len(clearingsAvailable) + 1))
            neckOfTheWoods = clearingsAvailable.pop(pick - 1)

            ## Adds to the loot table Cards for looting
            lootTable = h.cardLocation("loot table")
            setOfCards = []
            if LOOT_SHELLS_ONLY:
                setOfCards = gcbt.getDinoShellCards()
            else:
                setOfCards = gcbt.getDinoCards() + gcbt.getDinoShellCards()
            for card in setOfCards:
                if neckOfTheWoods.name in card().table:
                    lootTable.append(card())
            lootTable.shuffle()

            ## Sets the clearing
            clearing = neckOfTheWoods.clearing

        event = "Populate Clearing"

    elif event == "Populate Clearing":
        clearing.populate(difficulty)
        enemies = clearing.enemies
        event = "Start Round"

    elif event == "Start Round":
        os.system('cls')
        dino.roundStart()

        ## ----- Round Start Window -----
        for card in dino.getLocations():
            card.atTriggerRoundStart(dino, dino, enemies, vis.prefabEmpty())

        for i in range(len(enemies)):
            enemies[i].roundStart()
            enemies[i].index = i

            ## ----- Round Start Window -----
            for card in enemies[i].getLocations():
                card.atTriggerRoundStart(enemies[i], dino, enemies, vis.prefabEmpty())
        event = "Dino Turn Start"

    elif event == "Dino Turn Start":
        os.system('cls')
        dino.turnStart()

        while (dino.intoHand.length() > 0):
            dino.hand.append(dino.intoHand.pop())
        
        while (dino.intoIntoHand.length() > 0):
            dino.intoHand.append(dino.intoIntoHand.pop())
            
        for card in dino.play.getArray():
            card.atTriggerTurnStart(dino, dino, enemies)
        
        ## -- UNPACKING ABILITIES -- 
        while True:
            break
            ## This is outdated (before Pocket Mat), so copy and paste the lower code to implement
        
        for card in dino.hand.getArray():
            card.revealed = False

        ## ----- Actionable Code for Turn Start ------
        dino.atTriggerTurnStart(dino, enemies)

        event = "Dino Play Card"

    elif event == "Dino Play Card":   
        ## ----- Checks if Dino may still play cards, otherwise becomes enemy turns -----
        if dino.actions == 0:
            event = "Dino Turn End"
        else:
            extraSupressedTypes = ["looting", "round start"]
            vis.printDinoTurn(dino, enemies, roundCount, clearing, event, extraSupressedTypes = extraSupressedTypes)
            
            ## ----- Actionable Code -----
            while True:
                pick = input(vis.eventText(event) + "(Clear), (Pass), [Input Noun], or Play a " 
                    + Fore.GREEN + "Card" + Fore.WHITE 
                    + " [" + Fore.CYAN + "Actions" + Fore.WHITE + ": " 
                    + vis.rainbowNormalize(dino.actions, len(str(dino.actions))) + "]: ")
                try:
                    pick = int(pick)
                    if (pick <= 0 or pick > dino.hand.length() + dino.pocket.length()):
                        print(" INVALID PICK ")
                    else:
                        break
                except ValueError:
                    if pick.lower() == "pass":
                        break
                    elif pick.lower().strip() in entityNames.keys() and pick != "":
                        h.splash(entityNames[pick.lower().strip()], printInsteadOfInput = True)
                    elif pick.lower().strip() in cardNames.keys() and pick != "":
                        key = pick.lower().strip()
                        print("    " + Back.CYAN + Style.BRIGHT + " " + cardNames[key].name + " ")
                        print(h.normalize("", 3) + cardNames[key].niceBodyText(3, WIDTH, supressedTypes = []))
                    elif pick.lower() == "clear":
                        vis.printDinoTurn(dino, enemies, roundCount, clearing, event, extraSupressedTypes = extraSupressedTypes)
                    else:
                        print(vis.eventText(event) + "INVALID INPUT ")

            if pick != "pass":
                passedInVisuals = vis.prefabPrintDinoTurn(dino, enemies, roundCount, clearing, entityNames, cardNames, event, extraSupressedTypes = extraSupressedTypes)

                ## -- Are we playing from the Pocket or from Hand? --
                if pick <= dino.pocket.length():
                    dino.playCard(dino.pocket, pick - 1, dino, dino, enemies, passedInVisuals)
                else:
                    dino.playCard(dino.hand, pick - 1 - dino.pocket.length(), dino, dino, enemies, passedInVisuals)

                for enemy in enemies:
                    enemy.atTriggerDinoPlayedCard(dino, enemies)
            else:
                event = "Dino Turn End"

    elif event == "Dino Turn End":
        ## -- PACKING ABILITIES -- 
        while True:
            hasPackingCard = False
            
            ## ----- Finds all Cards that have yet to be revealed with Padcking abilities -----
            revealPicksIndexes = []
            
            for i in range(dino.pocket.length()):
                card = dino.pocket.at(i)
                if card.hasPackingAbility and not(card.revealed):
                    hasPackingCard = True
                    revealPicksIndexes.append(i + 1)
            for i in range(dino.hand.length()):
                card = dino.hand.at(i)
                if card.hasPackingAbility and not(card.revealed):
                    hasPackingCard = True
                    revealPicksIndexes.append(dino.pocket.length() + i + 1)
            
            ## ----- Leaves if there are no such Cards -----
            if not(hasPackingCard):
                break
            
            extraSupressedTypes = ["looting", "core", "{}", "revealed", "round start"]
            vis.printDinoTurn(dino, enemies, roundCount, clearing, event, extraSupressedTypes = extraSupressedTypes)
            
            while True:
                pick = input(vis.eventText(event) + "(Clear), (Pass), [Input Noun], or Pack a " + Fore.GREEN + "Card" + Fore.WHITE + ": ")
                try:
                    pick = int(pick)
                    if (pick not in revealPicksIndexes):
                        print(" INVALID PICK ")
                    else:
                        break
                except ValueError:
                    if pick.lower() == "pass":
                        break
                    elif pick.lower().strip() in entityNames.keys() and pick != "":
                        h.splash(entityNames[pick.lower().strip()], printInsteadOfInput = True)
                    elif pick.lower().strip() in cardNames.keys() and pick != "":
                        key = pick.lower().strip()
                        print("    " + Back.CYAN + Style.BRIGHT + " " + cardNames[key].name + " ")
                        print(h.normalize("", 3) + cardNames[key].niceBodyText(3, WIDTH, supressedTypes = []))
                    elif pick.lower() == "clear":
                        vis.printDinoTurn(dino, enemies, roundCount, clearing, event, extraSupressedTypes = extraSupressedTypes)
                    else:
                        print(vis.eventText(event) + "INVALID INPUT ")

            if pick != "pass":
                ## -- Are we playing from the Pocket or from Hand? --
                passedInVisuals = vis.prefabPrintDinoTurn(dino, enemies, roundCount, clearing, entityNames, cardNames, event, extraSupressedTypes = extraSupressedTypes)

                if pick <= dino.pocket.length():
                    dino.packCard(dino.pocket, pick - 1, dino, dino, enemies, passedInVisuals)
                else:
                    dino.packCard(dino.hand, pick - 1 - dino.pocket.length(), dino, dino, enemies, passedInVisuals)
            else:
                break
        
        for card in dino.getLocations():
            card.revealed = False

        ## -------- Reaction Window --------
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.AtTurnEnd(), r.DinoTurn()])
        ])
        extraSupressedTypes = ["looting", "core", "{}", "revealed", "round start"]
        passedInVisuals = vis.prefabPrintDinoTurn(dino, enemies, roundCount, clearing, entityNames, cardNames, event, extraSupressedTypes = extraSupressedTypes)
        r.reactionStack.react(dino, enemies, passedInVisuals)

        dino.turnEndTidying(dino, enemies, passedInVisuals)

        ## ----- Reset Card States -----
        for card in dino.deck.getArray():
            card.resetCardState_TurnEnd()

        ## ----- Check if all enemies are dead -----
        allDead = True
        for enemy in enemies:
            if enemy.dead == False:
                allDead = False
        
        if allDead:
            h.splash(" Cleared Clearing! ")
            event = "Round End"
        else:        
            dino.dinoTurnDinoDeathCheck(roundCount)
            if dino.takeAnotherTurnQuery():
                event = "Dino Turn Start"
            else:
                event = "Enemy Turn"
    
    elif event == "Enemy Turn":
        enemyIndex = 0
        while enemyIndex < len(enemies):
            enemy = enemies[enemyIndex]
            os.system('cls')
            unfinishedWithEnemyFlag = True
            ## ----- Checks if already finished -----
            if enemy.dead == True and enemy.deadCardPlays == False:
                unfinishedWithEnemyFlag = False
            
            ## ----- During Turn -----
            while unfinishedWithEnemyFlag:
                vis.printEnemyTurn(enemy, dino, enemies, roundCount, clearing, enemyIndex, event)
                ## ----- Enemy Turn Start -----
                enemy.turnStart()
                
                for card in enemy.play.getArray():
                    card.atTriggerTurnStart(enemy, dino, enemies)
            
                ## ----- Enemy Play Cards -----
                # Checks if the enemy can even play any cards
                playedAnyCards = False
                while unfinishedWithEnemyFlag:
                    if enemy.dead == True and enemy.deadCardPlays == False:
                        unfinishedWithEnemyFlag = False
                    elif enemy.hand.length() == 0 and playedAnyCards == False:
                        h.splash("Hand is empty, so it cannot play any Cards.")
                        unfinishedWithEnemyFlag = False
                    elif enemy.actions == 0 and playedAnyCards == False:
                        h.splash("Enemy has no Actions, so it cannot play any Cards.")
                        unfinishedWithEnemyFlag = False
                    elif enemy.actions == 0 or enemy.hand.length() == 0: 
                        unfinishedWithEnemyFlag = False
                    else:

                        cardIndex = enemy.cardIntellect()
                        if cardIndex != "nil":
                            card = enemy.hand.at(cardIndex)
                            # print(" Resolution of: " + Back.RED + Fore.BLACK + " " + card.name + " ")
                            # print("  > " + card.niceBodyText(3, WIDTH))

                            passedInVisuals = vis.prefabPrintEnemyTurn(enemy, dino, enemies, roundCount, clearing, enemyIndex, event, entityNames, cardNames)
                            enemy.playCard(enemy.hand, cardIndex, enemy, dino, enemies, passedInVisuals = passedInVisuals)
                            playedAnyCards = True
                            input(" ... ")
                            print("")
                        else:
                            unfinishedWithEnemyFlag = False

            ## ----- End Of Turn -----
            if enemy.dead == False:
                enemy.atTriggerTurnEnd(dino, enemies)
            
                enemy.turnEndTidying(dino, enemies, passedInVisuals)
                
                dino.enemyTurnDinoDeathCheck(roundCount)

            if enemy.takeAnotherTurnQuery():
                pass
            else:
                enemyIndex += 1

        event = "Turn End"
    
    elif event == "Turn End":
        ## ----- Check for Unlocks [[ by turn ]] -----
        '''
        updateMap = {}
        for enemy in enemies:
            if enemy.initialEnemyName == "Shrew" and enemy.diedThisTurn == True:
                h.plusDict(updateMap, "Shrews Dead", 1)
        
        if h.dictContainsAtLeast(updateMap, "Shrews Dead", 3):
            h.saveUpdate("save.txt", "Unlocked_Belly_Filled_Shrew", True,
                "Belly-Filled Shrew!")
        
        h.saveUpdate("save.txt", "Unlocked_Hungry_Wolf", True, 
                "Hungry Wolf Player!")
        '''
        
        event = "Dino Turn Start"

    elif event == "Round End":
        ## ----- Check for Unlocks [[ BY ROUND BY ROUND BY ROUND ]] -----


        ## ----- Resets Variables -----
        dino.roundEndTidying()
        
        ## ----- New Round -----
        event = "Initialize Round"













