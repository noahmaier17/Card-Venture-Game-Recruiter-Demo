import re

## Allows for modification of cardFunctions by using unique identifiers.

## A cmf can be stored in a card or entity. cardFunctions.py watches for certain cardModifierFunctions and changes behavior accordingly.

## The class for a card modifier function.
class cardModFunction():
    ## Inherited cardModFunction can override these to make for more customized implementation.
    ##  Can be omitted in the inheritance if unneeded.
    def __init__(self):
        self.permament = True

    ## The function call.
    ## Can be omitted in the inheritance of unneeded; some modifers are simply boolean (do we have this modifier or not?).
    def func(self, card, caster, dino, enemies, passedInVisuals):
        pass

    ## Modifies body text of the card.
    ## Many modifications permanently mutate a Card. To have consistent implementation, call this to mutate the card.
    def mutateCardBodyText(self, card):
        pass

    ## If we append to a depot a modification twice, determines the way in which to handle them.
    ## Default behavior is FIFO.
    def handleDuplicateCMF(self, depot):
        ## Too lazy to do right now
        pass

## MODIFIES:    cf.dealDamage()
## TYPE:        static
## USE CASE:    On Cards OR On Entities.
## All damage drops the -notick.
class dealDamage_dropNotick(cardModFunction):
    pass

## MODIFIES:    cf.getter_numberx()
## TYPE:        dynamic
## USE CASE:    On Cards, to change the #x or x# values on that card.
## Changes the number on a #x or x# effect to be [ value ].
class getter_numberX_modifyX(cardModFunction):
    def __init__(self, value):
        self.value = value

    def mutateCardBodyText(self, card):
        ## Replaces #x instances
        replacement = str(self.value) + "x"
        regexCondition = "[0-9]+x"

        card.bodyText.mutateThrowText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.core))
        card.bodyText.mutateRoundStartText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.roundStart))
        card.bodyText.mutatePackingText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.packing))

        ## Replaces x# instances
        replacement = "x" + str(self.value)
        regexCondition = "x[0-9]+"

        card.bodyText.mutateThrowText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.core))
        card.bodyText.mutateRoundStartText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.roundStart))
        card.bodyText.mutatePackingText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.packing))

## MODIFIES:    cf.chance()
## TYPE:        dynamic
## USE CASE:    On Cards, to change the chance values on that card.
## Modify all Chance values to be [ value ].
class chance_modifyChance(cardModFunction):
    def __init__(self, value):
        self.value = value

    def mutateCardBodyText(self, card):
        replacement = str(self.value) + " Chance"
        regexCondition = "0.[0-9]+ Chance"

        card.bodyText.mutateThrowText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.core))
        card.bodyText.mutateRoundStartText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.roundStart))
        card.bodyText.mutatePackingText(replaceRegexConditionWithString(regexCondition, replacement, card.bodyText.packing))

## Given a regex condition, a replacement string, and a body of text,
## replaces instances of that condition with the replacement string
def replaceRegexConditionWithString(regexCondition, replacement, text):
        split = re.split(regexCondition, text)
        returnText = split[0]
        split = split[1:len(split)]
        for element in split:
            returnText += replacement + element
        return returnText

## Checks to see if we have the right cardModFunctions
def cmf_isLeftInRight(leftMoments, rightMoments):
    typedRightMoments = []
    for rightMoment in rightMoments:
        typedRightMoments.append(type(rightMoment))

    for leftMoment in leftMoments:
        if leftMoment not in typedRightMoments:
            return False

    return True

## Gets the CMF; returns None if does not exist
def cmf_fetchInRight(leftMoments, rightMoments):
    typedRightMoments = []
    for rightMoment in rightMoments:
        typedRightMoments.append(type(rightMoment))

    for leftMoment in leftMoments:
        if leftMoment in typedRightMoments:
            for i, typedRightMoment in enumerate(typedRightMoments):
                if leftMoment == typedRightMoment:
                    return rightMoments[i]

    return None
