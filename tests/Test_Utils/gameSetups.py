import copy
import itertools
import random

import pytest

from Dinosaur_Venture import clearing as clr
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture.entities import dinoes as dinoes_import, enemieses as enemieses_import


## Sets up dino, enemies, and the clearing. 
## All of the returned values have no unique/atypical mechanics
##  (as in, using the default dino, enemy, and clearing values give the same behavior).
## Clearing is randomly assigned.
@pytest.fixture
def setup_getDinoEnemiesClearing():
    ## We want all the casters, dino, enemies, clearing, etc.

    ## (1 and 2) Caster and dino
    dinoes = [dinoes_import.Dinosaur()] ## Empty Player Character

    ## (3) Enemies
    enemieses = []
    enemieses.append([enemieses_import.Copperals()])

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
    cardses.append(gcbt.getCardByName("Twig!"))
    cardses.append(gcbt.getCardByName("Stick"))
    cardses.append(gcbt.getCardByName("Grasshopper Cache"))
    cardses.append(gcbt.getCardByName("Torch Bearing"))
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
    cardses.append(gcbt.getCardByName("Orchard Tree"))
    toLocations.append("hand")
    cardses.append(gcbt.getCardByName("Cultivator"))
    toLocations.append("draw")
    cardses.append(gcbt.getCardByName("Gnawed Cable Cord"))
    toLocations.append("draw")
    '''
    cardses.append(gcbt.getCardByName("Twig-Rock Scarecrow"))
    toLocations.append("draw")

    '''
    cardsesWithToLocations = []
    for index in range(len(cardses)):
        cardsesWithToLocations.append((cardses[index], toLocations))
    '''
    
    return zip(cardses, toLocations)