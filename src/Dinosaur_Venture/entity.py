import math, random, copy
from colorama import init, Fore, Back, Style
init(autoreset=True)
from Dinosaur_Venture import (
    helper as h,
    cardTokens as tk,
    react as r,
    mainVisuals as vis,
    getCardsByTable as gcbt,
    gameplayLogging as log,
    channel_linked_lists as cll
)

class Entity():
    def __init__(self):
        ## Index in the enemy list
        self.index = 0
        ## Presented name and stored name 
        self.name = ""
        self.initialEnemyName = ""
 
        self.text = "ERROR"

        self.looting = 1

        self.damageDist = 1
        self.siftDist = 1

        ## How difficult the enemy is to face.
        ##  Look for information in 'clearing.py'
        self.difficulty = 1
        
        ## Enemy and isDinosaur are exclusive; do not change this value by other commands
        self.enemy = True

        ## The health of the enemy; should be overriden in inheritance
        self.hp = cll.DeadHealthcons()

        ## The deck zones
        ## Do not change these names! Functionality depends on reading the names of these locations
        self.deck = h.cardLocation('deck')

        self.draw = h.cardLocation('draw')
        self.hand = h.cardLocation('hand')
        self.discard = h.cardLocation('discard')
        self.play = h.cardLocation('play')
        self.intoHand = h.cardLocation('into-hand')
        self.intoIntoHand = h.cardLocation('into-into-hand')
        self.pocket = h.cardLocation('pocket')

        ## Card Handler Functions, which allow the overriding of cardFunctions functionality
        ## Similar to Badges
        self.cmfDepot = []

        ## Action count.
        self.actions = 1
        ## How many Actions are gained at the start of each turn.
        self.upkeepActions = 1
        self.canGainActionsThisTurn = True

        ## At each Round Start, passively heals from each channel this much 
        self.healR = 0
        self.healG = 0
        self.healB = 0
        ## At each Rest Stop, increases the resetR, resetG, and resetB by this much
        self.uptickResetR = 0
        self.uptickResetG = 0
        self.uptickResetB = 0
        ## At Rest Stop, sets R, G, and B to be these values
        self.resetR = 0 - self.healR
        self.resetG = 0 - self.healG
        self.resetB = 0 - self.healB

        ## At the end of Rest, adds this many looting to looting
        self.uptickLooting = 1
        ## If we are skipping the next shop
        self.skipNextShop = False

        ## Tracks the upcoming values 
        self.upcomingPlusCard = []
        self.upcomingPlusAction = []
        ## What these are reset to
        self.resetUpcomingPlusCard = []
        self.resetUpcomingPlusAction = []

        ## Number of Cards to draw for a new Hand.
        self.deckDraw = 2

        ## If dead
        self.dead = False
        ## If, even while dead, the entity can play Cards
        self.deadCardPlays = False

        ## Tracks if a band was broken from a damage source currently -- if True, negates further damage
        self.bandBreak = False

        ## Tracks if damaged in a non-fatal way
        self.nonfatalDamageTaken = False
        self.didOnceATurnAtTriggerNonfatalDamageTaken = False

        self.didOnceATurnAtTriggerTurnStart = False

        self.didOnceARoundAtTriggerDinoPlayedCard = False
        self.didOnceATurnAtTriggerDinoPlayedCard = False

        ## Tracks if the entity has done any damage (even if that damage dealt was 0)
        self.dealtDamageThisTurn = False

        ## Tracks if the enemy died this turn -- reset at Turn End
        self.diedThisTurn = False

        ## Number of turns this entity has taken
        self.turn = 0
        ## Do we have another turn incoming?
        self.extraTurnQueued = False
        ## Are we on an extra turn?
        self.onExtraTurn = False
    
    ## Gets the locations of the entity CONCATENATED (notably excluding Deck)
    def getLocations(self):
        locations = self.getIterableOfLocations()
        returnArray = []
        for location in locations:
            returnArray += location.getArray()

        return returnArray

    ## Gets the locations of the entity AS AN ARRAY OF CardLocations (notably excluding Deck)
    def getIterableOfLocations(self):
        array = []
        array.append(self.pocket)
        array.append(self.hand)
        array.append(self.intoHand)
        array.append(self.intoIntoHand)
        array.append(self.discard)
        array.append(self.play)
        array.append(self.draw)
        return array

    ## Checks if Dino is Dead
    def enemyTurnDinoDeathCheck(self, roundCount):
        if self.getBands() == 0:
            self.hp = cll.DeadHealthcons()
    
    def dinoTurnDinoDeathCheck(self, roundCount):
        if self.getBands() == 0:
            input(Fore.RED + " !!! !!! !!!" + Fore.WHITE)
            input(self.name + " has run out of power :(")
            print("Areas traversed: " + str(roundCount + 1))
            print("Cards in deck:")
            for card in self.deck.getArray():
                print(" | " + Back.CYAN + Style.BRIGHT + card.name)
            print(0/0)
    
    def nextHandDrawCount(self, simplyObserve = False):
        totalDeckDraw = self.deckDraw
        if len(self.upcomingPlusCard) > 0:
            if simplyObserve:
                totalDeckDraw += self.upcomingPlusCard[0]
            else:
                totalDeckDraw += self.upcomingPlusCard.pop(0)
        return max(0, totalDeckDraw)

    def nextTurnActionCount(self, simplyObserve = False):
        actionCount = self.upkeepActions
        if len(self.upcomingPlusAction) > 0:
            if simplyObserve:
                actionCount += self.upcomingPlusAction[0]
            else:
                actionCount += self.upcomingPlusAction.pop(0)
        return actionCount

    ## Called to pick a card to play (by default, randomly but weighted by likelihood values). 
    ##  Returns 'nil' or a card index. 
    ##  Can be replaced if an entity has customized card selection mechanics. 
    def cardIntellect(self):
        # Checks if there is no card available
        if self.hand.length() == 0:
            return "nil"
        else:
            likelihoodTable = []
            for card in self.hand.getArray():
                likelihoodTable.append(card.likelihood)
            
            randomNumber = random.uniform(0, sum(likelihoodTable))
            for i in range(len(likelihoodTable)):
                randomNumber -= likelihoodTable[0]
                if randomNumber <= 0:
                    return i
                
            return len(likelihoodTable) - 1
    
    ## Defines the round-start behavior 
    def roundStart(self):
        ## Clears arrays
        self.pocket.clear()
        self.draw.clear()
        self.hand.clear()
        self.discard.clear()
        self.play.clear()
        self.intoHand.clear()
        self.intoIntoHand.clear()
        
        ## Resets elements of Cards that should not have carried over between Rounds
        # for card in self.deck.getArray():
        #     card.foreverLinger = False
        #     card.lingering = 0
        #     card.shelled = False
        
        ## Shuffles deck
        self.deck.shuffle()
        
        ## Initializes cards in all locations
        topDraw = h.cardLocation("")
        unsetDraw = h.cardLocation("")
        bottomDraw = h.cardLocation("")
        muck = h.cardLocation("")
        for deckCard in self.deck.array:
            card = copy.deepcopy(deckCard)
            if card.initialized == "Draw":
                unsetDraw.append(card)
            elif card.initialized == "Top":
                topDraw.append(card)
            elif card.initialized == "Bottom":
                bottomDraw.append(card)
            elif card.initialized == "Muck":
                muck.append(card)
            elif card.initialized == "Into Hand":
                self.intoHand.append(card)
            elif card.initialized == "Discard":
                self.discard.append(card)
            elif card.initialized == "Pocket":
                self.pocket.append(card)
            else:
                input("ERROR!")
                input(str(card.name) + " has no valid initialization location!")
        ## Adds Cards to deck
        for card in topDraw.getArray():
            self.draw.append(card)
        for card in unsetDraw.getArray():
            self.draw.append(card)
        for card in muck.getArray():
            self.draw.append(card)
        for card in bottomDraw.getArray():
            self.draw.append(card)

        ## Updates upcoming plus Action and plus Card
        self.upcomingPlusAction = copy.deepcopy(self.resetUpcomingPlusAction)
        self.upcomingPlusCard = copy.deepcopy(self.resetUpcomingPlusCard)

        ## Draws new cards for the first Hand
        totalDeckDraw = self.deckDraw
        if len(self.upcomingPlusCard) > 0:
            totalDeckDraw += self.upcomingPlusCard.pop(0)

        priorLength = -1
        while ((self.hand.lengthExcludingFeathery() + self.pocket.lengthExcludingFeathery()) < totalDeckDraw
                and self.hand.length() != priorLength):
            priorLength = self.hand.length()
            self.drawCard()

        ## Resets action count 
        self.actions = self.nextTurnActionCount()

        ## Heals
        if self.hp.isDeathHealthcons == True:
            self.hp = ""
            self.hp = cll.Healthcons(self.healR, self.healG, self.healB, 'nil')

            self.dead = False

        else:
            self.hp.r += self.healR
            self.hp.g += self.healG
            self.hp.b += self.healB
            
        ## Resets variables
        self.turn = 0

        ## Logs
        log.roundStartEntityLog(self)
    
    def roundEndTidying(self):
        pass
    
    def turnEndTidying(self, dino, enemies, passedInVisuals):
        ## Discards all cards that should be removed from hand
        while (self.hand.isEmpty() == False):
            self.discardCard(self.hand, 0, dino, enemies, passedInVisuals, moments = [r.AtTurnEndTidying()])
    
        ## Discards all cards that should be removed from play
        i = 0
        size = self.play.length()
        for j in range(size):
            card = self.play.at(i)
            if card.lingering <= 0 and card.foreverLinger == False:
                self.shelled = False
                self.discardCard(self.play, i, dino, enemies, passedInVisuals, moments = [r.AtTurnEndTidying()])
            else:
                i += 1
                card.lingering -= 1
                card.turnsLingering += 1

        ## Draws new cards for the next hand
        totalDeckDraw = self.nextHandDrawCount()
        priorLength = -1
        while ((self.hand.lengthExcludingFeathery() + self.pocket.lengthExcludingFeathery()) < totalDeckDraw
                and self.hand.length() != priorLength):
            priorLength = self.hand.length()
            self.drawCard()

        ## Resets action count 
        self.actions = self.nextTurnActionCount()

        ## Reset all once-a-turn variables
        self.didOnceATurnAtTriggerNonfatalDamageTaken = False
        self.didOnceATurnAtTriggerDinoPlayedCard = False
        self.didOnceATurnAtTriggerTurnStart = False
        self.dealtDamageThisTurn = False
        self.canGainActionsThisTurn = True

        for card in self.getLocations():
            card.resetCardState_TurnEnd()

    def takeAnotherTurnQuery(self):
        if self.extraTurnQueued and not self.onExtraTurn and (self.deadCardPlays == True or self.dead == False):
            h.splash("'" + self.name + "' has a 2nd Turn to take.")
            self.onExtraTurn = True
            self.extraTurnQueued = False
            return True
        else:
            self.onExtraTurn = False
            self.extraTurnQueued = False
            return False

    def plusExtraTurn(self):
        if self.extraTurnQueued or self.onExtraTurn:
            h.splash("FAIL_EXTRA_TURN")
        self.extraTurnQueued = True

    ## Finds a card and returns the matching card location; returns False if unsuccessful.
    def findMe(self, card):
        locations = self.getIterableOfLocations()
        for location in locations:
            if card in location.getArray():
                return location
        return False

    ## Given a specific Card, tries to find it, and then moves it. Returns True if successful. 
    def moveMe(self, fromLocation, card, toLocation, position = 0, printCard = False, inputCard = False, supressFailText = False):
        index = h.locateCardIndex(fromLocation, card)
        if index >= 0 and card.shelled == False:
            self.moveCard(fromLocation, index, toLocation, position = position, printCard = printCard, inputCard = inputCard)
            return True

        if not supressFailText:
            h.splash('FAIL_MOVE')
        return False

    def playMe(self, fromLocation, card, caster, dino, enemies, passedInVisuals, overrideToLocation = "null", supressFailText = False):
        index = h.locateCardIndex(fromLocation, card)
        if index >= 0:
            self.playCard(fromLocation, index, caster, dino, enemies, passedInVisuals, overrideToLocation = overrideToLocation)
        elif supressFailText:
            h.splash('FAIL_MOVE')

    def discardMe(self, fromLocation, card, dino, enemies, passedInVisuals, moments = None):
        if moments == None:
            moments = []

        success = self.moveMe(fromLocation, card, self.discard)
        if success:
            r.reactionStack = r.reactStack([
                r.reactionWindow([r.DiscardedCard(fromLocation, card)] + moments)
            ])
            r.reactionStack.react(dino, enemies, passedInVisuals)

    ## Given a selected index, plays that Card. 
    def playCard(self, fromLocation, cardIndex, caster, dino, enemies, passedInVisuals, overrideToLocation = "null"):
        ## Logging
        log.playCardLog(self, fromLocation, cardIndex, caster, dino, enemies)

        ## Can we play this Card or is it <<inoperable>>?
        if tk.checkTokensOnThis(fromLocation.at(cardIndex), [tk.inoperable()]):
            if fromLocation.name == "hand" or fromLocation.name == "pocket":
                h.splash('FAIL_ATTEMPT_PLAY_INOPERABLE')
                return

        ## Where are we playing this Card to?
        if overrideToLocation == "null":
            card = self.moveCard(fromLocation, cardIndex, self.play, position = self.play.length())
        else:
            card = self.moveCard(fromLocation, cardIndex, overrideToLocation)

        ## Reaction window for before the Card's resolution
        # r.reactionStack = r.reactStack([
        #     r.reactionWindow([r.BeforeCardPlayResolution(card)])
        # ])
        # r.reactionStack.react(dino, enemies, passedInVisuals)

        ## Does this token have a <<prepare>> token?
        if tk.checkTokensOnThis(card, [tk.prepare()]):
            caster.plusActions(1)
            card.removeToken(tk.prepare())

        ## ----- Calls the onPlay of the Card -----
        card.onPlay(caster, dino, enemies, passedInVisuals)

        ## Reaction window for after the Card's resolution
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.AfterCardPlayResolution(card)])
        ])
        r.reactionStack.react(dino, enemies, passedInVisuals)

        ## Resets state after playing a Card
        for entity in enemies + [dino]:
            for card in entity.getLocations():
                card.resetCardState_AfterAnyCardResolves()

    ## Given a select index, resolves the packing text of that Card.
    def packCard(self, fromLocation, cardIndex, caster, dino, enemies, passedInVisuals, overrideToLocation = "null"):
        ## Where are we playing this Card to?
        if overrideToLocation == "null":
            # We move in nowhere, but still need access to this card
            card = fromLocation.at(cardIndex)
        else:
            card = self.moveCard(fromLocation, cardIndex, overrideToLocation)

        ## ----- Calls the onPacking of the Card -----
        card.onPacking(caster, dino, enemies, passedInVisuals)

        ## Resets state after playing a Card
        for entity in enemies + [dino]:
            for card in entity.getLocations():
                card.resetCardState_AfterAnyCardResolves()

    ## Given a fromLocation, toLocation, and shuffleLocation, 
    ##  takes a random card from the fromLocation (unless empty, wherein reshuffle with shuffleLocation),
    ##  putting it into the toLocation.
    ##  Defaults to: fromLocation - draw // toLocation - hand // shuffleLocation - discard
    ##  Returns either 'empty' or the Card, depending. 
    def drawCard(self, fromLocation = 'DEFAULT', toLocation = 'DEFAULT', shuffleLocation = 'DEFAULT', printCard = False, inputCard = False):
        ## -- sets default locations --
        if fromLocation == 'DEFAULT':
            fromLocation = self.draw
        if toLocation == 'DEFAULT':
            toLocation = self.hand
        if shuffleLocation == 'DEFAULT':
            shuffleLocation = self.discard
        if shuffleLocation == 'NONE':
            shuffleLocation = h.cardLocation("Nothing")
        
        ## -- does the drawing --
        ## Reshuffles if need be. 
        if (fromLocation.length() == 0 and shuffleLocation.length() > 0):
            if (self.enemy == False):
                input("   " + Fore.MAGENTA + " Triggered a Shuffle" + Fore.WHITE + "... ")
            shuffleLocation.shuffleTriggeredByDraw()
            for i in range(shuffleLocation.length()):
                fromLocation.append(shuffleLocation.at(i))
            shuffleLocation.clear()
        
        ## Moves the Card. 
        if (fromLocation.length() > 0):
            card = self.moveCard(fromLocation, 0, toLocation, position = toLocation.length(), printCard = printCard, inputCard = inputCard)
            
            return card
        else:
            return "empty"
    
    def destroyCard(self, location, index):
        location.pop(index)
    
    def printMovedCard(self, card, locationName, booleanPrint):
        text = h.colorize(" | During Resolution: Moved ^" + card.name + "^ to " + locationName + ". ")
        if booleanPrint:
            print(text)
        else:
            input(text)

    ## Gains a Card. 
    def gainCard(self, card, toLocation, position = 0, printCard = False, inputCard = False):
        fantasy = h.cardLocation("fantasy")
        fantasy.append(card)
        self.moveCard(fantasy, 0, toLocation, position, printCard, inputCard)

    def gainCopyOfCard(self, card, toLocation, position = 0, printCard = False, inputCard = False):
        fantasy = h.cardLocation("fantasy")
        cardCopy = copy.deepcopy(card)
        fantasy.append(cardCopy)
        self.moveCard(fantasy, 0, toLocation, position, printCard, inputCard)


    ## Moves a card from one location to another
    ## Throws an error if that card in the fromLocation does not exist
    ## Adds the item to a specific position if wanted -- position = 0 is the bottom of the toLocation, so toLocation.length() would be the top of the location (meaning soonest to be drawn next). 
    ## ANY TIME A CARD MOVES IT MUST PASS THROUGH THIS!!!
    ## Returns the moved Card. 
    def moveCard(self, fromLocation, cardIndex, toLocation, position = 0, printCard = False, inputCard = False):
        if cardIndex < fromLocation.length() and position <= toLocation.length():
            movingCard = fromLocation.at(cardIndex)

            # Moved Cards always turn this into False
            movingCard.existingOnPlay = False

            fromLocation.pop(cardIndex)
            toLocation.insert(position, movingCard)

            if printCard == True or inputCard == True:
                booleanPrint = printCard
                self.printMovedCard(movingCard, toLocation.niceName(), booleanPrint)
            return movingCard

        else:
            print(" FATAL ERROR!!! moveCard did not succeed. ")
            print("  Card Index: ", cardIndex)
            print("  From Location: ", fromLocation.name)
            print("  Boolean if position <= len(toLocation): ", str(position <= toLocation.length()))
            input(" ... ")
            print(0/0)
    
    ## Moves a card from one location to another, but specifically discards it 
    ##  (meaning it goes into the discard). 
    ## Returns the discarded Card. 
    def discardCard(self, fromLocation, cardIndex, dino, enemies, passedInVisuals, moments = None, printCard = False, inputCard = False):
        if moments == None:
            moments = []

        movedCard = self.moveCard(fromLocation, cardIndex, self.discard, printCard = printCard, inputCard = inputCard)

        ## Run any special on-discard triggers
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.DiscardedCard(fromLocation, movedCard)] + moments)
        ])
        r.reactionStack.react(dino, enemies, passedInVisuals)

    '''
    ## From a set of cards, allows user to draft 1 of them, adding them to the toLocation.
    ##  Returns the drafted card. 
    def draftCard(self, draftPool, draftPoolPulls, toLocation, bonusGuarenteedPulls = [], supressedTypes = []):
        print(" -- Drafting to <<" + toLocation.niceName() + ">> --")
        if draftPoolPulls == 0 or (draftPool.length() == 0 and len(bonusGuarenteedPulls) == 0):
            print(draftPool.length())
            input(" Attempted to draft cards, but Pulls: " + str(draftPoolPulls) + " and draftPool: " + str(draftPool) + " and bonusGuarenteedPulls: " + str(bonusGuarenteedPulls))
            return
        
        draftPoolCopy = h.cardLocation("")
        for card in draftPool.getArray():
            draftPoolCopy.append(copy.deepcopy(card))
            
        picks = h.cardLocation("")
        for i in range(draftPoolPulls):
            if draftPoolCopy.length() > 0:
                picks.append(draftPoolCopy.pop(random.randint(0, draftPoolCopy.length() -1)))
                print(" " + str(i + 1) + ". " 
                        + Back.CYAN + Style.BRIGHT + " " + picks.at(i).name + " "
                        + Back.RESET + Style.NORMAL 
                        + h.normalize("", 41 - 5 - len(str(i+1)) - len(picks.at(i).name) - 3) + ":  "
                        + picks.at(i).niceBodyText(41, h.WIDTH, supressedTypes))
                ## print(h.normalize("", 41 - 3) + ".")
        for card in bonusGuarenteedPulls:
            picks.append(card)
        
        index = h.pickValue("Pick a Card", range(1, picks.length() + 1)) - 1
        pickedCard = picks.pop(index)
        toLocation.append(pickedCard)
        return pickedCard
    '''
    
    def plusUpcomingPlusCard(self, when, count):
        if len(self.upcomingPlusCard) < when + 1:
            self.upcomingPlusCard.append(0)
            self.plusUpcomingPlusCard(when, count)
        else:
            self.upcomingPlusCard[when] += count

    def publishPermanentPlusCard(self, when, count):
        if len(self.resetUpcomingPlusCard) < when + 1:
            self.resetUpcomingPlusCard.append(0)
            self.publishPermanentPlusCard(when, count)
        else:
            self.resetUpcomingPlusCard[when] += count

    def plusUpcomingPlusAction(self, when, count):
        if len(self.upcomingPlusAction) < when + 1:
            self.upcomingPlusAction.append(0)
            self.plusUpcomingPlusAction(when, count)
        else:
            self.upcomingPlusAction[when] += count

    def publishPermanentPlusAction(self, when, count):
        if len(self.resetUpcomingPlusAction) < when + 1:
            self.resetUpcomingPlusAction.append(0)
            self.publishPermanentPlusAction(when, count)
        else:
            self.resetUpcomingPlusAction[when] += count

    # Attempts to give + Action, ignoring under specific debuffs
    def plusActions(self, plusActions):
        if self.canGainActionsThisTurn:
            self.actions += plusActions
    
    # Attempts to give - Action, ignoring under specific debuffs
    def minusActions(self, minusActions):
        self.actions -= minusActions
        self.actions = max(self.actions, 0)
    
    def turnStart(self):
        self.turn += 1
    
    def atTriggerTurnStart(self, dino, enemies):
        pass
    
    def atTriggerTurnEnd(self, dino, enemies):
        pass
    
    def atTriggerLoseBand(self, dino, enemies):
        pass
    
    def atTriggerAnyEnemyNonfatallyDamaged(self, damageTaker, dino, enemies):
        pass
    
    def atTriggerEnemySummoned(self, summonedEnemy, dino, enemies):
        pass
    
    def atTriggerDinoPlayedCard(self, dino, enemies):
        pass
    
    def r(self):
        return self.hp.r
    
    def g(self):
        return self.hp.g

    def b(self):
        return self.hp.b
    
    def getBands(self):
        if self.hp == 'nil':
            return 0
        else:
            return self.hp.getBands()
        
    def getDisplayName(self):
        returnText = self.name + " "
        if self.enemy == True:
            if self.actions == 0 or self.hand.length() == 0:
                returnText += "//"
        return returnText
    
    def destroyBand(self, dino, enemies):
        if self.hp.getBands() > 0:
            self.hp = self.hp.tail
            self.atTriggerLoseBand(dino, enemies)
        self.upkeepHealth(dino, enemies)

    ## Stores information about damage dealt, returned byt damage
    ## Static class
    class damageData():
        def __init__(self):
            ## Stores attributes to cross-compare after damage is dealt
            self.fatalDamage = False
            self.brokeABand = False

    def damage(self, caster, dino, enemies, AttackData):
        ## Entity value for if any damage was dealt this turn
        caster.dealtDamageThisTurn = True

        ## Creates a new damageData, and creates variables used to populate it
        DamageData = self.damageData()
        alreadyDead = False
        beforeBandCount = self.getBands()

        ## Deals damage, and runs all channels through rounding just in case
        self.__damage(caster, dino, enemies, AttackData)
        if self.hp != 'nil':
            self.hp.r = h.roundThird(self.hp.r) 
            self.hp.g = h.roundThird(self.hp.g) 
            self.hp.b = h.roundThird(self.hp.b) 

        ## Performs upkeep
        self.upkeepHealth(dino, enemies)

        ## Compares the stored attributes against what occurred, populating DamageData
        if not alreadyDead:
            DamageData.fatalDamage = self.dead
        if beforeBandCount > self.getBands():
            DamageData.brokeABand = True

        ## Reaction window for after attacking
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.AfterEntityAttacked(self, caster, AttackData, DamageData)])
        ])
        r.reactionStack.react(dino, enemies, vis.prefabEmpty())

        ## Resets flags (are these even needed?)
        self.nonfatalDamageTaken = False
        self.bandBreak = False

        ## Resets reaction states of CARDS
        for card in caster.getLocations():
            card.resetCardState_AfterAfterEntityAttacked()

        return DamageData

    ## Returns R, G, B, R-notick, G-notick, or B-notick, given a chl value of the set of all chl values
    def getRGBChannel(self, caster, dino, enemies, chl):
        channels = [self.r(), self.g(), self.b()]
        colorset = ['R', 'G', 'B']

        if chl == 'Notnil':
            possibleChl = []
            for i in range(3):
                if channels[i] > 0:
                    possibleChl.append(colorset[i])
            chl = possibleChl[random.randint(0, len(possibleChl) - 1)]

        if chl == 'Random':
            chl = colorset[random.randint(0, 2)]

        if chl == 'Random-notick':
            chl = colorset[random.randint(0, 2)] + "-notick"

        if chl == 'L':
            possibleChl = []
            lowestValue = float('inf')
            for i in range(3):
                if channels[i] > 0 and channels[i] < lowestValue:
                    lowestValue = channels[i]
            if self.r() == lowestValue:
                possibleChl.append('R')
            if self.g() == lowestValue:
                possibleChl.append('G')
            if self.b() == lowestValue:
                possibleChl.append('B')

            chl = possibleChl[random.randint(0, len(chl) - 1)]

        if chl == 'M':
            possibleChl = []
            highestValue = max(channels)
            if self.r() == highestValue:
                possibleChl.append('R')
            if self.g() == highestValue:
                possibleChl.append('G')
            if self.b() == highestValue:
                possibleChl.append('B')

            if len(possibleChl) == 1:
                chl = possibleChl[0]
            else:
                chl = possibleChl[random.randint(0, len(possibleChl) - 1)].upper()

        ## In the case we have R, R-notick, G, G-notick, B, or B-notick,
        ##  the chl is already the correct core-6 channel type!
        return chl

    ## Sets the health of the entity to a new value
    def setHP(self, newHealthcons):
        self.hp = newHealthcons

    ## Heals!
    def heal(self, caster, dino, enemies, AttackData):
        self.upkeepHealth(dino, enemies)
        if AttackData == 'nil':
            return
        if self.getBands() == 0:
            self.hp = cll.Healthcons(0, 0, 0, 'nil')

        dmg = AttackData.damage
        chl = AttackData.channel
        
        chl = self.getRGBChannel(caster, dino, enemies, chl)
        
        if chl == 'R' or chl == 'R-notick':
            self.hp.r += dmg
        elif chl == 'G' or chl == 'G-notick':
            self.hp.g += dmg
        elif chl == 'B' or chl == 'B-notick':
            self.hp.b += dmg
        
        self.heal(caster, dino, enemies, AttackData.tail)
    
    ## Deals damage!
    ##  Checks if this creature is dead, and if the AttackData is just 'nil'.
    def __damage(self, caster, dino, enemies, AttackData):
        if AttackData == 'nil':
            return
        if self.dead == True:
            return

        dmg = AttackData.damage
        chl = AttackData.channel

        if chl == 'Row':
            self.__takeRDamage(dmg, dino, enemies, notick = True)
            self.__takeGDamage(dmg, dino, enemies, notick = True)
            self.__takeBDamage(dmg, dino, enemies, notick = True)
        else:
            chl = self.getRGBChannel(caster, dino, enemies, chl)

            if chl == 'R':
                self.__takeRDamage(dmg, dino, enemies)
            elif chl == 'R-notick':
                self.__takeRDamage(dmg, dino, enemies, notick = True)
            elif chl == 'G':
                self.__takeGDamage(dmg, dino, enemies)
            elif chl == 'G-notick':
                self.__takeGDamage(dmg, dino, enemies, notick = True)
            elif chl == 'B':
                self.__takeBDamage(dmg, dino, enemies)
            elif chl == 'B-notick':
                self.__takeBDamage(dmg, dino, enemies, notick = True)

        ## Iterates
        AttackData = AttackData.tail
        self.__damage(caster, dino, enemies, AttackData)

    ## For taking R-channel damage
    def __takeRDamage(self, dmg, dino, enemies, notick = False):
        self.upkeepHealth(dino, enemies)
        if self.dead or (dmg == 0) or self.bandBreak:
            return

        if self.hp.r > 0:
            self.hp.r = max(self.hp.r - dmg, 0)
        elif self.hp.g > 0 and notick == False:
            self.hp.g = max(self.hp.g - 1, 0)
        elif self.hp.b > 0 and notick == False:
            self.hp.b = max(self.hp.b - 1, 0)
        self.upkeepHealth(dino, enemies)

    ## For taking G-channel damage
    def __takeGDamage(self, dmg, dino, enemies, notick = False):
        self.upkeepHealth(dino, enemies)
        if self.dead or (dmg == 0) or self.bandBreak:
            return

        if self.hp.g > 0:
            self.hp.g = max(self.hp.g - dmg, 0)
        elif self.hp.b > 0 and notick == False:
            self.hp.b = max(self.hp.b - 1, 0)
        elif self.hp.r > 0 and notick == False:
            self.hp.r = max(self.hp.r - 1, 0)
        self.upkeepHealth(dino, enemies)

    ## For taking B-channel damage
    def __takeBDamage(self, dmg, dino, enemies, notick = False):
        self.upkeepHealth(dino, enemies)
        if self.dead or (dmg == 0) or self.bandBreak:
            return

        if self.hp.b > 0:
            self.hp.b = max(self.hp.b - dmg, 0)
        elif self.hp.r > 0 and notick == False:
            self.hp.r = max(self.hp.r - 1, 0)
        elif self.hp.g > 0 and notick == False:
            self.hp.g = max(self.hp.g - 1, 0)
        self.upkeepHealth(dino, enemies)

    ## Checks if all bands of this row are zeros AND if hp is only now "nil",
    ##  changing the value of self.dead accordingly
    def upkeepHealth(self, dino, enemies):
        self.nonfatalDamageTaken = True
        if self.hp == "nil":
            self.dead = True
            self.diedThisTurn = True
            self.nonfatalDamageTaken = False
            self.hp = cll.DeadHealthcons()
            return True
        elif self.hp.r == 0 and self.hp.g == 0 and self.hp.b == 0:
            self.hp = self.hp.tail
            self.bandBreak = True
            self.atTriggerLoseBand(dino, enemies)
            return self.upkeepHealth(dino, enemies)
        else:
            return False
    
    ## Makes it so you can break a band
    def publishBandBreak(self, number, discardHand = False, special = False):
        count = 0
        if (discardHand):
            count += 1
        if (special):
            count += 1
        if count > 1:
            print("ERROR!!! Tried to add a band break, but attempted to add multiple!")
            print(0/0)
        
        self.hp.publishBandBreak(number, discardHand, special)

























































