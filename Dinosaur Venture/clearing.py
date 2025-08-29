import math, random, os
from colorama import init, Fore, Back, Style
import entity as e
import helper as h

## The Neck of the Woods
class NeckOfTheWoods():
    def __init__(self):
        self.name = None
        self.include = False

        self.themes = None
        self.high_damage = None
        self.multi_damage = None
        self.bestows_actions = None
        self.bestows_cards = None
        self.saps_actions = None
        self.saps_cards = None

        self.clearing = None

    def showClearing(self):
        text = []

## The distribution of the types
class dtr():
    def __init__(self, number, annotations):
        self.number = number
        self.annotations = annotations

## The actual clearing(s)
class Clearing():
    ## Sets all static variables prepared
    def __init__(self):
        ## The enemies this clearing have
        self.enemies = []

    ## Clears all stored information, resetting the clearing
    def populate(self, difficulty):
        self.enemies = []
        quitout = 50
        while True:
            quitout -= 1
            if quitout == 0:
                break
            else:
                worked, difficulty = self.attemptAdd(self.enemiesToLikelihood, difficulty)
                if worked == True:
                    quitout = 50
        random.shuffle(self.enemies)

    ## Tries to add an enemy to a clearing, ensuring that the difficulty cap is not exceeded.
    ## Returns [booleanIfWorked, newDifficulty]
    def attemptAdd(self, enemiesToLikelihood, difficulty):
        initialDifficulty = difficulty

        ## ----- Accounts for Enemies Size -----
        tableOfI = []
        for i in range(1, len(self.enemies) + 1):
            ## tableOfI.append(0.55 * i)
            ## difficulty -= sum(tableOfI)
            tableOfI.append(self.enemies[i - 1].difficulty)
            difficulty -= sum(tableOfI)

        ## ----- Selects Enemy -----
        # Adds all enemies which do not breach the difficulty threshold to likelihood + enemies table
        likelihoodTable = []
        enemiesTable = []
        for enemy, likelihood in enemiesToLikelihood.items():
            initEnemy = enemy()
            if initEnemy.difficulty <= difficulty:
                enemiesTable.append(initEnemy)
                likelihoodTable.append(likelihood)

        # If there are no enemies that may be added, returns False
        if len(enemiesTable) == 0:
            return (False, initialDifficulty)

        # Takes one of the enemies, weighted by likelihood
        randomNumber = random.uniform(0, sum(likelihoodTable))
        pickedEnemyIndex = -1
        for i in range(len(likelihoodTable)):
            randomNumber -= likelihoodTable[i]
            if randomNumber <= 0 and pickedEnemyIndex == -1: # stores the first time we breach the cusp of the likelihood table
                pickedEnemyIndex = i
        enemy = enemiesTable[pickedEnemyIndex]

        # With the enemy, decreases the difficulty
        difficulty -= enemy.difficulty

        ## ----- Special Things -----
        # enemy.specialSpawning()

        ## ----- Will it be added? -----
        if difficulty >= 0:
            self.enemies.append(enemy)
            return (True, difficulty)
        else:
            return (False, initialDifficulty)








'''
## Heirloom location
class HeirloomLocation(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "Heirlooms"
        self.clearing = self.KitchenTable()

    class KitchenTable(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "Kitchen Table"
            self.clearingText = "Don't forget this before you leave!"
'''

