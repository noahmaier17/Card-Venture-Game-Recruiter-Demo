from datetime import datetime

## Global boolean that will force logging to be ignored 
IGNORE_GAMEPLAY_LOGGING = False

LOG_FILE_NAME = "Logs/" + str(datetime.now())
LOG_FILE_NAME = LOG_FILE_NAME.replace(":", ".")

def newLogFile():
    if not IGNORE_GAMEPLAY_LOGGING:
        open(LOG_FILE_NAME, 'x')

## General function for writing text
def writeToLog(text):
    if not IGNORE_GAMEPLAY_LOGGING:
        with open(LOG_FILE_NAME, "a") as file:
            file.write(text + "\n")

## Logs playing a card
def playCardLog(entity, fromLocation, cardIndex, caster, dino, enemies):
    writeToLog(
        "PLAY CARD: " + 
        entity.name + " plays the " + str(cardIndex) + "th card from " + getCardLocationSpiel(fromLocation)
    )

## Logs the state of an entity at round start
def roundStartEntityLog(entity):
    locationsSpiel = ""
    for cardLocaiton in entity.getIterableOfLocations():
        locationsSpiel += getCardLocationSpiel(cardLocaiton)
    writeToLog(
        "ROUND START: " + 
        entity.name + " state: " + locationsSpiel
    )

## Logs the current 'event'
def currentEventLog(event):
    writeToLog(
        "CURRENT EVENT: " +
        event
    )


## Helper function -- gets information about a helper.cardLocation()
def getCardLocationSpiel(cardLocation):
    cardsSpiel = ""
    for card in cardLocation.getArray():
        cardsSpiel += getCardSpiel(card)
    if len(cardLocation.getArray()) == 0:
        cardsSpiel = "None"
    return "{ " + cardLocation.name + " -> " + cardsSpiel + " } "

## Helper function -- gets information about a card.Card()
def getCardSpiel(card):
    return "[ " + card.name + " -> tokens: " + str(card.tokens) + " ] "