import copy

## from Dinosaur_Venture.dino_cards_depot import GeneralDinoCards as gdc
from Dinosaur_Venture import enemyCards as ec_ec
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.dino_cards_depot import (AppleOrchardHollowCards,
                                               BanditsOfTheHighwayCards,
                                               ChickenCoupCards,
                                               FeFarmersCards,
                                               DebuffsCards, DebugCards,
                                               FallowFarmlandCards,
                                               FastFoodMascotsCards,
                                               FruitbearingMonksCards,
                                               FundamentalCards)
from Dinosaur_Venture.dino_cards_depot import GeneralDinoCards as gdc
from Dinosaur_Venture.dino_cards_depot import (GraverobberCards,
                                               HorseHostelryCards,
                                               NewBearOrderCards,
                                               PackingBotCards,
                                               RubbleDwellersCards, ShopCards,
                                               ThePierCards)

## Tier 1 Tables
TIER_1_TABLES = [
    "Fallow Farmland",
    "New Bear Order",
    "Bandits of the Highway",
    "Fe Farmers",
    "Apple Orchard Hollow",
    "The Pier"
]

## Character Tables
CHARACTER_TABLES = [
    "Packing Bot",
    "Graverobber"
]

## All Dino Cards (so TIER 1, 2, 3, and 4)
ALL_DINO_CARDS = [] + CHARACTER_TABLES + TIER_1_TABLES

## Tables that are implememented but their cards are not in the game currently
WIP_TABLES = [
    "Fruit-Bearing Monks",
    "Horse Hostelry",
    "Rubble-Dwellers",
    "Chicken Coup"
]

## All Dino Cards including WIP Dino Clearings
ALL_DINO_CARDS_INCLUDING_WIP = [] + ALL_DINO_CARDS + WIP_TABLES

## Enemy cards
ENEMY_TABLES = [
    "Enemy",
    "Enemy Card Pool"
]

## All the tables (including WIP)
ALL_TABLES = [
    "Debug",
    "Fundamental",
    "Shop",
    "Debuffs"
] + ALL_DINO_CARDS + WIP_TABLES + ENEMY_TABLES

## Gets a list of all the cards.
def getAllCards():
    cardLocation = h.cardLocation("All Cards")
    for card in gdc.DinoCard.__subclasses__() + gdc.DinoShellCard.__subclasses__() + ec_ec.EnemyCard.__subclasses__():
        cardLocation.append(card())
    return cardLocation

## All Cards global variable
ALL_CARDS = getAllCards()

## Pools all the enemy cards into an uninitialized list
ENEMY_CARD_POOL_UNINIT = []
for Card in ec_ec.EnemyCard.__subclasses__():
    if any(i in Card().table for i in ["Enemy Card Pool"]):
        ## We add it 2x
        ENEMY_CARD_POOL_UNINIT.append(Card)
        ENEMY_CARD_POOL_UNINIT.append(Card)

## Gets a card based on its name. Assumes all cards have unique names.
def getCardByName(name):
    for card in ALL_CARDS.getArray():
        if card.name.lower() == name.lower():
            return copy.deepcopy(card)
    h.splash("FAILURE Cannot getCardByName with a name of: '" + name + "'; Returning 'Nothing'.")
    return getCardByName("Nothing")

## Gathers into a list all cards that contain at least 1 matching location
##  Performs a deep copy of the cards.
def getCardsByTable(crosscompareTable, locationName = "", excludeShells = False, excludeNonShells = False):
    cardLocation = h.cardLocation(locationName)
    tabulizedCards = []

    for card in ALL_CARDS.getArray():
        if any(i in card.table for i in crosscompareTable):
            if not((excludeShells and card.isShellCard) or (excludeNonShells and not card.isShellCard)):
                tabulizedCards.append(card)

    for card in tabulizedCards:
        card = copy.deepcopy(card)
        cardLocation.append(card)

    return cardLocation

## Gets all Dino Cards (shells EXCLUDED) as an Array
def getDinoCards():
    return getCardsByTable(ALL_DINO_CARDS, excludeShells=True).getArray()

## Gets all Dino Shell Cards (non-shells EXCLUDED) as an Array
def getDinoShellCards():
    return getCardsByTable(ALL_DINO_CARDS, excludeNonShells=True).getArray()

## Gets all Enemy Cards as an Array
def getEnemyCards():
    return getCardsByTable(["Enemy Card Pool"]).getArray()

## Gets all Dino Cards including those of which that are in process of being created as an Array
def getAllCards_includingWIP(excludeShells = False, excludeNonShells = False):
    return getCardsByTable(ALL_TABLES, excludeShells=excludeShells, excludeNonShells=excludeNonShells).getArray()

## Gets Cards by Name
def getMapOfCardNames():
    cardNames = {}
    for child in ALL_CARDS.getArray():
        child = copy.deepcopy(child)
        cardNames.update({child.name.lower(): child})
    return cardNames