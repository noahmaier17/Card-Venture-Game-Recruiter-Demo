import random, copy
from Dinosaur_Venture import cardModFunctions as cmf, helper as h, cardTokens as tk

## Groupings of common Card functionality.
##  Used for both Shell functions, and for the sake of lengthy-yet-common-enough Card functionality.

## Look at 'cache' in dinoCards.py for an example of making a custom card function for the purpose of shells.

## The class for a card function.
class cardFunctions():
    ## Inherited cardFunctions can override these to make for more customized implementation.
    ##  Can be omitted in the inheritance if unneeded.
    def __init__(self):
        pass

    ## The function call. Should be overridden every time.
    def func(self, card, caster, dino, enemies, passedInVisuals):
        pass

## For shells, a class for the parameters of the shell. Includes text and the cardFunction itself.
class shellTextWrapper():
    def __init__(self, text, cardFunction, excludeLineBreak = False):
        self.text = text
        self.cardFunction = cardFunction
        self.excludeLineBreak = excludeLineBreak

## ...
class dots(cardFunctions):
    pass

## +[ plusActionsCount ] Actions.
##  Use for shells; do not use for base-functionality of Cards.
##  Search Terms: +1 Action +2 Actions
class plusXActions(cardFunctions):
    def __init__(self, plusActionsCount):
        self.plusActionsCount = plusActionsCount

    def func(self, card, caster, dino, enemies, passedInVisuals):
        caster.plusActions(self.plusActionsCount)

## -[ minusActionsCount ] Actions.
##  Used for shells; do not use for base-functionality of Cards.
class minusXActions(cardFunctions):
    def __init__(self, minusActionsCount):
        self.minusActionsCount = minusActionsCount

    def func(self, card, caster, dino, enemies, passedInVisuals):
        caster.minusActions(self.minusActionsCount)

## +[ plusCardsCount ] Card(s).
##  Use for shells; do not use for base-functionality of Cards.
class plusXCards(cardFunctions):
    def __init__(self, plusCardsCount):
        self.plusCardsCount = plusCardsCount

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if self.plusCardsCount > 0:
            for i in range(self.plusCardsCount):
                caster.drawCard()

'''
    Cards ABOVE here are used EXCLUSIVELY for shells. 
        Do not use them for cards -- the functionality of the above cards tend to have easier-to-use function calls.
'''

## Break a Band.
class breakABand(cardFunctions):
    def init(self):
        self.fatalDamage = False
        self.brokeABand = False

    def func(self, card, caster, dino, enemies, passedInVisuals):
        preamble = ["Dealing: Break a Band."]

        pick = h.pickLivingEnemy("Pick an Enemy to Attack", enemies, preamble = preamble, passedInVisuals = passedInVisuals)
        if pick == -1:
            h.splash(" No Enemies can be targeted!")
            return
        else:
            enemy = enemies[pick]

            ## Stores attributes to cross-compare after damage is dealt
            alreadyDead = False
            beforeBandCount = enemy.getBands()

            ## Deals Damage
            enemy.destroyBand(dino, enemies)

            ## Compares the stored attributes against what occurred
            if not alreadyDead:
                self.fatalDamage = enemies[pick].dead
            if beforeBandCount > enemy.getBands():
                self.brokeABand = True

## [ damageArray ].
## Returns information about the nature of that damage dealt (see entity.DamageData).
class dealDamage(cardFunctions):
    ## def init(self):
    ##     self.fatalDamage = False
    ##     self.brokeABand = False

    def func(self, card, caster, dino, enemies, passedInVisuals, damageArray):
        ## CMF CASE: Check for dealDamage_dropNotick. If we have that modifer, changes the damageArray accordingly.
        if cmf.cmf_isLeftInRight([cmf.dealDamage_dropNotick], card.cmfDepot + caster.cmfDepot):
            h.splash("Card Modifier: Dealing Damage while ignoring -notick.")
            damageArray.stripNotick()

        if caster.enemy:
            dino.damage(caster, dino, enemies, damageArray)
        else:
            preamble = ["Dealing: " + str(damageArray) + "."]

            pick = h.pickLivingEnemy("Pick an Enemy to Attack", enemies, preamble = preamble, passedInVisuals = passedInVisuals)
            if pick == -1:
                h.splash(" No Enemies can be targeted!")
                return
            else:
                enemy = enemies[pick]

                ## Stores attributes to cross-compare after damage is dealt
                # alreadyDead = False
                # beforeBandCount = enemy.getBands()

                ## Deals Damage
                damageData = enemy.damage(caster, dino, enemies, damageArray)

                ## Compares the stored attributes against what occurred
                # if not alreadyDead:
                #     self.fatalDamage = enemies[pick].dead
                # if beforeBandCount > enemy.getBands():
                #     self.brokeABand = True

                return damageData

