## Maps out enemy cards

import bisect
import copy
import math
import os
import random

from colorama import Back, Fore, Style, init

init(autoreset=True)
from Dinosaur_Venture import enemyCards as ec
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis

LOWERCASE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'y', 'v', 'w', 'x', 'y', 'z']
UPPERCASE_LETTERS = []
for letter in LOWERCASE_LETTERS:
    UPPERCASE_LETTERS.append(letter.upper())
NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
NUMBER_SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
KEYS = []
for key in NUMBER_SYMBOLS + LOWERCASE_LETTERS + UPPERCASE_LETTERS:
    KEYS.append(str(key))

SET_OF_NUMBERS = []
for i in range(-100, 100):
    for j in range(0, 100):
        SET_OF_NUMBERS.append(i + round((1/100) * j, 2))

plotWidth = h.WIDTH - 5
plotHeight = 30 - 5
MAP_ALL = True      ## Maps out all enemy cards

PAD = 37

PAD_X = 2
PAD_Y = 1

PAD_BEFORE_PLOT_X = 6
PAD_BEFORE_PLOT_Y = 2

def code(MAP_ALL):
    uninitializedEnemyCards = ec.EnemyCard.__subclasses__()
    enemyCards = []
    for card in uninitializedEnemyCards:
        enemyCards.append(card())

    ## Finds lowest and highest values of damageDist and siftDist
    damageRanges = None
    siftRanges = None

    for card in enemyCards:
        dd = card.damageDist
        sd = card.siftDist

        if damageRanges == None or siftRanges == None:
            damageRanges = [dd, dd]
            siftRanges = [sd, sd]

        damageRanges[0] = min(damageRanges[0], dd)
        damageRanges[1] = max(damageRanges[1], dd)
        siftRanges[0] = min(siftRanges[0], sd)
        siftRanges[1] = max(siftRanges[1], sd)

    ## With those ranges, we now construct the outline of a plot
    lines = []
    for i in range(plotHeight + PAD_Y + PAD_BEFORE_PLOT_Y - 1):
        lines.append("")

    ## The top 2 lines will be tick markers for damageRanges
    damageBinCounts = plotWidth // 5 - 1
    damageBinWidth = (damageRanges[1] - damageRanges[0]) / damageBinCounts

    text = "      "
    for i in range(damageBinCounts + 1):
        value = round(damageRanges[0] + damageBinWidth * i, 2)
        string = ""
        normalizedAbsoluteValue = h.normalize(abs(value), 4)
        if value < 0:
            string = Fore.RED + normalizedAbsoluteValue + Fore.WHITE
        else:
            string = Fore.GREEN + normalizedAbsoluteValue + Fore.WHITE
        text += " " + string

    lines[0] = text
    lines[1] = "     X" + ("``|``") * (damageBinCounts + 1)

    ## The left 6 of each line will be for siftRanges
    siftBinCounts = (plotHeight) - 1
    siftBinWidth = (siftRanges[1] - siftRanges[0]) / siftBinCounts

    for i in range(siftBinCounts + 1):
        index = i + PAD_BEFORE_PLOT_Y
        if i % 2 == 1:
            lines[index] += h.normalize(round(siftRanges[0] + siftBinWidth * i, 2), 4) + " -"
        else:
            lines[index] += " " + "   " + " `"

    ## Then, we need to plot all of these values
    ## Calculates all of the pixel-width bins for this
    damageBinWidthPixel = (damageRanges[1] - damageRanges[0]) / (plotWidth - 5 - PAD_X) ## We pad by 2 at the start
    uniformDamageBins = []
    for i in range(plotWidth + 1):
        uniformDamageBins.append(round(damageRanges[0] + damageBinWidthPixel * i, 5))

    siftBinWidthPixel = (siftRanges[1] - siftRanges[0]) / (plotHeight - 1 - PAD_Y) ## We pad at the start
    uniformSiftBins = []
    for i in range(plotHeight + 1):
        uniformSiftBins.append(round(siftRanges[0] + siftBinWidthPixel * i, 5))

    ## Gets all the points
    allPositions = {}
    for y in uniformSiftBins:
        for x in uniformDamageBins:
            allPositions[(x, y)] = []

    for card in enemyCards:
        damage = uniformDamageBins[bisect.bisect_left(uniformDamageBins, card.damageDist)]
        sift = uniformSiftBins[bisect.bisect_left(uniformSiftBins, card.siftDist)]

        newPoint = (damage, sift)
        allPositions[newPoint].append(card)

    ## With every coordinate with 1+ cards, we create a mapping to those cards
    keys = copy.deepcopy(KEYS)
    symbolToCardSet = {}
    coordinatesToCardSet = {}
    coordinatesToSymbolSet = {}

    for coordinate in allPositions:
        cards = allPositions[coordinate]
        if len(cards) > 0:
            key = keys.pop(random.randint(0, len(keys) - 1))
            symbolToCardSet[key] = cards

            coordinatesToCardSet[coordinate] = cards
            coordinatesToSymbolSet[coordinate] = key

    return (symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines)

def symbolicPrint(symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines):
    ## For every coordinate, first across horizontally and then down vertically, plots points
    lines = copy.deepcopy(lines)
    os.system('cls')
    print("-- SYMBOLIC PRINT -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")

    characterCountPerLine = []
    for line in lines:
        characterCountPerLine.append(0)

    for coordinate in coordinatesToSymbolSet:
        key = coordinatesToSymbolSet[coordinate]
        cardCount = len(coordinatesToCardSet[coordinate])

        damagePos = bisect.bisect_left(uniformDamageBins, coordinate[0])
        siftPos = bisect.bisect_left(uniformSiftBins, coordinate[1])
        lineIndex = siftPos + PAD_BEFORE_PLOT_Y + PAD_Y

        currentLine = lines[lineIndex]
        lines[lineIndex] = (
            currentLine + 
            h.normalize("", damagePos + PAD_X - characterCountPerLine[lineIndex]) +
            key
        )
        ## vis.rainbowColorizeFetcher(cardCount) + key + Style.NORMAL + Fore.WHITE

        characterCountPerLine[lineIndex] = damagePos + PAD_X + 1

    ## We need to make sure every line has enough whitespace
    for i in range(2, len(lines)):
        while characterCountPerLine[i] < plotWidth:
            characterCountPerLine[i] += 1
            lines[i] += " "

    return lines