## The Pier
class ThePier(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "The Pier"
        self.include = True

        self.themes = [
            "^Fish^.",
            "<<inoperable>> Tokens and ways to remove them.",
            "$ Triggers.",
            "Turn End Triggers."
        ]

        self.high_damage        = dtr(2, ["~2 Cards",
                                          "Many ^Fish^ gainers also can do high damage"])
        self.multi_damage       = dtr(5, ["~7 Cards"])
        self.bestows_actions    = dtr(1, ["~2 Cards"])
        self.bestows_cards      = dtr(1.5, ["~3 Cards"])
        self.saps_actions       = dtr(2, ["~4 Cards"])
        self.saps_cards         = dtr(0, [])

        self.clearing = self.PierEntrance()

    class PierEntrance(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "The Dock"
            self.clearingText = "Not as bustling as it once before, nevertheless there prevails fish to be caught."
            self.table = ["The Pier"]

            self.enemiesToLikelihood = {
                e.Fisherman: 1,
                e.FishingCaravan: 0.25
            }

## Apple Orchard Hollow
class AppleOrchardHollow(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "Apple Orchard Hollow"
        self.include = True

        self.themes = [
            "'Plow'.",
            "Conditional <<prepared>> Tokens.",
            "To the previous / subsequent Card in Play..."
        ]

        self.high_damage        = dtr(2.5, ["~4 Cards"])
        self.multi_damage       = dtr(0, ["~0 Cards"])
        self.bestows_actions    = dtr(5, ["~8 Cards",
                                           "Includes: <<prepared>> and 'Plow'"])
        self.bestows_cards      = dtr(2, ["~2 Cards"])
        self.saps_actions       = dtr(1, ["~1 Cards"])
        self.saps_cards         = dtr(0, [])

        self.clearing = self.OrchardEntrance()

    class OrchardEntrance(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "Orchard Entrance"
            self.clearingText = "Harvest season is drawing closer, inviting those who which to poach the growing fruits."
            self.table = ["Apple Orchard Hollow"]

            self.enemiesToLikelihood = {
                e.MalabarGiantSquirrel: 1,
                e.FlyingSquirrel: 1
            }

## Bandits of the Highway
class BanditsOfTheHighway(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "Bandits of the Highway"
        self.include = True

        self.themes = [
            "+ Cantrip, + Cantrip.",
            "^Shovel^ and ^Rubbish^.",
            "Pocket and Chance mechanic.",
            "Discard your Hand.",
            "2_-nt / 2_-nt and variations."
        ]

        self.high_damage        = dtr(4, ["~6 Cards"])
        self.multi_damage       = dtr(0, ["~0 Cards"])
        self.bestows_actions    = dtr(1, ["~3 Cards"])
        self.bestows_cards      = dtr(3, ["~5 Cards",
                                          "Includes: ^Shovel Cards^"])
        self.saps_actions       = dtr(2, [])
        self.saps_cards         = dtr(2, [])

        self.clearing = self.Highwaymen()

    class Highwaymen(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "Highwaymen"
            self.clearingText = "These Bandits feign death in front of cars, taking advantage of the goodwill of drivers to steal car parts."
            self.table = ["Bandits of the Highway"]

            self.enemiesToLikelihood = {
                e.RaccoonBandit: 1,
                e.Skunk: 1,
                e.Karkit: 0.2
            }

## Copper Croppers
class CopperCroppers(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "Copper Croppers"
        self.include = True

        self.themes = [
            "If you have 1+ Actions at the End of Turn.",
            "{ HH }, namely |>| { HH }.",
            "Discard Cards in Enemy's Hand.",
            "'2_' and variations.",
            "'4_' and variations."
        ]

        self.high_damage        = dtr(2.5, ["~3-4 Cards"])
        self.multi_damage       = dtr(1, ["~2 Cards"])
        self.bestows_actions    = dtr(4, ["~5 Cards",
                                          "Mostly: 1-shots"])
        self.bestows_cards      = dtr(2, ["~3-4 Cards",
                                          "Mostly: 1-shots"])
        self.saps_actions       = dtr(1, [])
        self.saps_cards         = dtr(0, [])

        self.clearing = self.Farmhouse()

    class Farmhouse(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "Farmhouse"
            self.clearingText = "The center piece of a place designed to torment the rustic creatures that farmed there."
            self.table = ["Copper Croppers"]

            self.enemiesToLikelihood = {
                e.Copperals: 1,
                e.Rusterials: 1
            }

## New Bear Order
class NewBearOrder(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "New Bear Order"
        self.include = True

        self.themes = [
            "Action Economy, namely +2 Actions.",
            "Discard Cards of Draw.",
            "Discard your Hand.",
            "[ iTop ], < iTop >."
        ]

        self.high_damage        = dtr(5, ["~6 Cards"])
        self.multi_damage       = dtr(1, ["~1 Card (and ~1 Half Card)"])
        self.bestows_actions    = dtr(4, ["~5 Cards"])
        self.bestows_cards      = dtr(1.5, ["~ Cards",
                                            "Mostly: Discarding Draw.",
                                            "Mostly: '+1 Card'"])
        self.saps_actions       = dtr(3, [])
        self.saps_cards         = dtr(2, [])

        self.clearing = self.BearHeartland()

    class BearHeartland(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "Bear Heartland"
            self.clearingText = "Bears were once top of the food chain. They miss that spotlight, and hope to reclaim the title of wilderness’ most feared--where did the reverence go?"
            self.table = ["New Bear Order"]

            self.enemiesToLikelihood = {
                e.CinnamonBear: 1,
                e.Babybear: 1
            }


## Fallow Farmland
class FallowFarmland(NeckOfTheWoods):
    def __init__(self):
        super().__init__()
        self.name = "Fallow Farmland"
        self.include = True

        self.themes = [
            "Draw to 3 Cards in Hand.",
            "Move this onto Draw.",
            "Shell Cards.",
            "2_ / 2_ and variations."
        ]

        self.high_damage        = dtr(3.5, ["~5 Cards"])
        self.multi_damage       = dtr(3.5, ["~5 Cards",
                                            "Mostly: +1 Action."])
        self.bestows_actions    = dtr(1.0, ["~2 Cards",
                                            "Situational, Weak"])
        self.bestows_cards      = dtr(1.5, ["~3 Cards",
                                            "Mostly: Draw to X."])
        self.saps_actions       = dtr(0, [])
        self.saps_cards         = dtr(0, [])

        self.clearing = self.ShrewDen()

    class ShrewDen(Clearing):
        def __init__(self):
            super().__init__()
            self.name = "Shrew Den"
            self.clearingText = "A once peaceful prairie became the lucrative source of agricultural gains. It was farmed into desolation, and left the denizens infertile."
            self.table = ["Fallow Farmland"]

            self.enemiesToLikelihood = {
                e.Shrew: 1,
                e.HoardOfShrews: 0.75
            }

## Prints the clearings, showing comparisons / contrasting
def printClearings(clearings, roundCount):
    pad = 30

    ## Gets top line
    lineOne = h.normalize(" | [Round: " + str(roundCount) + "] Clearing: ???", 30) + "` "
    for i in range(len(clearings)):
        clearing = clearings[i]
        lineOne += h.normalize(str(i + 1) + ". '" + clearing.name + "'", 31 + 5) + "` "

    prefixText = []
    prefixText.append(lineOne)
    ## prefixText.append(h.normalize("-X-", pad + len(clearings) * (31 + 5 + 2) + 2, separator = "-"))
    prefixText.append(h.normalize("-X-", h.WIDTH + 2, separator = "-"))

    ## Gets index
    mainText = []
    mainText.append(h.normalize(" | High Damage", pad) + "` ")
    mainText.append(h.normalize(" | ", pad) + "` ")
    mainText.append(h.normalize(" | Multiple Damage", pad) + "` ")
    mainText.append(h.normalize(" | ", pad) + "` ")
    mainText.append(h.normalize(" | Bestows Actions", pad) + "` ")
    mainText.append(h.normalize(" | ", pad) + "` ")
    mainText.append(h.normalize(" | Bestows Cards", pad) + "` ")
    mainText.append(h.normalize(" | ", pad) + "` ")
    mainText.append(h.normalize(" | Saps Actions", pad) + "` ")
    mainText.append(h.normalize(" | ", pad) + "` ")
    mainText.append(h.normalize(" | Saps Cards", pad) + "` ")
    mainText.append(h.normalize(" | ", pad) + "` ")

    mainText.append(h.normalize("-X-", h.WIDTH + 2, separator = "-"))
    mainText.append(h.normalize(" | Clearing Themes", pad) + "` ")

    ## Adds distribution data
    for clearing in clearings:
        text = []

        distributionCalculator(text, clearings, clearing.high_damage)
        distributionCalculator(text, clearings, clearing.multi_damage)
        distributionCalculator(text, clearings, clearing.bestows_actions)
        distributionCalculator(text, clearings, clearing.bestows_cards)
        distributionCalculator(text, clearings, clearing.saps_actions)
        distributionCalculator(text, clearings, clearing.saps_cards)

        for i in range(len(text)):
            mainText[i] += text[i]

    ## Adds the strangely dropped "` "
    for i in range(len(mainText)):
        if i in [0, 2, 4, 6, 8, 10]:
            mainText[i] += "` "

    ## Colors
    for i in range(len(mainText)):
        if i in [0, 2, 4, 6, 8, 10]:
            # Gets the numbers
            iterations = len(clearings)
            numbers = []
            for j in range(iterations):
                numbers.append(mainText[i][pad + 2 + (j * (33 + 5)):pad + 5 + (j * (33 + 5))])
            # Looks for maximum counts
            maximum = max(numbers)

            maximumCount = 0
            for number in numbers:
                if number == maximum:
                    maximumCount += 1

            for j in range(len(numbers)):
                # print(j, numbers[j], ">>>", mainText[i][22 + (j * (33 + 5 + 6)):25 + (j * (33 + 5 + 6))])

                maxColorCode = "FoG"
                if maximumCount > 1:
                    maxColorCode = "FoY"

                usedColor = "FoR"
                if numbers[j] == maximum:
                    usedColor = maxColorCode

                mainText[i] = (
                    mainText[i][0:pad + 2 + (j * (33 + 11))] + usedColor
                    + mainText[i][pad + 2 + (j * (33 + 11)):pad + 5 + (j * (33 + 11))] + "FoW"
                    + mainText[i][pad + 5 + (j * (33 + 11)):-1])

    ## Prints themes
    startIndex = len(mainText) - 1 - 1
    foreward = h.normalize(" | ", pad) + "` "
    maxIndex = startIndex

    ## Adds theme information
    for clearing in clearings:
        index = startIndex
        for theme in clearing.themes:
            # Checks that we have the line, otherwise creates it
            lines = h.trueIndent("> " + theme, 2, 31 + 5, nextLineText = "", keepAsArray = True)

            # Prints the lines
            for line in lines:
                index += 1
                if len(mainText) - 1 < index:
                    mainText.append(foreward)

                mainText[index] += h.normalize(line, 31 + 5) + "` "

        maxIndex = max(maxIndex, index + 1)
        for remainingIndex in range(index + 1, maxIndex):
            mainText[remainingIndex] += h.normalize("", 31 + 5) + "` "

        foreward += h.normalize("", 31 + 5) + "` "

    ## Spacer line
    mainText.append(" | ")


    ## Prints it all
    for line in prefixText:
        ## h.splash(line, printInsteadOfInput = True, removePreline = True)
        print(h.colorize(line))
    for line in mainText:
        ## h.splash(line, printInsteadOfInput = True, removePreline = True)
        print(h.colorize(line))

def distributionCalculator(text, clearings, thisDtr):
    minitext = []
    dist = ""

    for i in range(int(5 * thisDtr.number)):
        dist += "|"

    minitext.append(h.normalize(thisDtr.number, 3) + " > " + h.normalize(dist, 30) + "` ")
    minitext.append(h.normalize("", 30 + 6) + "` ")

    for line in minitext:
        text.append(line)













class westernTown(Clearing):
    def __init__(self):
        super().__init__()
        self.name = "Western Town"
        self.clearingText = "Horses Everywhere!"
        self.table = ["Horse Hostelry"]

        self.enemiesToLikelihood = {
            e.RaccoonBandit: 1,
            e.Skunk: 1,
            e.Karkit: 0.2
        }

"""
class PopulatedFieldlandKnights(Clearing):
    def __init__(self):
        super().__init__()
        self.name = "Populated Fieldland Knights"
        self.clearingText = "A place dotted to the brim with 'Shrews,' with some 'Enshrined Capybaras' and 'Prairie Watch Dogs' that guard and train them."
        self.table = ["Humming Mech Field"]
        
        self.enemiesToLikelihood = {
            e.EnshrinedCapybara: 0.6,
            e.Shrew: 0.6,
            e.PrairieWatchDog: 0.6
        }

"""