'''
    Cards ABOVE here are used for dealingDamage and special cases when dealing damage.
    Cards BELOW are the rest of them all.
'''

## [ value ] Chance.
## Returns TRUE on success (printing a success), and FALSE on failure (printing a failure).
class chance(cardFunctions):
    def __init__(self, value, onSuccess_printInsteadOfInput = False, onFailure_printInsteadOfInput = False,
                              onSuccess_noOutput = False, onFailure_noOutput = False):
        self.value = value
        self.onSuccess_printInsteadOfInput = onSuccess_printInsteadOfInput
        self.onFailure_printInsteadOfInput = onFailure_printInsteadOfInput
        self.onSuccess_noOutput = onSuccess_noOutput
        self.onFailure_noOutput = onFailure_noOutput

    def func(self, card, caster, dino, enemies, passedInVisuals):
        ## CMF CASE: Did we override this chance value for this card?
        fetchedCMF = cmf.cmf_fetchInRight([cmf.chance_modifyChance], card.cmfDepot + caster.cmfDepot)
        if fetchedCMF != None:
            self.value = fetchedCMF.value
            ## h.splash("Card Modifier: Chance value has been changed to " + str(self.value) + ".")

        if random.random() <= self.value:
            if not self.onSuccess_noOutput:
                h.splash("Succeeded " + str(self.value) + " Chance.", printInsteadOfInput = self.onSuccess_printInsteadOfInput)
            return True
        else:
            if not self.onFailure_noOutput:
                h.splash("Failed " + str(self.value) + " Chance.", printInsteadOfInput = self.onFailure_printInsteadOfInput)
            return False

## [ number ]x, ...
## Returns the number of times to do the something; used for cards that override [ number ]x.
class getter_numberX(cardFunctions):
    def __init__(self, value):
        self.value = value

    def func(self, card, caster, dino, enemies, passedInVisuals):
        ## CMF CASE: Check for getter_numberX_modifyX.
        ## If we have that modifer, changes the value we return accordingly.
        if cmf.cmf_isLeftInRight([cmf.getter_numberX_modifyX], card.cmfDepot + caster.cmfDepot):
            replacementValue = cmf.cmf_fetchInRight([cmf.getter_numberX_modifyX], card.cmfDepot + caster.cmfDepot).value
            h.splash("Card Modifier: Changing the #x value of this Card to " + str(replacementValue) + "x.")
            return replacementValue

        return self.value

## Gain a [ CARD ].
class gainACard(cardFunctions):
    def __init__(self, cardToGain, toLocation = "DEFAULT TO LOCATION", position = 0, printCard = False, inputCard = False):
        self.cardToGain = copy.deepcopy(cardToGain)
        self.toLocation = toLocation
        self.position = position
        self.printCard = printCard
        self.inputCard = inputCard

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if self.toLocation == "DEFAULT TO LOCATION":
            self.toLocation = caster.discard
        caster.gainCard(self.cardToGain(), self.toLocation,
                        position = self.position,
                        printCard = self.printCard,
                        inputCard = self.inputCard)

## To (an Arbitrary Enemy / every Enemy): +1 Action.
class toBlankEnemy_Plus1Action(cardFunctions):
    def __init__(self, toArbitraryEnemy = False, toEveryEnemy = False):
        self.toArbitraryEnemy = toArbitraryEnemy
        self.toEveryEnemy = toEveryEnemy

        ## Check
        if not self.toArbitraryEnemy and not self.toEveryEnemy:
            input("ERROR WITH INITIALIZATION OF toBlankEnemy_Plus1Action")

    def func(self, card, caster, dino, enemies, passedInVisuals):
        potentialEnemies = []
        for enemy in enemies:
            if not enemy.dead:
                potentialEnemies.append(enemy)

        if len(potentialEnemies) == 0:
            h.splash("FAIL_FIND_ENEMY")
            return None

        if self.toArbitraryEnemy:
            position = random.randint(0, len(potentialEnemies) - 1)
            potentialEnemies = [potentialEnemies[position]]

        for enemy in potentialEnemies:
            enemy.plusActions(1)