## Creates the Dinosaur
class Dinosaur(Entity):
    def __init__(self):
        super().__init__()
        self.name = "Dinosaur"
        self.hp = cll.Healthcons(3, 3, 3, 'nil')
        self.enemy = False
        self.deckDraw = 4
        self.actions = 2
        self.upkeepActions = 2

        self.looting = 0
        self.uptickLooting = 1

        self.healR = 1
        self.healG = 1
        self.healB = 1

        self.resetR = 4 - self.healR
        self.resetG = 4 - self.healG
        self.resetB = 4 - self.healB

        ## Text explaining what happens when you pass on looting
        self.passedLootingInfoText = "When passing on Looting or a Shop, you may: Destroy a Card from Deck."

    def passedLooting(self, clearingName, roundCount, lootTables, pullsTable, picksTable, incrementTable):
        ## h.splash("When passing as '" + self.name + "', you may: Destroy a Card from Deck.", printInsteadOfInput = True)
        query = h.yesOrNo("Destroy a Card from Deck?")
        if query:
            pickedValue = h.pickValue("Destroy a Card", picksTable) - 1

            offset = 0
            priorOffset = -1
            while offset != priorOffset:
                priorOffset = offset
                offset = sum(incrementTable[0:picksTable[pickedValue] + offset])

            removedCard = self.deck.at(pickedValue + offset)
            self.deck.pop(pickedValue + offset)

            h.splash("Hopefully the ^" + removedCard.name + "^ is best left forgotten...")

        else:
            h.splash("Hopefully all is well with your deck...")

