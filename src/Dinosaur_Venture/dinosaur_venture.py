"""
dinosaur_venture.py

The main file of the program where all the logic is run.

In being the very first thing I programmed, some of the logic could use some significant work.
IE, handling each event with a string value could be replaced with something more robust.
Moreover, some of the logic could be better factored out, which I have begun to do with the
gameplayLoopEvents.py file.
"""

import os
import random
from typing import TYPE_CHECKING

from colorama import Back, Fore, Style, init

from Dinosaur_Venture.entities import dinoes

init(autoreset=True) 
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import clearing as clr
from Dinosaur_Venture import gameplay_logging as log
from Dinosaur_Venture import gameplayLoopEvents as gameEvent
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis
from Dinosaur_Venture import react as r

if TYPE_CHECKING:
    from Dinosaur_Venture.entities import entity as e

def code():
    ## ----- Starting Variables -----
    # Whatever current event we are at; main logic driver
    event: str = "Initialize Round"

    # If we are going to skip the 0th Rest Stop
    skipRoundZeroRestStop: bool = True

    # Round count
    roundCount: int = -1

    # List of all enemies
    enemies: list[e.Entity] = []
    
    # The current clearing
    clearing: clr.Clearing = None

    # How much to increase difficulty across each round
    # Gets modified a lot which is why there are so many numbers here
    roundDifficultyCreep: int = 3.50 + 0.5 - 0.5 - 0.25 + 2.10 + 1.10 + 0.75 - 0.75

    # Stores all the loot for this clearing
    lootTable: h.cardLocation = h.cardLocation("loot table")

    # The current difficulty
    # Gets modified a lot which is why there are so many numbers here
    difficulty = 10 + 8 - roundDifficultyCreep

    # Gets a list of all possible places we can traverse
    setOfAllWoods: list[clr.NeckOfTheWoods] = []
    for neck in clr.NeckOfTheWoods.__subclasses__():
        if neck().include:
            setOfAllWoods.append(neck())

    # Current neck of the woods
    neckOfTheWoods: clr.NeckOfTheWoods = None

    # Available clearings from the superset of possible places to traverse
    clearingsAvailable: list[clr.NeckOfTheWoods] = []

    # List of all playable characters
    characters: list[e.Entity] = [
        dinoes.Rover(),
        dinoes.Graverobber()
    ]

    # No longer used
    # possible_heirlooms: h.cardLocation = ["Shop"]

    # I use to automatically play nature sounds via webbrowser when the game is played
    ## webbrowser.open('https://www.youtube.com/watch?v=xNN7iTA57jM&t=291s&ab_channel=TheGuildofAmbience')

    ## ----- Pick your Player -----
    preamble = []
    preamble.append(" WELCOME TO THE DINSAUR VENTURE")

    for i in range(len(characters)):
        character = characters[i]
        preamble.append(str(i + 1) + ": '" + character.name + "'")
    value = h.pickValue("Pick a Character", range(1, len(characters) + 1), preamble = preamble) - 1

    # The player's entity
    dino: e.Entity = characters[value]

    ## ----- Does intensive remaining set up -----
    # List of all shop cards
    shopLocation: h.cardLocation = gcbt.getCardsByTable(["Shop"], 
                                                        locationName = "Shop Cards")
    # Set of random tier-1 cards (which will get debuffed)
    randomTier1Location: h.cardLocation = gcbt.getCardsByTable(gcbt.TIER_1_TABLES, 
                                                               locationName = "Tier 1 Cards")
    # Card debuffs
    allDebuffs: h.cardLocation = gcbt.getCardsByTable(["Debuffs"], 
                                                      locationName = "Debuffs")

    # Modifies all the random tier-1 cards to have debuffs
    for card in randomTier1Location.getArray():
        if not card.isShellCard:
            for i in range(2):
                debuff = allDebuffs.at(random.randint(0, allDebuffs.length() - 1))
                debuff.onLootedEnshelling(dino, card)

    # Gets maps for entities/cards and their description/text
    entityNames, cardNames = gameEvent.setupEntityAndCardNames()

    ## ----- Debugging Values ----
    ## For all booleans, the non-debugging value is False

    # For debugging, if we want to increase/decrease the difficulty
    # Non-debugging value: 0
    DIFFICULTY_DEBUG_BONUS = 0

    # For debugging, if we want to loot more cards at a Rest Stop
    # Non-debugging value: 4
    NUMBER_OF_CARDS_TO_LOOT = 4

    ## If we will loot round 1; useful for faster testing speed
    DO_ROUND_1_LOOTING = False

    # To replace all of dino's deck with nothing
    NUKE_DINO_DECK = False

    # To replace dino's deck with the special debugging deck (see below)
    DEBUG_DINO_DECK = False

    # Skips every shop for the purpose of debugging; useful for faster testing speed
    SKIP_SHOP_DEBUG = False

    # Only loot shells
    LOOT_SHELLS_ONLY = False

    # Skip picking clearings; useful for faster testing speed
    SKIP_PICKING_CLEARINGS = False

    # To replace the shop cards, uncomment the following and add cards as you please
    # shopLocation = h.cardLocation("")
    # for card in [gcbt.getCardByName("Bolster")]: shopLocation.append(card)

    ## ----- Performs Debugging Actions -----
    if NUKE_DINO_DECK or DEBUG_DINO_DECK:
        dino.deck = h.cardLocation("deck")

    # If DEBUG_DINO_DECK == True, replaces dino's deck with the following cards
    if DEBUG_DINO_DECK:
        '''
        testCard = gcbt.getCardByName("Forklift Certificate")
        testCard.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("+2 Actions.", cf.plusXActions(2)),
                            belowThrowTextWrapper = cf.shellTextWrapper("+2 Actions.", cf.plusXActions(2)))
        dino.deck.append(testCard)

        dino.deck.append(gcbt.getCardByName("Time in a Bottle"))
        card = gcbt.getCardByName("Fish Fry")
        gcbt.getCardByName("//shell// In-Ruins").onLootedEnshelling(dino, card)
        dino.deck.append(card)
        '''

        dino.deck.append(gcbt.getCardByName("MEGA Damage"))
        dino.deck.append(gcbt.getCardByName("MEGA Damage"))
        dino.deck.append(gcbt.getCardByName("MEGA Damage"))
        dino.deck.append(gcbt.getCardByName("Twig!"))
        dino.deck.append(gcbt.getCardByName("Twig!"))
        dino.deck.append(gcbt.getCardByName("Twig!"))

    difficulty += DIFFICULTY_DEBUG_BONUS
    if difficulty <= 0:
        print(Fore.RED + " CLEARING DIFFICULTY IS A NEGATIVE VALUE!")
        print(Fore.RED + " CLEARING DIFFICULTY IS A NEGATIVE VALUE!")
        print(Fore.RED + " CLEARING DIFFICULTY IS A NEGATIVE VALUE!")
        input(" ... ")

    difficulty += DIFFICULTY_DEBUG_BONUS

    if DO_ROUND_1_LOOTING:
        skipRoundZeroRestStop = False

    ## ----- Remaining Preparation Logic -----
    # Commented out line is for picking a special card to start with (possible later feature)
    # h.selectCard(dino, "Hierloom", 0, [randomTier1Location], [4], lootVacuously = True, canPass = True, activateAbilityOnPass = True)

    # Logic for picking a guarenteed location
    notFirstNeckOfTheWoods = True
    guarenteedClearing = None
    if not SKIP_PICKING_CLEARINGS:
        woodsPreamble = []
        for index, wood in enumerate(setOfAllWoods):
            woodsPreamble.append(str(index + 1) + ": '" + wood.name + "'")
        print("")
        guarenteedClearingIndex = h.pickValue("Pick a guarenteed Neck of the Woods", 
                                              range(1, len(setOfAllWoods) + 1), 
                                              preamble=woodsPreamble) - 1
        guarenteedClearing = setOfAllWoods.pop(guarenteedClearingIndex)

    # Creates a new log file instance
    log.new_log_file()

    # The below while loop runs the entire game
    while True:
        log.current_event_log(event)

        if event == "Initialize Round":
            """Prepares a Round, doing tasks like looting/buying Cards."""
            ## Uptick difficulty 
            difficulty += roundDifficultyCreep
            
            ## ----- DISPLAY CODE -----
            os.system('cls')
            roundCount += 1
                        
            ## ----- Rest Stop -----
            if roundCount % 2 == 0:
                # Upticks reset values
                dino.resetR += dino.uptickResetR
                dino.resetG += dino.uptickResetG
                dino.resetB += dino.uptickResetB
            
                # Heals back to values
                if dino.hp.isDeathHealthcons == True:
                    dino.hp = ""
                    dino.hp = cll.Healthcons(dino.healR, dino.healG, dino.healB, 'nil')
                    dino.dead = False
                
                dino.hp.r = dino.resetR
                dino.hp.g = dino.resetG
                dino.hp.b = dino.resetB
            
                # Loots a Clearing
                if not skipRoundZeroRestStop:
                    h.selectCard(dino, 
                                 clearing.name, 
                                 roundCount, 
                                 [lootTable], 
                                 [NUMBER_OF_CARDS_TO_LOOT], 
                                 canPass=True,
                                 activateAbilityOnPass=True)

                skipRoundZeroRestStop = False

                # Buy from a Shop
                if not SKIP_SHOP_DEBUG and roundCount % 4 == 0:
                    if dino.skipNextShop:
                        h.splash("'" + dino.name + "' must skip this shop...")
                        dino.skipNextShop = False
                    else:
                        h.selectCard(dino, 
                                     "Shop", 
                                     0, 
                                     [shopLocation, randomTier1Location], 
                                     [4, 0], 
                                     lootVacuously=True, 
                                     canPass=True, 
                                     activateAbilityOnPass=True)

                ## ----- End of Rest Stop Triggers -----
                for card in dino.deck.getArray():
                    card.atTriggerEndOfRestStop(dino)

                # Clears screen
                os.system('cls')

                # Sets dino looting back to as it should be
                dino.looting += dino.uptickLooting

            ## ----- New Neck of the Woods -----
            if roundCount % 4 == 0:
                # ----- Pick Neck of the Woods Clearing -----
                # print(" The Wilderness beckons towards... ")

                # Populates the available clearings
                while len(clearingsAvailable) < 2 and len(setOfAllWoods) > 0:
                    if notFirstNeckOfTheWoods and guarenteedClearing != None:
                        clearingsAvailable.append(guarenteedClearing)
                        notFirstNeckOfTheWoods = False
                    else:
                        random.shuffle(setOfAllWoods)
                        clearingsAvailable.append(setOfAllWoods.pop())

                clr.printClearings(clearingsAvailable, roundCount)

                # For debugging if we want to skip picking (automatically picking the 0th option)
                if SKIP_PICKING_CLEARINGS:
                    pick = 0
                else:
                    pick = h.pickValue("Pick a Direction", range(1, len(clearingsAvailable) + 1))
                neckOfTheWoods = clearingsAvailable.pop(pick - 1)

                # Adds to the loot table Cards for looting
                lootTable = h.cardLocation("loot table")
                setOfCards = []
                if LOOT_SHELLS_ONLY:
                    setOfCards = gcbt.getDinoShellCards()
                else:
                    setOfCards = gcbt.getDinoCards() + gcbt.getDinoShellCards()
                for card in setOfCards:
                    if neckOfTheWoods.name in card.table:
                        lootTable.append(card)
                lootTable.shuffle()

                # Sets the clearing
                clearing = neckOfTheWoods.clearing

            event = "Populate Clearing"

        elif event == "Populate Clearing":
            """Populates a clearing, adding things like the enemies."""
            clearing.populate(difficulty)
            enemies = clearing.enemies
            event = "Start Round"

        elif event == "Start Round":
            """Starts a Round; handled via `gameEvent.startRound()`."""
            os.system('cls')
            gameEvent.startRound(dino, enemies)
            event = "Dino Turn Start"

        elif event == "Dino Turn Start":
            """Handles the start of dino's turn; handled via `gameEvent.dinoTurnStart()`."""
            os.system('cls')
            gameEvent.dinoTurnStart(dino, enemies)
            event = "Dino Play Card"

        elif event == "Dino Play Card":   
            """Handles dino playing a card; handled via `gameEvent.dinoPlayCard()`."""
            returnValues = gameEvent.dinoPlayCard(dino, 
                                                  enemies, 
                                                  roundCount, 
                                                  clearing, 
                                                  event, 
                                                  entityNames, 
                                                  cardNames)
            event = returnValues[0]

        elif event == "Dino Turn End":
            ## ----- PACKING ABILITIES -----
            while True:
                hasPackingCard = False
                
                # Finds all Cards that have yet to be revealed with Packing abilities
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
                
                # Quits if there are no such Cards
                if not(hasPackingCard):
                    break
                
                # Handles UI for the Packing Phase
                extraSuppressedTypes = ["looting", "core", "{}", "revealed", "round start"]
                vis.printDinoTurn(dino, 
                                  enemies, 
                                  roundCount, 
                                  clearing, 
                                  event, 
                                  extraSuppressedTypes=extraSuppressedTypes)

                selectionText = (
                    vis.eventText(event) + "(Clear), (Pass), [Input Noun], or Pack a "
                    + Fore.GREEN + "Card" + Fore.WHITE + ": "
                )
                pick = h.selectCardFromHandAndPocket(revealPicksIndexes, 
                                                     selectionText,
                                                     dino, 
                                                     enemies, 
                                                     roundCount,
                                                     clearing,
                                                     event,
                                                     entityNames,
                                                     cardNames,
                                                     extraSuppressedTypes=extraSuppressedTypes,
                                                     canPass=True)

                if pick != "pass":
                    # Handles visuals
                    passedInVisuals = vis.prefabPrintDinoTurn(dino, 
                                                              enemies, 
                                                              roundCount, 
                                                              clearing,
                                                              entityNames, 
                                                              cardNames, 
                                                              event, 
                                                              extraSuppressedTypes=extraSuppressedTypes)

                    # Are we playing from the Pocket or from Hand?
                    if pick <= dino.pocket.length():
                        dino.packCard(dino.pocket, 
                                      pick - 1, 
                                      dino, 
                                      dino, 
                                      enemies, 
                                      passedInVisuals)
                    else:
                        dino.packCard(dino.hand, 
                                      pick - 1 - dino.pocket.length(), 
                                      dino, 
                                      dino, 
                                      enemies,
                                      passedInVisuals)
                else:
                    break
            
            for card in dino.getLocations():
                card.revealed = False

            ## ----- Reaction Window for Dino Turn End -----
            r.reactionStack = r.reactStack([
                r.reactionWindow([r.AtTurnEnd(), r.DinoTurn()])
            ])
            extraSuppressedTypes = ["looting", "core", "{}", "revealed", "round start"]
            passedInVisuals = vis.prefabPrintDinoTurn(dino, 
                                                      enemies, 
                                                      roundCount, 
                                                      clearing, 
                                                      entityNames, 
                                                      cardNames, 
                                                      event, 
                                                      extraSuppressedTypes=extraSuppressedTypes)
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
            """Each enemy takes their turn(s)."""
            enemyIndex = 0

            # Iterates across all enemies
            while enemyIndex < len(enemies):
                enemy = enemies[enemyIndex]
                os.system('cls')
                unfinishedWithEnemyFlag = True

                ## ----- Checks if this turn is finished already -----
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

                        # Handles all cases where the enemy cannot play a card
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
                            # Picks the card index that the enemy will play
                            cardIndex = enemy.cardIntellect()

                            if cardIndex != "nil":
                                card = enemy.hand.at(cardIndex)

                                # Plays the card
                                passedInVisuals = vis.prefabPrintEnemyTurn(enemy, 
                                                                           dino, 
                                                                           enemies, 
                                                                           roundCount, 
                                                                           clearing, 
                                                                           enemyIndex, 
                                                                           event, 
                                                                           entityNames, 
                                                                           cardNames)
                                enemy.playCard(enemy.hand, 
                                               cardIndex, 
                                               enemy, 
                                               dino, 
                                               enemies, 
                                               passedInVisuals=passedInVisuals)

                                playedAnyCards = True
                                input(" ... ")
                                print("")
                            else:
                                unfinishedWithEnemyFlag = False

                ## ----- End Of Turn -----
                if enemy.dead == False:
                    enemy.atTriggerTurnEnd(dino, enemies)
                
                    enemy.turnEndTidying(dino, enemies, passedInVisuals)
                    
                    dino.enemyTurnDinoDeathCheck()

                if enemy.takeAnotherTurnQuery():
                    pass
                else:
                    enemyIndex += 1

            event = "End of All Enemy Turns"
        
        elif event == "End of All Enemy Turns":
            """Currently does nothing; considered to be used for Unlocks."""
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
            """Handles the end of an entire Round."""
            ## ----- Check for Unlocks [[ BY ROUND BY ROUND BY ROUND ]] -----
            '''Currently not used.'''

            ## ----- Resets Variables -----
            dino.roundEndTidying()
            
            ## ----- New Round -----
            event = "Initialize Round"

if __name__ == '__main__':
    code()