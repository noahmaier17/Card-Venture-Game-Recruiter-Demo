from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import mainVisuals as vis, helper as h

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
def dinoPlayCard(dino, enemies, roundCount, clearing, event, entityNames, cardNames):
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
                    print(h.normalize("", 3) + cardNames[key].niceBodyText(3, h.WIDTH, supressedTypes = []))
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
    return (event,)