class Rover(Dinosaur):
    def __init__(self):
        super().__init__()
        self.text = "It has been left in the package for a decade, only now free to roam the cruel, changing, crying world. //Special Gimmick: At Turn Start, pockets a 'Petrol Mantra' [+1 Action. All Damage arrays you deal this turn are now the M channel.]"
        self.name = "Rover"

        cards = gcbt.getCardsByTable(["Packing Bot"])
        for card in cards.getArray():
            self.deck.append(card)
        for i in range(4):
            self.deck.append(gcbt.getCardByName("Junk"))

class Graverobber(Dinosaur):
    def __init__(self):
        super().__init__()
        self.text = "As a scrappy dinosaur, maybe there is something out in the beyond that can sedate its wandering soul."
        self.name = "Graverobber"

        cards = gcbt.getCardsByTable(["Graverobber"])
        for card in cards.getArray():
            self.deck.append(card)
        for i in range(2):
            self.deck.append(gcbt.getCardByName("Junk"))
        self.deckDraw = 0
        ## self.deck.append(gcbt.getCardByName("miscellany"))

    def turnEndTidying(self, dino, enemies, passedInVisuals):
        for i in range(24):
            self.plusUpcomingPlusCard(i, 1)
        super().turnEndTidying(dino, enemies, passedInVisuals)

