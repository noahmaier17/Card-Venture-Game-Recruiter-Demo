import math
import os
import random

from colorama import Back, Fore, Style, init

init(autoreset=True)
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h

## Simulates card pulls, showing what can be expected from different sets

def code():
    PULL_TABLE = []
    #PULL_TABLE.append("Bandits of the Highway")
    PULL_TABLE.append("Apple Orchard Hollow")
    #PULL_TABLE.append("Fallow Farmland")
    #PULL_TABLE.append("New Bear Order")
    ## PULL_TABLE = ["Home"]
    PULLS = 4

    tabulizedCards = []
    for card in gcbt.getDinoCards() + gcbt.getDinoShellCards() + gcbt.getEnemyCards():
        if any(i in card.table for i in PULL_TABLE):
            tabulizedCards.append(card)

    os.system('cls')
    epoch = 0 
    while True:
        epoch += 1
        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - // " + str(epoch) + " // - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        picks = []
        random.shuffle(tabulizedCards)
        for i in range(PULLS):
            if len(tabulizedCards) > i:
                picks.append(tabulizedCards[i])
        for i in range(len(picks)):
            print(" " + str(i + 1) + ". " 
                + Back.CYAN + Style.BRIGHT + " " + picks[i].name + " "
                + Back.RESET + Style.NORMAL 
                + h.normalize("", 41 - 5 - len(str(i+1)) - len(picks[i].name)) 
                + picks[i].niceBodyText(41, h.WIDTH, suppressedTypes = []))
            print("")
        input(" ... ")

if __name__ == '__main__':
    code()