## To (an Arbitrary Enemy / every Enemy): Heal [ Heal Array ].
class toBlankEnemy_Heal(cardFunctions):
    def __init__(self, healArray, toArbitraryEnemy = False, toEveryEnemy = False):
        self.healArray = healArray
        self.toArbitraryEnemy = toArbitraryEnemy
        self.toEveryEnemy = toEveryEnemy

        ## Check
        if not self.toArbitraryEnemy and not self.toEveryEnemy:
            input("ERROR WITH INITIALIZATION OF toBlankEnemy_Heal")

    def func(self, card, caster, dino, enemies, passedInVisuals):
        potentialEnemies = []
        for enemy in enemies:
            if not enemy.dead:
                potentialEnemies.append(enemy)

        if len(potentialEnemies) == 0:
            h.splash("FAIL_FIND_ENEMY")
            return None

        if self.toArbitraryEnemy:
            position = random.randint(0, len(potentialEnemies) - 1)
            potentialEnemies = [potentialEnemies[position]]

        for enemy in potentialEnemies:
            enemy.heal(caster, dino, enemies, self.healArray)

## To (an Arbitrary Enemy / every Enemy): Discard (X / every) Card in Hand.
##  Returns the list of enemies affected.
class toBlankEnemy_DiscardBlank_fromHand(cardFunctions):
    def __init__(self, numberOfCardsToDiscard = 'ALL', toArbitraryEnemy = False, toEveryEnemy = False):
        if numberOfCardsToDiscard == 'ALL':
            self.discardAllCards = True
            self.numberOfCardsToDiscard = None
        else:
            self.discardAllCards = False
            self.numberOfCardsToDiscard = numberOfCardsToDiscard

        self.toArbitraryEnemy = toArbitraryEnemy
        self.toEveryEnemy = toEveryEnemy

        ## Check
        if not self.toArbitraryEnemy and not self.toEveryEnemy:
            input("ERROR WITH INITIALIZATION OF toBlankEnemy_DiscardBlank_fromHand")

    def func(self, card, caster, dino, enemies, passedInVisuals):
        potentialEnemies = []
        for enemy in enemies:
            if not enemy.dead:
                potentialEnemies.append(enemy)

        if len(potentialEnemies) == 0:
            h.splash("FAIL_FIND_ENEMY")
            return None

        if self.toArbitraryEnemy:
            position = random.randint(0, len(potentialEnemies) - 1)
            potentialEnemies = [potentialEnemies[position]]

        ## Gets the display text ready
        prefixText = "Discard "
        suffixText = "Card."
        if self.discardAllCards:
            prefixText += "all "
            suffixText = "Cards."
        elif self.numberOfCardsToDiscard == 1:
            prefixText += "a "
        else:
            prefixText += self.numberOfCardsToDiscard + " "
            suffixText = "Cards."

        for enemy in potentialEnemies:
            h.splash("To '" + enemy.name + "': " + prefixText + suffixText, printInsteadOfInput = True)
            if self.discardAllCards:
                while enemy.hand.length() > 0:
                    position = random.randint(0, enemy.hand.length() - 1)
                    enemy.discardCard(enemy.hand, position, dino, enemies, passedInVisuals)

            else:
                numberOfCardsToDiscard = self.numberOfCardsToDiscard
                if enemy.hand.length() == 0:
                    h.splash('FAIL_FIND_CARD')

                while enemy.hand.length() > 0 and numberOfCardsToDiscard > 0:
                    numberOfCardsToDiscard -= 1
                    position = random.randint(0, enemy.hand.length() - 1)
                    enemy.discardCard(enemy.hand, position, dino, enemies, passedInVisuals)

        return potentialEnemies