class Shepherd(Dinosaur):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Shepherd"

        cards = gcbt.getCardsByTable(["Shepherd"])
        for card in cards.getArray():
            self.deck.append(card)
        for i in range(3):
            self.deck.append(gcbt.getCardByName("Junk"))

'''
class HungryWolf(Dinosaur):
    def __init__(self):
        super().__init__()
        self.name = "Hungry Wolf"
    
    def roundStart(self):
        self.plusUpcomingPlusCard(0, 1)
        super().roundStart()
    
class Weewarrasaurus(Dinosaur):
    def __init__(self):
        super().__init__()
        self.name = "Weewarrasaurus"
        
    def atTriggerTurnStart(self, dino, enemies):    
        self.didOnceATurnAtTriggerTurnStart = True
        h.splash("Triggered innate turn start ability:", printInsteadOfInput = True)
        query = h.yesOrNo("Discard Hand for +3 Cards?")
        if query == True:
            size = len(dino.hand)
            for i in range(size):
                dino.discardCard(dino.hand, 0, dino, enemies, passedInVisuals)
            for i in range(3):
                dino.drawCard() 
'''

## Creates the general Enemies
class Enemy(Entity):
    def __init__(self):
        super().__init__()

    ## THE IMPLEMENTATION OF EXTRA DRAFTS ALSO NEEDS AN ODDS NUMBER OR SOMETHING
    def fillDeck(self, extraDrafts = h.cardLocation("extra drafts")):
        EFD = h.cardLocation("EFD")

        ## Pre-processing, finding all cards that are reasonable-enough matches
        for Card in gcbt.ENEMY_CARD_POOL_UNINIT:
            card = Card(targetDamage = self.damageDist, targetSift = self.siftDist)
            deltaDamage = (card.damageDist - self.damageDist)
            deltaSift = (card.siftDist - self.siftDist)
            if (math.sqrt(deltaDamage ** 2 + deltaSift ** 2) <= 0.8):
                EFD.append(card)

        ## Adds extra drafts to the list too
        for card in extraDrafts.getArray():
            EFD.append(card)

        ## Selects cards randomly, and if they pass a probability check, adds them
        while (self.deck.length() < 6):
            if EFD.length() == 0:
                # Case where we cannot add any more Cards
                self.deck.append(gcbt.getCardByName("Nothing"))
            else:
                card = EFD.pop(random.randint(0, EFD.length() - 1))

                deltaDamage = (card.damageDist - self.damageDist)
                deltaSift = (card.siftDist - self.siftDist)

                if (random.random() >= math.sqrt(deltaDamage ** 2 + deltaSift ** 2)):
                    # We passed the randomness check -- adds this Card to the selection
                    self.deck.append(card)
                else:
                    # We failed the randomness check -- tries again
                    EFD.append(card)


        '''
        ## Fills the EFD with valid cards from the enemyFillDeck and all cards from extraDrafts
        EFD = h.cardLocation("EFD")
        for card in ec.enemyFillDeck.getArray():
            deltaDamage = (card.damageDist - self.damageDist)
            deltaSift = (card.siftDist - self.siftDist)
            delta = math.sqrt(deltaDamage ** 2 + deltaSift ** 2)
            if (delta <= 0.8):
                EFD.append(card)
        for card in extraDrafts.getArray():
            EFD.append(card)

        ## Picks those cards randomly, and makes them available for the enemies
        while (self.deck.length() < 6):
            if EFD.length() == 0: # Case where we have no more attacks to add
                self.deck.append(ec.nothing())
            else:
                randomCard = EFD.pop(random.randint(0, EFD.length() - 1))

                deltaDamage = (randomCard.damageDist - self.damageDist)
                deltaSift = (randomCard.siftDist - self.siftDist)
                delta = math.sqrt(deltaDamage ** 2 + deltaSift ** 2)

                if (random.random() >= delta):
                    self.deck.append(randomCard)
                else:
                    EFD.append(randomCard)

        self.deck.shuffle()
        '''