def countsPrint(symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines):
    ## For every coordinate, first across horizontally and then down vertically, plots points
    lines = copy.deepcopy(lines)
    os.system('cls')
    print("-- COUNTS PRINT - -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")

    characterCountPerLine = []
    for line in lines:
        characterCountPerLine.append(0)

    for coordinate in coordinatesToCardSet:
        cards = coordinatesToCardSet[coordinate]
        cardCount = len(cards)

        damagePos = bisect.bisect_left(uniformDamageBins, coordinate[0])
        siftPos = bisect.bisect_left(uniformSiftBins, coordinate[1])
        lineIndex = siftPos + PAD_BEFORE_PLOT_Y + PAD_Y

        currentLine = lines[lineIndex]
        lines[lineIndex] = (
            currentLine + 
            h.normalize("", damagePos + PAD_X - characterCountPerLine[lineIndex]) +
            vis.rainbowNormalize(cardCount, 1)
        )

        characterCountPerLine[lineIndex] = damagePos + PAD_X + 1

    ## We need to make sure every line has enough whitespace
    for i in range(2, len(lines)):
        while characterCountPerLine[i] < plotWidth:
            characterCountPerLine[i] += 1
            lines[i] += " "

    return lines

def addCircle(center, symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines):
    binCenterX, binCenterY = fetchPointInPlot(center, symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines)

    centerX = center[0]
    centerY = center[1]

    ITERATIONS = 1009
    ## SYMBOLS = [" ", ".", ":", "%"]
    SYMBOLS = [" ", " ", " ", "%"]

    for i in range(0, ITERATIONS):
        theta = 2 * math.pi * (i / ITERATIONS)
        for iteration, symbol in enumerate(SYMBOLS):
            x = centerX + math.cos(theta) * 0.8 * (iteration / len(SYMBOLS))
            y = centerY + math.sin(theta) * 0.8 * (iteration / len(SYMBOLS))

            plotPoint((x, y), symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines, symbol = symbol)

    return newLines

def plotPoint(center, symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines, symbol = "#"):
    ## Gets the coordinates
    binXPos, binYPos = fetchPointInPlot(center, symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines)
    if binXPos == None or binYPos == None:
        return

    ## Gets the correct line-based position
    lineIndex = binYPos + PAD_BEFORE_PLOT_Y + PAD_Y
    positionedIndex = binXPos + PAD_BEFORE_PLOT_X + PAD_X

    if lines[lineIndex][positionedIndex] == " ":
        lines[lineIndex] = (
            lines[lineIndex][:positionedIndex] +
            symbol +
            lines[lineIndex][positionedIndex + 1:]
        )

def fetchPointInPlot(center, symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines):
    ## Gets the coordinates
    x = center[0]
    y = center[1]

    binXPos = bisect.bisect_left(uniformDamageBins, x)
    if binXPos == 0 and x < uniformDamageBins[0]:
        return (None, None)
    if binXPos == len(uniformDamageBins):
        return (None, None)
    if binXPos + PAD_BEFORE_PLOT_X + PAD_X > PAD_BEFORE_PLOT_Y + PAD_Y + plotWidth:
        return (None, None)

    binYPos = bisect.bisect_left(uniformSiftBins, y)
    if binYPos == 0 and y < uniformSiftBins[0]:
        return (None, None)
    if binYPos == len(uniformSiftBins):
        return (None, None)
    if binYPos + PAD_BEFORE_PLOT_Y + PAD_Y >= len(lines):
        return (None, None)

    return (binXPos, binYPos)
















## ----- -----
symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines = code(MAP_ALL)

typeSwitch = 0
lastPoint = (0, 0)
while True:
    if typeSwitch == 0:
        newLines = symbolicPrint(symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines)
        newLines = addCircle(lastPoint, symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, newLines)
    elif typeSwitch == 1:
        newLines = countsPrint(symbolToCardSet, coordinatesToCardSet, coordinatesToSymbolSet, uniformDamageBins, uniformSiftBins, lines)

    for newLine in newLines:
        print(newLine)

    character = input(" [Symbol], (point), (circle), (color), (set_range): ")
    print("")

    if character in symbolToCardSet:
        count = 1
        for card in symbolToCardSet[character]:

            print("  " + h.normalize(card.nameWithTokens(), PAD) + ":  " + card.niceBodyText(PAD + 5, h.WIDTH, supressedTypes = []))
            print("  " + h.normalize( "(damageDist: " + str(round(card.damageDist, 2)) + ") (siftDist: " + str(round(card.siftDist, 2)) + ")", PAD ) + ".")

            count += 1
            
            text = "  " + h.normalize("", PAD) + "."
            print(text)
        input(" ... ")

    if character.strip().lower() == "point":
        typeSwitch = 0
        x = h.pickValue("What damageDist value?", SET_OF_NUMBERS, intType = False)
        y = h.pickValue("What siftDist value?", SET_OF_NUMBERS, intType = False)
        lastPoint = (x, y)
    if character.strip().lower() == "circle":
        typeSwitch = 0
    if character.strip().lower() == "color":
        typeSwitch = 1