## { HH }.
class foreverLinger(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        card.foreverLinger = True

## { HH } Shell this.
class foreverLingerShellThis(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        card.foreverLinger = True
        card.shelled = True

## Shell this.
class shellThis(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        card.shelled = True

## Discard the bottom Card of Draw.
class discardBottomCardOfDraw(cardFunctions):
    def __init__(self, inputCard = True):
        self.inputCard = inputCard

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if caster.draw.length() > 0:
            caster.discardCard(caster.draw, caster.draw.length() - 1, dino, enemies, passedInVisuals, inputCard = self.inputCard)
        else:
            h.splash('FAIL_MOVE')

## + Cantrip.
class plusCantrip(cardFunctions):
    def __init__(self, inputCard = True):
        self.inputCard = inputCard

    def func(self, card, caster, dino, enemies, passedInVisuals):
        caster.drawCard()
        caster.plusActions(1)

## Arbitrarily Discard a Card from Draw.
class arbitrarilyDiscardCardFromDraw(cardFunctions):
    def __init__(self, inputCard = False):
        self.inputCard = inputCard

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if caster.draw.length() > 0:
            position = random.randint(0, caster.draw.length() - 1)
            caster.discardCard(caster.draw, position, dino, enemies, passedInVisuals, inputCard = self.inputCard)
        else:
            h.splash('FAIL_MOVE')

## Arbitrarily Discard a Card from [ Location ].
class arbitrarilyDiscardCardFrom_Location(cardFunctions):
    def __init__(self, location, inputCard = False):
        self.location = location
        self.inputCard = inputCard

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if self.location.length() > 0:
            position = random.randint(0, self.location.length() - 1)
            caster.discardCard(self.location, position, dino, enemies, passedInVisuals, inputCard = self.inputCard)
        else:
            h.splash('FAIL_MOVE')

## To an Arbitrary Card in [ Location ]:
##  --> Returns that Card, and then if it was successful
##  --> REQUIRES a location.
class getter_toArbitraryCardInLocation(cardFunctions):
    def __init__(self, location):
        self.location = location

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if self.location.length() > 0:
            position = random.randint(0, self.location.length() - 1)
            return [self.location.at(position), True]
        else:
            h.splash('FAIL_PICK_CARD')
            return ["null", False]

## Discard your Draw.
class discardYourDraw(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        while caster.draw.length() > 0:
            caster.discardCard(caster.draw, 0, dino, enemies, passedInVisuals)

## To every Enemy: [ damageArray ].
class toEveryEnemy_dealDamage(cardFunctions):
    def __init__(self, damageArray):
        self.damageArray = damageArray

    def func(self, card, caster, dino, enemies, passedInVisuals):
        for enemy in enemies:
            if enemy.dead == False:
                h.splash("To '" + enemy.name + "': " + str(self.damageArray) + ".", printInsteadOfInput = True)
                enemy.damage(caster, dino, enemies, self.damageArray)

## Move a Card from Hand onto Draw.
class moveACardFromHandOntoDraw(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        preamble = []

        if caster.hand.length() > 0:
            index = 1
            for card in caster.hand.getArray():
                text = str(index) + ": ^" + card.name + "^."
                preamble.append(text)
                index += 1

            pick = h.pickValue("Pick a Card to Move onto Draw", range(1, index), preamble = preamble, passedInVisuals = passedInVisuals) - 1

            caster.moveCard(caster.hand, pick, caster.draw, position = caster.draw.length())
        else:
            h.splash('FAIL_PICK_CARD')

## Destroy this.
class destroyThis(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals, location = 'DEFAULT', suppressErrorText = False):
        if location == 'DEFAULT':
            location = caster.play

        index = h.locateCardIndex(location, card)
        if index >= 0:
            caster.destroyCard(location, index)
            return True
        elif not suppressErrorText:
            h.splash('FAIL_DESTROY')
        return False

## [ Number ]x, to an Arbitrary Enemy: [ Damage Array ].
class numberX_toArbitraryEnemy_dealDamage(cardFunctions):
    def __init__(self, number, damageArray):
        self.number = number
        self.damageArray = damageArray

    def func(self, card, caster, dino, enemies, passedInVisuals):
        for i in range(self.number):
            livingEnemies = []
            for enemy in enemies:
                if enemy.dead == False:
                    livingEnemies.append(enemy)
            if len(livingEnemies) > 0:
                enemy = random.choice(livingEnemies)
                h.splash("To '" + enemy.name + "': " + str(self.damageArray) + ".", printInsteadOfInput = True)
                enemy.damage(caster, dino, enemies, self.damageArray)
            else:
                h.splash("FAIL_FIND_ENEMY")

## Discard All [ Names ] from [Location ].
##  --> discardMatches: if True (default behavior), discard all Cards which are in the "names" set.
##                      if False, keeps only the Cards in the "names" set.
##  --> To Discard All Cards from Hand: discardAll_names_fromLocation(caster.hand, [], discardMatches = False)
class discardAll_names_fromLocation(cardFunctions):
    def __init__(self, fromLocation, names, discardMatches = True):
        self.fromLocation = fromLocation
        self.names = names
        self.discardMatches = discardMatches

    def func(self, card, caster, dino, enemies, passedInVisuals):
        position = 0
        while position != self.fromLocation.length():
            if ((self.discardMatches and self.fromLocation.at(position).unmodifiedName in self.names)
                        or (self.discardMatches == False and self.fromLocation.at(position).name not in self.names)):
                caster.discardCard(self.fromLocation, position, dino, enemies, passedInVisuals)
            else:
                position += 1

## Mill [ numberToMill ] Cards from [ Location ], Unless [ checkClause ]. Then, Immill.
##  --> Returns the Card that matches "checkClause," moving it still to the "toLocation."
class mill(cardFunctions):
    def __init__(self, fromLocation = 'DEFAULT', toLocation = 'DEFAULT', numberToMill = 'INFINITE', usingCheckClause = False, checkClause = None):
        self.usingDefaultFromLocation = (fromLocation == 'DEFAULT')
        if self.usingDefaultFromLocation: ## We cannot yet assign this because we lack access to caster
            self.fromLocation = None
        else:
            self.fromLocation = fromLocation

        self.usingDefaultToLocation = (toLocation == 'DEFAULT')
        if self.usingDefaultToLocation:
            self.toLocation = h.cardLocation("Mill's Set Aside Mat")
        else:
            self.toLocation = toLocation

        self.foreverMill = (numberToMill == 'INFINITE')
        if not self.foreverMill:
            self.numberToMill = numberToMill
        else:
            self.numberToMill = -1

        self.usingCheckClause = usingCheckClause
        self.checkClause = checkClause

    ## Getter
    def getToLocation(self):
        return self.toLocation

    ## Returns the Card that matches the checkClause if any; it is still in the self.toLocation
    def mill_func(self, card, caster, dino, enemies, passedInVisuals, inputMatchCard = False):
        ## Sets the from location (now that we have access to caster)
        if self.usingDefaultFromLocation:
            self.fromLocation = caster.draw

        numberOfCardsMilled = 0
        ## Mills until milled the correct amount or the location is empty
        while self.fromLocation.length() > 0 and numberOfCardsMilled != self.numberToMill:
            card = self.fromLocation.pop()

            ## Do we have a match?
            if self.usingCheckClause and self.checkClause(card):
                if inputMatchCard:
                    h.splash("Found a Match while Milling: ^" + card.name + "^.")
                self.toLocation.append(card)
                return card
            self.toLocation.append(card)

            numberOfCardsMilled += 1

        ## In the case we are using a check clause, shows that we had no matches
        if self.usingCheckClause:
            h.splash("Found no Matches while Milling.")
        return 'NO MATCHES'

    def immill_func(self, card, caster, dino, enemies, passedInVisuals):
        ## Puts the milled cards back onto the toLocation in the same order
        if not self.usingDefaultToLocation:
            input(h.splash("COMPILER ERROR: Cannot 'immill' if not using the default 'toLocation' when Mill is done."))
            return

        self.toLocation.reverse()
        while self.toLocation.length() != 0:
            card = self.toLocation.pop()

            self.fromLocation.insert(0, card)

## #x, 'Plow' % Location %.
##  Unless there are no cards in % Location %:
##  (1) #x, pick an Arbitrary Card in % Location %; To it, Entoken it with <<prepared>>.
## --> Returns an array of the cards that were plowed. 
class plow(cardFunctions):
    def __init__(self, instances, location):
        self.location = location
        self.instances = instances

    def func(self, card, caster, dino, enemies, passedInVisuals):
        if self.location.length() == 0:
            h.splash("FAILURE Could not 'Plow'; there are no Cards in that Location.")
            return []

        array = []
        for i in range(self.instances):
            card, success = getter_toArbitraryCardInLocation(self.location).func(card, caster, dino, enemies, passedInVisuals)
            if success:
                card.publishToken(tk.prepare())
                if card not in array:
                    array.append(card)
        return array

## To the Previous Card in Play
##  --> Returns that Card, and then if it was successful
class getter_toPreviousCardInPlay(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        index = h.locateCardIndex(caster.play, card)
        if index == -1:
            h.splash('FAIL_FIND_CARD')
            return ["null", False]
        elif index == 0:
            h.splash('FAILURE There is no Previous Card in Play.')
            return ["null", False]

        previousCard = caster.play.at(index - 1)
        return [previousCard, True]

## To the Subsequent Card in Play
##  --> Returns that Card, and then if it was successful
class getter_toSubsequentCardInPlay(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        index = h.locateCardIndex(caster.play, card)
        if index == -1:
            h.splash('FAIL_FIND_CARD')
            return ["null", False]
        elif index == caster.play.length() - 1:
            h.splash('FAILURE There is no Subsequent Card in Play.')
            return ["null", False]

        subsequentCard = caster.play.at(index + 1)
        return [subsequentCard, True]

## |>| Pocket this.
class packingText_PocketThis(cardFunctions):
    def func(self, card, caster, dino, enemies, passedInVisuals):
        success = caster.moveMe(caster.hand, card, caster.pocket, supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, card, caster.pocket)








