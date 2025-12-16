import copy
import itertools
import random

import pytest

from Dinosaur_Venture import clearing as clr
from Dinosaur_Venture.dino_cards_depot.apple_orchard_hollow_cards import \
    orchardTree
from Dinosaur_Venture.dino_cards_depot.fallow_farmland_cards import (
    cultivator, gnawedCableCord, grasshopperCache, twigRockScarecrow)
from Dinosaur_Venture.dino_cards_depot.fundamental_cards import twigExclamation
from Dinosaur_Venture.dino_cards_depot.new_bear_order_cards import torchBearing
from Dinosaur_Venture.dino_cards_depot.shop_cards import stick
from Dinosaur_Venture.entities import dinoes as dinoes_import
from Dinosaur_Venture.entities import enemieses as enemieses_import


## Sets up dino, enemies, and the clearing. 
## All of the returned values have no unique/atypical mechanics
##  (as in, using the default dino, enemy, and clearing values give the same behavior).
## Clearing is randomly assigned.
def setup_getDinoEnemiesClearing():
    ## We want all the casters, dino, enemies, clearing, etc.

    ## (1 and 2) Caster and dino
    dinoes = [dinoes_import.Dinosaur()] ## Empty Player Character

    ## (3) Enemies
    enemieses = [
        [enemieses_import.Copperals()],
        [enemieses_import.Shrew(), enemieses_import.Shrew()],
        [enemieses_import.Enemy(), enemieses_import.Enemy(), enemieses_import.Enemy()],
        [enemieses_import.RaccoonBandit(), enemieses_import.RaccoonBandit(), enemieses_import.RaccoonBandit(), enemieses_import.RaccoonBandit(), enemieses_import.RaccoonBandit()]
    ]

    ## (4) Gets 5 clearings (randomly, allowing duplicates)
    clearinges = []
    setOfAllWoods = []
    for neck in clr.NeckOfTheWoods.__subclasses__():
        if neck().include:
            setOfAllWoods.append(neck())
    for i in range(3):
        random.shuffle(setOfAllWoods)
        neckOfTheWoods = setOfAllWoods[0]
        clearinges.append(neckOfTheWoods.clearing)

    return (dinoes, enemieses, clearinges)

## Gets the cartesian product of the given dinoes, enemieses, clearingses, and cardses
def getCartesianProduct_dinoEnemiesClearingCards(dinoes, enemieses, clearingses, cardses):
    masterSet = []
    for dinoCopy in dinoes:
        for enemiesCopy in enemieses:
            for clearingCopy in clearingses:
                for cardCopy in cardses:
                    ## Gets copies of all these items
                    dino = copy.deepcopy(dinoCopy)
                    enemies = copy.deepcopy(enemiesCopy)
                    clearing = copy.deepcopy(clearingCopy)
                    cards = copy.deepcopy(cardCopy)

                    masterSet.append((dino, enemies, clearing, cards))

    return masterSet

## More customized cartesian product.
## An array within this array within this array is not unpacked. Meaning, if you have an input like:
##      [ ..., [["first", "second"], [1, 2]], ... ]
## Those nested nested arrays stay paired.
def getCartesianProduct_anyInput(arrays):
    uncopiedReturnArray = list(itertools.product(*arrays))

    masterSet = []
    for uncopiedSubArray in uncopiedReturnArray:
        newSubArray = []
        for element in uncopiedSubArray:
            newSubArray.append(copy.deepcopy(element))
        masterSet.append(newSubArray)

    return masterSet

## For every array within arrays, returns a single instance of each.
## Most useful to get a single dino, enemies, and clearing for testing.
def getSingleSlice(arrays) -> tuple:
    returnArray = []
    for array in arrays:
        index = random.randint(0, len(array) - 1)
        print(" >> ", array[index])
        copiedValue = copy.deepcopy(array[index])
        returnArray.append(copiedValue)
    
    return tuple(returnArray)

## Returns a single slice of the dino, enemies, and clearing.
## Most useful for when we simply need burner values for these.
def getSingleSliceOfDinoEnemiesClearing() -> tuple:
    dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing()
    dino = dinoes[random.randint(0, len(dinoes) - 1)]
    enemies = enemieses[random.randint(0, len(enemieses) - 1)]
    clearing = clearingses[random.randint(0, len(clearingses) - 1)]
    return (dino, enemies, clearing)

## Gets card set 1, defined as cards that are:
## (1) Dino's and Vanilla
## (2) { 0H }
## (3) Stay in play after resolution
## (4) Requires no further input upon being played
## There are no guarentees about:
## (1) [ Text ] nor < Text >            - Although they will be vanilla
## (2) Tokens                           - Although they will be vanilla
@pytest.fixture
def setup_getCardSetOne():
    cardses = []
    cardses.append(twigExclamation())
    cardses.append(stick())
    cardses.append(grasshopperCache())
    cardses.append(torchBearing())
    return cardses

## Gets card set 2, which are cards that reappear in some location.
## These cards are returned 2 lists, cardses and toLocations. Equal index means same referent.
## Constraints:
## (1) Must give 0+ Actions
@pytest.fixture
def setup_getCardSetTwoWithToLocations():
    cardses = []
    toLocations = []
    '''
    cardses.append(orchardTree())
    toLocations.append("hand")
    cardses.append(cultivator())
    toLocations.append("draw")
    cardses.append(gnawedCableCord())
    toLocations.append("draw")
    '''
    cardses.append(twigRockScarecrow())
    toLocations.append("draw")

    '''
    cardsesWithToLocations = []
    for index in range(len(cardses)):
        cardsesWithToLocations.append((cardses[index], toLocations))
    '''
    
    return zip(cardses, toLocations)