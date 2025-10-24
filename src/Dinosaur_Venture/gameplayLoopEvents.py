from colorama import Back, Fore, Style, init

init(autoreset=True)
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis


def setupEntityAndCardNames():
    from Dinosaur_Venture import getCardsByTable as gcbt
    from Dinosaur_Venture.entities import entity as e
    cardNames = gcbt.getMapOfCardNames()
    entityNames = {}
    for child in e.Entity.__subclasses__():
        for subChild in child.__subclasses__():
            entityNames.update({subChild().name.lower(): subChild().text})
    return (entityNames, cardNames)

## Starts a round against some enemies.
## Returns NOTHING.
def startRound(dino, enemies):
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

## Handles the start of the player's turn.
## Returns NOTHING.
def dinoTurnStart(dino, enemies):
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

## Handles when dino plays a card.
## Returns (event)
def dinoPlayCard(dino, enemies, roundCount, clearing, event, entityNames, cardNames, scriptedInput_dinoPlayCard=None):
    ## ----- Checks if Dino may still play cards, otherwise becomes enemy turns -----
    if dino.actions == 0:
        event = "Dino Turn End"
    else:
        extraSuppressedTypes = ["looting", "round start"]
        vis.printDinoTurn(dino, enemies, roundCount, clearing, event, extraSuppressedTypes=extraSuppressedTypes)
        
        ## ----- Actionable Code -----
        ## Input text string
        selectionText = (vis.eventText(event) + "(Clear), (Pass), [Input Noun], or Play a " 
                + Fore.GREEN + "Card" + Fore.WHITE 
                + " [" + Fore.CYAN + "Actions" + Fore.WHITE + ": " 
                + vis.rainbowNormalize(dino.actions, len(str(dino.actions))) + "]: ")

        if scriptedInput_dinoPlayCard != None:
            print(selectionText) ## We still want to ensure the inputText string is valid, even though it is not useful to print it
            pick = scriptedInput_dinoPlayCard.getNextValue(dino, enemies, roundCount, clearing, event, entityNames, cardNames)

        else:
            revealPicksIndexes = []
            for i in range(dino.hand.length() + dino.pocket.length()):
                revealPicksIndexes.append(i + 1)

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
            passedInVisuals = vis.prefabPrintDinoTurn(dino, enemies, roundCount, clearing, entityNames, cardNames, event, extraSuppressedTypes = extraSuppressedTypes)

            # Are we playing from the Pocket or from Hand?
            if pick <= dino.pocket.length():
                dino.playCard(dino.pocket, pick - 1, dino, dino, enemies, passedInVisuals)
            else:
                dino.playCard(dino.hand, pick - 1 - dino.pocket.length(), dino, dino, enemies, passedInVisuals)

            for enemy in enemies:
                enemy.atTriggerDinoPlayedCard(dino, enemies)
        else:
            event = "Dino Turn End"
    return (event,)
