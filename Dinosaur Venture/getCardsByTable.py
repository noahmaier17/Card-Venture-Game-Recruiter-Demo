import dinoCards as dc_dc
import enemyCards as ec_ec
import helper as h
import copy

## Variables
TIER_1_TABLES = [
    "Fallow Farmland",
    "New Bear Order",
    "Bandits of the Highway",
    "Copper Croppers",
    "Apple Orchard Hollow",
    "The Pier"
]

## Gathers into a list all cards that contain at least 1 matching location
##  Performs a deep copy of the cards.
def getCardsByTable(crosscompareTable, locationName = ""):
    cardLocation = h.cardLocation("")
    tabulizedCards = []

    for Card in dc_dc.DinoCard.__subclasses__() + dc_dc.DinoShellCard.__subclasses__() + ec_ec.EnemyCard.__subclasses__():
        if any(i in Card().table for i in crosscompareTable):
            tabulizedCards.append(Card())

    for card in tabulizedCards:
        copy.deepcopy(card)
        cardLocation.append(card)

    return cardLocation

## Gets Cards bytearraycardNames = {}
def getMapOfCardNames():
    cardNames = {}
    for child in dc_dc.DinoCard.__subclasses__() + dc_dc.DinoShellCard.__subclasses__() + ec_ec.EnemyCard.__subclasses__():
        cardNames.update({child().name.lower(): child()})
    return cardNames







