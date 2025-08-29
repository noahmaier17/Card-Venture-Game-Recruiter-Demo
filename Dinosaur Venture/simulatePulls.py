import math, random, os
from colorama import init, Fore, Back, Style
init(autoreset=True)
import card as c
import enemyCards as ec
import dinoCards as dc
import helper as h

## Simulates card pulls, showing what can be expected from different sets

PULL_TABLE = []
#PULL_TABLE.append("Bandits of the Highway")
PULL_TABLE.append("Apple Orchard Hollow")
#PULL_TABLE.append("Fallow Farmland")
#PULL_TABLE.append("New Bear Order")
## PULL_TABLE = ["Home"]
PULLS = 4

tabulizedCards = []
for Card in dc.DinoCard.__subclasses__() + dc.DinoShellCard.__subclasses__() + ec.EnemyCard.__subclasses__():
    if any(i in Card().table for i in PULL_TABLE):
        tabulizedCards.append(Card())

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
            + picks[i].niceBodyText(41, h.WIDTH, supressedTypes = []))
        print("")
    input(" ... ")