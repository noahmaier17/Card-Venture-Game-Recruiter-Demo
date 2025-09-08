import pytest, pytest_timeout, random
from Dinosaur_Venture import entity as e, getCardsByTable as gcbt, clearing as clr

## Sets up dino, enemies, and the clearing.
## Clearing is randomly assigned.
@pytest.fixture
def setup_getDinoEnemiesClearing():
    ## We want all the casters, dino, enemies, clearing, etc.

    ## (1 and 2) Caster and dino
    dinoes = [e.Dinosaur()] ## Empty Player Character

    ## (3) Enemies
    enemieses = []
    enemieses.append([e.Copperals()])

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

## Gets card set 1, defined as cards that are:
## (1) Dino's and Vanilla
## (2) { 0H }
## (3) Stay in play after resolution
## (4) Requires no further input upon being played
## There are no guarentees about:
## (1) [ Text ] nor < Text >            - Although they will be vanilla
## (2) Tokens                           - Although they will be vanilla
@ pytest.fixture
def setup_getCardSetOne():
    cardses = []
    cardses.append(gcbt.getCardByName("Twig!"))
    cardses.append(gcbt.getCardByName("Stick"))
    cardses.append(gcbt.getCardByName("Grasshopper Cache"))
    cardses.append(gcbt.getCardByName("Torch Bearing"))
    return cardses