'''
class Litterbugs(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Loiterers of nearby grime and filth, both in body and morality."
        self.name = "Litterbugs"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 0.75
        self.siftDist = 1
        super().fillDeck()
        
        self.difficulty = 1
    
    def __healthInit(self):
        hpA = [0.3, 0, 0]
        random.shuffle(hpA)
        hpB = [2, 1, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))
'''

class plainEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A plain Enemy."
        self.name = "Enemy"
        self.initialEnemyName = self.name

        self.damageDist = -1
        self.siftDist = -1

        self.difficulty = -1

    def plainEnemyInit(self, name, difficulty, damageDist, targetHealth, siftDist):
        super().__init__()
        self.text = "A plain Enemy."
        self.name = name
        self.initialEnemyName = self.name

        self.damageDist = damageDist
        self.siftDist = siftDist
        super().fillDeck()

        self.targetHealth = targetHealth
        self.hp = cll.Healthcons(0, 0, 0, 'nil')
        self.plainEnemyHealthInit(self.hp, targetHealth)

        self.difficulty = difficulty

    def plainEnemyHealthInit(self, hp, target):
        ## print(" -------------- ")
        self.__hpStart(hp, target)

    def __hpStart(self, hp, target):
        ## input("S: " + str(target))
        channels = [hp.r, hp.g, hp.b]
        if (target <= 0 and not max(channels) == 0):
            return

        if (target <= 0 and max(channels) == 0) or (target == 1):
            chl = random.randint(0, 2)
            if chl == 0:
                hp.r = 1
            elif chl == 1:
                hp.g = 1
            else:
                hp.b = 1
            return
        else:
            return self.__hpContinue(hp, target)

    def __hpContinue(self, hp, target):
        ## input("C: " + str(target))
        if target <= 0:
            return

        channels = [hp.r, hp.g, hp.b]
        emptyChannels = 0
        for chl in channels:
            if chl == 0:
                emptyChannels += 1

        if emptyChannels == 3:
            return self.__hpInset(hp, target)
        elif emptyChannels == 0:
            return self.__hpBand(hp, target)

        elif emptyChannels == 1:
            if random.random() < (0.85 / 2):
                return self.__hpInset(hp, target)
            return self.__hpBand(hp, target)
        else:
            if random.random() < 0.85:
                return self.__hpInset(hp, target)
            return self.__hpBand(hp, target)

    def __hpInset(self, hp, target):
        ## input("I: " + str(target))
        channels = [hp.r, hp.g, hp.b]
        emptyChannels = []
        pos = 0
        for chl in channels:
            if chl == 0:
                emptyChannels.append(pos)
            pos += 1
        chl = random.randint(0, len(emptyChannels) - 1)

        if chl == 0:
            hp.r = 1
            target -= 1
            while target > 0 and random.random() < 0.5:
                hp.r += 1
                target -= 1
        elif chl == 1:
            hp.g = 1
            target -= 1
            while target > 0 and random.random() < 0.5:
                hp.g += 1
                target -= 1
        else:
            hp.b = 1
            target -= 1
            while target > 0 and random.random() < 0.5:
                hp.b += 1
                target -= 1
        return self.__hpContinue(hp, target)

    def __hpBand(self, hp, target):
        ## input("B: " + str(target))
        target -= 1
        hp.tail = cll.Healthcons(0, 0, 0, 'nil')
        return self.__hpStart(hp.tail, target)

