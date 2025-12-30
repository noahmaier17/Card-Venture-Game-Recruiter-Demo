from colorama import Back, Fore, Style, init

init(autoreset=True)
from typing import TYPE_CHECKING

from Dinosaur_Venture import helper as h
from Dinosaur_Venture import main_visuals as vis

if TYPE_CHECKING:
    from Dinosaur_Venture import clearing as clr
    from Dinosaur_Venture.entities import entity as e

def setupEntityAndCardNames():
    from Dinosaur_Venture import get_cards_by_table as gcbt
    from Dinosaur_Venture.entities import entity as e
    cardNames = gcbt.getMapOfCardNames()
    entityNames = {}
    for child in e.Entity.__subclasses__():
        for subChild in child.__subclasses__():
            entityNames.update({subChild().name.lower(): subChild().text})
    return (entityNames, cardNames)

## Starts a round against some enemies.
## Returns NOTHING.
def startRound(dino: "e.Entity", enemies: "e.Entity"):
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
def dinoTurnStart(dino: "e.Entity", enemies: "e.Entity"):
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
def dinoPlayCard(
    dino: "e.Entity", 
    enemies: "e.Entity",
    roundCount: int, 
    clearing: "clr.Clearing", 
    event: str, 
    entityNames: dict, 
    cardNames: dict, 
    scriptedInput=None
) -> None:

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
                                                canPass=True,
                                                scriptedInput=scriptedInput)

        print(pick)

        if pick != "pass":
            passedInVisuals = vis.prefabPrintDinoTurn(dino, enemies, roundCount, clearing, entityNames, cardNames, event, extraSuppressedTypes = extraSuppressedTypes)

            # Are we playing from the Pocket or from Hand?
            if pick <= dino.pocket.length():
                dino.playCard(dino.pocket, pick - 1, dino, dino, enemies, passedInVisuals, scriptedInput=scriptedInput)
            else:
                dino.playCard(dino.hand, pick - 1 - dino.pocket.length(), dino, dino, enemies, passedInVisuals, scriptedInput=scriptedInput)

            for enemy in enemies:
                enemy.atTriggerDinoPlayedCard(dino, enemies)
        else:
            event = "Dino Turn End"
    return (event,)

def dinoPackingCard(
    dino: "e.Entity", 
    enemies: "e.Entity",
    roundCount: int, 
    clearing: "clr.Clearing", 
    event: str, 
    entityNames: dict, 
    cardNames: dict, 
    scriptedInput=None
) -> None:

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
                                                canPass=True,
                                                scriptedInput=scriptedInput)

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
                                passedInVisuals,
                                scriptedInput=scriptedInput)
            else:
                dino.packCard(dino.hand, 
                                pick - 1 - dino.pocket.length(), 
                                dino, 
                                dino, 
                                enemies,
                                passedInVisuals,
                                scriptedInput=scriptedInput)
        else:
            break
    
    for card in dino.getLocations():
        card.revealed = False

    return (event,)