class Fisherman(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Ravenous Fisherman"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Crave Fish Mantra"))
        self.damageDist = 1.8
        self.siftDist = 0.75
        super().fillDeck()

        self.difficulty = 3

    def __healthInit(self):
        hpA = [1, 1, 2]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class FishingCaravan(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Fishing Caravan"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Fish Frenzy"))
        if random.random() < 0.25:
            self.deck.append(gcbt.getCardByName("Fish Frenzy"))
            if random.random() < 0.1:
                self.deck.append(gcbt.getCardByName("Fish Frenzy"))
        self.damageDist = 1.35
        self.siftDist = 1.25
        super().fillDeck()

        self.difficulty = 6.75

    def __healthInit(self):
        hpA = [0, 2, 2]
        random.shuffle(hpA)
        hpB = [0, 2, 2]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

class FlyingSquirrel(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Flying Squirrel"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Prepare To Fly"))
        self.damageDist = 0.8
        self.siftDist = 1.2
        super().fillDeck()

        self.difficulty = 3

    def __healthInit(self):
        hpA = [2, 2, 2]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')


class MalabarGiantSquirrel(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Malabar Giant Squirrel"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Going Nuts"))
        self.damageDist = 1
        self.siftDist = 1
        super().fillDeck()

        self.difficulty = 2.75

    def __healthInit(self):
        hpA = [5, 0, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class Copperals(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Small copper critters, fighting for what is right."
        self.name = "Copperals"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.damageDist = 0.75
        self.siftDist = 1
        super().fillDeck()

        self.difficulty = 2

    def __healthInit(self):
        hpA = [2, 2, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class Rusterials(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "The forgotten, disillusioned, and angry."
        self.name = "Rusterials"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        self.publishBandBreak(1, discardHand = True)

        self.damageDist = 2
        self.sistDist = 1
        super().fillDeck()

        self.difficulty = 4.75

    def __healthInit(self):
        hpA = [4, 2, 0]
        hpB = [1, 0, 0]
        random.shuffle(hpA)
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)

class Karkit(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A baby Skunk."
        self.name = "Karkit"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.damageDist = 0.75
        self.siftDist = 1.5
        super().fillDeck()

        self.difficulty = 0.75

    def __healthInit(self):
        hpA = [2, 0, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class Skunk(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "They reek."
        self.name = "Skunk"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 1
        self.siftDist = 1.25
        super().fillDeck()
        
        self.difficulty = 1.75
    
    def __healthInit(self):
        hpA = [1, 0, 0]
        random.shuffle(hpA)
        hpB = [2, 2, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

class RaccoonBandit(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Bandits of the Night, first you must unmask them in order to chase them away."
        self.name = "Raccoon Bandit"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        ## self.publishBandBreak(1, discardHand = True)
    
        self.damageDist = 1.25
        self.siftDist = 1.25
        super().fillDeck()
        
        self.difficulty = 2.75
    
    def __healthInit(self):
        hpA = [2, 0, 0]
        random.shuffle(hpA)
        hpB = [2, 0, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))
    
    ''' def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)
    '''

## Hoard of Shrews
class HoardOfShrews(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A Legion of Shrews, jealous of each other, far more feral in a pack than alone."
        self.name = "Hoard Of Shrews"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        self.publishBandBreak(1, discardHand = True)

        self.damageDist = 1.45
        self.siftDist = 1
        super().fillDeck()
        
        self.difficulty = 2.75
    
    def __healthInit(self):
        hpA = [2, 1, 0]
        random.shuffle(hpA)
        hpB = [2, 1, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))
    
    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)

## Shrew -- A timid creature, easily frightened. 
class Shrew(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A timid creature, easily frightened."
        self.name = "Shrew"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.damageDist = 0.67
        self.siftDist = 0.5
        super().fillDeck()

        self.difficulty = 1.75

    def __healthInit(self):
        hpA = [2, 1, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')
    
    def atTriggerTargetedToTakeDamage(self, dino, enemies):
        chance = random.random()
        if (chance <= 0.1 and not self.dead):
            h.splash("Triggered Gimmick: [ 0.1 Chance when Targeted to Take Damage ] ARR [ Discard Hand ].")
            while (self.hand.length() > 0):
                self.discardCard(self.hand, 0, dino, enemies, vis.prefabEmpty)

## Torch Bear -- It calls to the wild for apostles of the new order. 
class CinnamonBear(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "It calls to the wild for apostles of what can become of a New Order; only 'Shrews' heed the call."
        self.name = "Torch Bearer"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        self.publishBandBreak(1, discardHand = True)

        self.deck.append(gcbt.getCardByName("Soapbox Stump"))
        self.damageDist = 1.1
        self.siftDist = 1.1
        super().fillDeck()
        
        self.difficulty = 7.25

    def __healthInit(self):
        hp = [0, 2, 3]
        random.shuffle(hp)
        return cll.Healthcons(hp[0], hp[1], hp[2], cll.Healthcons(hp[2], hp[1], hp[0], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)

## Babybear -- The upcoming new beneficiary, disillusioned by how small of land they shall inherit. 
class Babybear(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "The upcoming new beneficiary, disillusioned by how small of a land they shall inherit."
        self.name = "Babybear"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(gcbt.getCardByName("Demanding Inheritance"))
        self.damageDist = 1
        self.siftDist = 1
        super().fillDeck()
        
        self.difficulty = 1.45
    
    def __healthInit(self):
        hp = [3, 0, 0]
        random.shuffle(hp)
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')



"""
## Torchbearer -- Eventually, its facade of leadership and pride shall falter, in which its once-was followers will turn on it. 
class Torchbearer(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "It gives off a boastful presence, at least until it falls from its prideful rock and is turned on by its once-were followers. //Special Gimmick: At Turn End, if 'Torchbearer' has 2 Bands: 'Torchbearer' gets 1 additional Action next turn. //Special Gimmick: When 'Torchbearer' loses a Band, -1 Actions, and per each living Enemy: self-damage 2M."
        self.name = "Torchbearer"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 1
        self.siftDist = 0.5
        super().fillDeck()
        
        self.difficulty = 8

    def __healthInit(self):
        hpA = [2, 2, 0]
        random.shuffle(hpA)
        hpB = [2, 2, 2]
        
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Triggered Special Gimmick: When 'Torchbearer' loses a Band, -1 Actions, and per each living Enemy: self-damage 2M.")
            self.minusActions(1)
            count = 0
            for enemy in enemies:
                if enemy.dead == False:
                    count += 1
            for i in range(count):
                self.damage(self, dino, enemies, cll.Attackcons([2, 'M'], 'nil'))
    
    def atTriggerTurnEnd(self, dino, enemies):
        if self.getBands() == 2:
            h.splash("Triggered Special Gimmick: At Turn End, if 'Torchbearer' has 2 Bands: 'Torchbearer' gets 1 additional Action next turn.")
            self.plusUpcomingPlusAction(0, 1)
    
## Discarded Plastic -- 
##  Focus: Helps with +Actions, hurts medium sifting. 
class DiscardedPlastic(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Discarded Plastic"
        self.initialEnemyName = self.name 
        self.hp = self.__healthInit()
        
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
    
        self.difficulty = 1
    
    def __healthInit(self):
        return cll.Healthcons(0, 0, 0, 'nil')
    
    def atTriggerDinoPlayedCard(self, dino, enemies):
        if len(dino.play) > 1 and self.didOnceARoundAtTriggerDinoPlayedCard == False and self.dead == False:
            self.didOnceARoundAtTriggerDinoPlayedCard = True
            h.splash("Triggered Special Gimmick: Once a Round, while 'Discarded Plastic' is Alive: if '" + str(dino.name) + "' has more than 1 Card in play: Dino gains 'To-Toss Plastic,' and draws 1 additional Card next Turn.")
            dino.discard.append(gcbt.getCardByName("To-Toss Plastic"))
            dino.plusUpcomingPlusCard(0, 1)

## Grizzly -- More than any other bear does it despise what has come of the species. 
class Grizzly(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "More than any other Bear does it despise what has come of the species. //Special Gimmick: While Alive, at Turn End, 'Grizzly' heals 1L and self-damages 1M."
        self.name = "Grizzly"
        self.initialEnemyName = self.name 
        self.hp = self.__healthInit()
        
        self.damageDist = 1.25
        self.siftDist = 0.8
        super().fillDeck()
        
        self.difficulty = 7

    def __healthInit(self):
        hp = [0, 2, 4]
        random.shuffle(hp)
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')
    
    ''' def atTriggerTurnEnd(self, dino, enemies):
        if self.dead == False:
            # h.splash("Triggered Special Gimmick: While Alive, at Turn End, 'Grizzly' heals 1L and self-damages 1M.")
            self.heal(self, dino, enemies, cll.Attackcons([1, 'L'], 'nil'))
            self.damage(self, dino, enemies, cll.Attackcons([1, 'M'], 'nil')) '''
    
## Shrew -- A small, puny rodent, easily frightened. 
class Shrew(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A small, puny rodent, trying to be courageous."
        self.name = "Shrew"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.musterCourage())
        self.damageDist = 0.6
        self.siftDist = 0.6
        super().fillDeck()
        
        self.difficulty = 1

    def __healthInit(self):
        hp = [0, 0, 0]
        hp[random.randint(0, 2)] = 1
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

## Belly-Filled Shrew -- That small, puny rodent, now full of grass in its stomach. 
class BellyFilledShrew(Shrew):
    def __init__(self):
        super().__init__()
        self.name = "Belly-Filled Shrew"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 0.7
        self.siftDist = 0.5
        super().fillDeck()
        
        self.difficulty = 1.5
    
    def __healthInit(self):
        hp = [0, 0, 0]
        hp[random.randint(0, 2)] = 2
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

## Enshrined Capybara -- Enveloped in metal, with metal-sharpened teeth. 
##  Special Gimmick: When it loses a band and only has 1 remaining, it discards its hand. 
class EnshrinedCapybara(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Enveloped in thin metal, with metal-sharpened teeth. //Special Gimmick: When 'Enshrined Capybara' loses a Band and has only 1 left, it discards its hand."
        self.name = "Enshrined Capybara"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.twoMetalTeeth())
        self.deck.append(ec.frightened1())
        self.damageDist = 0.3
        self.siftDist = 0.3
        super().fillDeck()
        
        self.difficulty = 4.75
    
    def __healthInit(self):
        hpA = [0, 0, 0]
        hpA[random.randint(0, 2)] = 1
        
        hpB = [2, 2, 2]
        hpB[random.randint(0, 2)] = 0
        return cll.Healthcons(hpA[0], hpA[1], hpA[2],
            cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Triggered Special Gimmick: 'Enshrined Capybara' lost a Band and has only 1 left, so: discard Hand.")
            size = len(self.hand)
            for i in range(size):
                self.moveCard(self.hand, 0, self.discard)

## Prairie Watch Dog -- Defends its kind with its life. 
class PrairieWatchDog(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "It defends its kind with its life. //Special Gimmick: Once a Turn, while 'Prairie Watch Dog' is alive: when an Enemy is damaged non-fatally: +1 Action, play a Card from Hand, and self-damage 1M."
        self.name = "Prairie Watch Dog"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 0.85
        self.siftDist = 0.45
        super().fillDeck()
        
        self.difficulty = 2

    def __healthInit(self):
        hp = [1, 1, 1]
        hp[random.randint(0, 2)] = 0
        
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

    def atTriggerAnyEnemyNonfatallyDamaged(self, damageTaker, dino, enemies):
        if self.didOnceATurnAtTriggerNonfatalDamageTaken == False and self.dead == False:
            h.splash("Triggered Special Gimmick: Once a Turn, while 'Prairie Watch Dog' is alive: when an Enemy is damaged non-fatally: +1 Action, play a Card from Hand, and self-damage 1M.")
            self.didOnceATurnAtTriggerNonfatalDamageTaken = True
            
            self.plusActions(1)
            cardIndex = self.cardIntellect()
            if cardIndex != "nil":
                card = self.hand[cardIndex]
                print(" | Resolution of: " + Back.RED + Fore.BLACK + " " + card.name + " ")
                print(" |  > " + card.niceBodyText(3, 100))
                input(" | ... ")
                self.playCard(self.hand, cardIndex, self, dino, enemies)
            else:
                h.splash("It could not play any Cards.")
        
            self.damage(self, dino, enemies, cll.Attackcons([1, 'M'], 'nil'))

## Squirrel Researcher -- Trying to better understand this forsaken place. 
class SquirrelResearcher(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Trying to better understand this forsaken place."
        self.name = "Squirrel Researcher"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.yellowPadResearch())
        self.deck.append(ec.loosePapers())
        self.damageDist = 1.5
        self.siftDist = 0.5
        super().fillDeck()
        
        self.difficulty = 3

    def __healthInit(self):
        hp = [1, 1, 1]
        hp[random.randint(0, 2)] = 2
        
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.difficulty = 5

class TheMoltOfHundreds(BossEnemy):
    def __init__(self):
        super().__init__()
        self.text = "The nectar of a sun-melted Mech lured the naive who believed its false promise of immortality."
        self.name = "The Molt of Hundreds!"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.shearedCreature())
        self.damageDist = 2
        self.siftDist = 0.5
        super().fillDeck()
        
    def __healthInit(self):
        hpA = [2, 2, 2]
        
        hpB = [2, 2, 2]
        hpB[random.randint(0, 2)] = 0

        hpC = [0, 0, 0]
        hpC[random.randint(0, 2)] = 2
        
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 
            cll.Healthcons(hpB[0], hpB[1], hpB[2], 
                cll.Healthcons(hpC[0], hpC[1], hpC[2], 'nil')))

    def atTriggerLoseBand(self, dino, enemies):
        h.splash("Triggered Special Gimmick: Lost a Band, so: Summoning a 'Shrew.'")
        summonedEnemy = Shrew()
        summonedEnemy.roundStart()
        enemies.append(summonedEnemy)
        for enemy in enemies:
            enemy.atTriggerEnemySummoned(summonedEnemy, dino, enemies)
"""







'''
DISPLAY = True

if DISPLAY:
    print("--" + " -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
    print("  " + " -- ENEMY NAME --              | -- TEXT --")
    ## Lists out all Enemy Cards
    for child in DinoCard.__subclasses__():
        if any(i in child().table for i in TABLES) or not(ONLY_SPECIFIC_TABLES):
            print("  " + h.normalize(child().name, 31) + ":  " 
                + child().niceBodyText(36, 120))
'''