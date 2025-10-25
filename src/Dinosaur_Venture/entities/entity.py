"""
entity.py

Represents a general-purpose entity, if that be the player or the enemy.
"""

import copy
import random
from typing import TYPE_CHECKING

from colorama import Back, Fore, Style, init

init(autoreset=True)
from Dinosaur_Venture import cardTokens as tk
from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import gameplay_logging as log
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis
from Dinosaur_Venture import react as r

if TYPE_CHECKING:
    from Dinosaur_Venture import card as c

class Entity():
    """
    Implementation of that entity.

    Attributes:
        ## --- Identification ----
        index (int): the location of this entity as it relates to the clearing.
        name (string): the name of the entity.
        initialEnemyName (string): the initial name of the entity in case it changes.
        text (string): flavor blurb explaining the entity.

        ## --- Card Locations ---
        deck (cardLocation): the entity's deck.
        draw (cardLocation): the entity's draw pile.
        hand (cardLocation): the entity's hand.
        discard (cardLocation): the entity's discard pile.
        play (cardLocation): the entity's play area.
        intoHand (cardLocation): cards in the 'into-hand' location.
        intoIntoHand (cardLocation): cards in the 'into-into-hand' location.
        pocket (cardLocation): the entity's pocket pile.

        ## --- Health and Healing ---
        hp (Healthcons): the HP.
        healR (int): passive R healing at Round Start.
        healG (int): passive G healing at Round Start.
        healB (int): passive B healing at Round Start.
        uptickResetR (int): how much more to heal at each Rest Stop. 
        uptickResetG (int): how much more to heal at each Rest Stop. 
        uptickResetB (int): how much more to heal at each Rest Stop. 
        resetR (int): reset value of R at a Rest Stop.
        resetG (int): reset value of G at a Rest Stop.
        resetB (int): reset value of B at a Rest Stop.

        ## --- Action and Card Draw Management ---
        actions (int): action count.
        upkeepActions (int): ignoring edge cases, how many +actions at the start of turn.
        canGainActionsThisTurn (bool): if the entity can gain actions this turn.
        upcomingPlusAction (list[int]): how many extra actions to gain on the ith turn.
        resetUpcomingPlusAction (list[int]): what to reset upcomingPlusAction to at Round End.

        deckDraw (int): ignoring edge cases, how many cards to draw at end/start of turn.
        upcomingPlusCard (list[int]): how many extra cards to draw on the ith turn.
        resetUpcomingPlusCard (list[int]): what to reset upcomingPlusCard to at Round End.

        ## --- Enemy Initializer and Information ---
        damageDist (int): how much damage an enemy's deck should deal. See clearing.py.
        siftDist (int): how much sifting an enemy's deck should have. See clearing.py.
        difficulty (int): how difficult of an enemy this is. See clearing.py.
        enemy (bool): if this entity is an enemy.

        ## --- Stored Attributes ---
        deadCardPlays (bool): if this entity while dead still palys cards.
        bandBreak (bool): if a band was broken by a current damage source.
        dealtDamageThisTurn (bool): if any damage was performed by this entity.
        diedThisTurn (bool): if this entity died this turn.
        turn (int): the number of turns this entity has taken.
        extraTurnQueued (bool): if an extra turn is queued.
        onExtraTurn (bool): if the entity is currently on an extra turn.
        dead (bool): if the entity is dead.
        cmfDepot (list[cmf.card_mod_function]): list of things that modify card_functions.
        
        ## --- Rest Stop Information ---
        looting (int): how many cards this entity will loot at a Rest Stop. See clearing.py.
        uptickLooting (int): adds that amount of self.looting at the end of Rest Stop.
        skipNextShop (bool): if the next shop will be skipped.

    Notes:
        `upkeepActions` and `upcomingPlusAction` are cumulative, as in the entity will gain both
            at the start of turn. 
        If `bandBreak` == True, further damage from the current damage string is negated.
            Reset at the end of dealing damage.
        `dealtDamageThisTurn` = True even if the damage dealt was 0 like with '0R / 0G / 0B.'
        Functionality depends on the specific string names of the card locations (ie, 'deck').
    """
    def __init__(self):
        # Index in the enemy list
        self.index = 0
        # Presented name and stored name 
        self.name = ""
        self.initialEnemyName = ""
 
        self.text = ""

        self.looting = 1

        self.damageDist = 1
        self.siftDist = 1

        # How difficult the enemy is to face.
        #   Look for information in 'clearing.py'
        self.difficulty = 1
        
        # Enemy and isDinosaur are exclusive; do not change this value by other commands
        self.enemy = True

        # The health of the enemy; should be overridden in inheritance
        self.hp = cll.DeadHealthcons()

        # The deck zones
        # Do not change these names! Functionality depends on reading the names of these locations
        self.deck = h.cardLocation('deck')

        self.draw = h.cardLocation('draw')
        self.hand = h.cardLocation('hand')
        self.discard = h.cardLocation('discard')
        self.play = h.cardLocation('play')
        self.intoHand = h.cardLocation('into-hand')
        self.intoIntoHand = h.cardLocation('into-into-hand')
        self.pocket = h.cardLocation('pocket')

        # Card Handler Functions, which allow the overriding of cardFunctions functionality
        self.cmfDepot = []

        # Action count
        self.actions = 1
        # How many Actions are gained at the start of each turn
        self.upkeepActions = 1
        self.canGainActionsThisTurn = True

        # At each Round Start, passively heals from each channel this much 
        self.healR = 0
        self.healG = 0
        self.healB = 0
        # At each Rest Stop, increases the resetR, resetG, and resetB by this much
        self.uptickResetR = 0
        self.uptickResetG = 0
        self.uptickResetB = 0
        # At Rest Stop, sets R, G, and B to be these values
        self.resetR = 0 - self.healR
        self.resetG = 0 - self.healG
        self.resetB = 0 - self.healB

        # At the end of Rest, adds this many looting to looting
        self.uptickLooting = 1
        # If we are skipping the next shop
        self.skipNextShop = False

        # Tracks the upcoming values 
        self.upcomingPlusCard = []
        self.upcomingPlusAction = []
        # What these are reset to
        self.resetUpcomingPlusCard = []
        self.resetUpcomingPlusAction = []

        # Number of Cards to draw for a new Hand.
        self.deckDraw = 2

        # If dead
        self.dead = False
        # If, even while dead, the entity can play Cards
        self.deadCardPlays = False

        # Tracks if a band was broken from a damage source currently -- if True, negates further damage
        self.bandBreak = False

        # Tracks if the entity has done any damage (even if that damage dealt was 0)
        self.dealtDamageThisTurn = False

        # Tracks if the enemy died this turn -- reset at Turn End
        self.diedThisTurn = False

        # Number of turns this entity has taken
        self.turn = 0
        # Do we have another turn incoming?
        self.extraTurnQueued = False
        # Are we on an extra turn?
        self.onExtraTurn = False
    
    def getLocations(self) -> list["h.cardLocation"]:
        """Returns all locations (excluding deck) concatenated."""
        locations = self.getIterableOfLocations()
        returnArray = []
        for location in locations:
            returnArray += location.getArray()

        return returnArray

    def getIterableOfLocations(self) -> list["c.Card"]:
        """Returns all cards in all locations (excluding deck) concatenated."""
        array = []
        array.append(self.pocket)
        array.append(self.hand)
        array.append(self.intoHand)
        array.append(self.intoIntoHand)
        array.append(self.discard)
        array.append(self.play)
        array.append(self.draw)
        return array

    def enemyTurnDinoDeathCheck(self) -> None:
        """Run to fix dino if they are dead; likely no longer needed."""
        if self.getBands() == 0:
            self.hp = cll.DeadHealthcons()
    
    def dinoTurnDinoDeathCheck(self, roundCount: int) -> None:
        """
        Checks if dino is dead on dino's turn.
        
        Raises a RuntimeError if dead; change this functionality later.
        """
        if self.getBands() == 0:
            input(Fore.RED + " !!! !!! !!!" + Fore.WHITE)
            input(self.name + " has run out of power :(")
            print("Areas traversed: " + str(roundCount + 1))
            print("Cards in deck:")
            for card in self.deck.getArray():
                print(" | " + Back.CYAN + Style.BRIGHT + card.name)

            raise RuntimeError("Game over!")
    
    def nextHandDrawCount(self, simplyObserve: bool = False) -> int:
        """
        Fetches how many cards will be drawn on the Next Turn.
        
        Arguments:
            simplyObserve: will not modify any internal data structures.

        Notes:
            If the `nextHandDrawCount` is a negative number, will return 0.
        """
        totalDeckDraw = self.deckDraw
        if len(self.upcomingPlusCard) > 0:
            if simplyObserve:
                totalDeckDraw += self.upcomingPlusCard[0]
            else:
                totalDeckDraw += self.upcomingPlusCard.pop(0)
        return max(0, totalDeckDraw)

    def nextTurnActionCount(self, simplyObserve: bool = False) -> int:
        """
        Fetches how many actions will be gained on the Next Turn.
        
        Arguments:
            simplyObserve: will not modify any internal data structures.

        Notes:
            Can possibly return a negative value.
        """
        actionCount = self.upkeepActions
        if len(self.upcomingPlusAction) > 0:
            if simplyObserve:
                actionCount += self.upcomingPlusAction[0]
            else:
                actionCount += self.upcomingPlusAction.pop(0)
        return actionCount

    def cardIntellect(self) -> any:
        """
        For enemies, handles the logic for cards to be played. 
        Does so randomly, weighted by `self.likelihood` values.

        Can be overridden by other entities for more/less intelligent card selection.
        
        Returns:
            Either 'nil' (if no card gets selected) or the index of the selected card.
        """
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
    
    def roundStart(self) -> None:
        """Handles Round Start behavior."""
        # Clears arrays
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
        
        # Shuffles deck
        self.deck.shuffle()
        
        # Initializes cards in all locations
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
        
        # Adds Cards to deck
        for card in topDraw.getArray():
            self.draw.append(card)
        for card in unsetDraw.getArray():
            self.draw.append(card)
        for card in muck.getArray():
            self.draw.append(card)
        for card in bottomDraw.getArray():
            self.draw.append(card)

        # Updates upcoming plus Action and plus Card
        self.upcomingPlusAction = copy.deepcopy(self.resetUpcomingPlusAction)
        self.upcomingPlusCard = copy.deepcopy(self.resetUpcomingPlusCard)

        # Draws new cards for the first Hand
        totalDeckDraw = self.deckDraw
        if len(self.upcomingPlusCard) > 0:
            totalDeckDraw += self.upcomingPlusCard.pop(0)

        priorLength = -1
        while ((self.hand.lengthExcludingFeathery() + self.pocket.lengthExcludingFeathery()) < totalDeckDraw
                and self.hand.length() != priorLength):
            priorLength = self.hand.length()
            self.drawCard()

        # Resets action count 
        self.actions = self.nextTurnActionCount()

        # Heals
        if self.hp.isDeathHealthcons == True:
            self.hp = ""
            self.hp = cll.Healthcons(self.healR, self.healG, self.healB, 'nil')

            self.dead = False

        else:
            self.hp.r += self.healR
            self.hp.g += self.healG
            self.hp.b += self.healB
            
        # Resets variables
        self.turn = 0

        # Logs
        log.round_start_entity_log(self)
    
    def roundEndTidying(self) -> None:
        """Handles Round End behavior."""
        pass
    
    def turnEndTidying(
        self,
        dino: "Entity",
        enemies: list["Entity"],
        passedInVisuals: vis.prefabPassedInVisuals) -> None:
        """Handles the very end of Turn End behavior."""
        # Discards all cards that should be removed from hand
        while (self.hand.isEmpty() == False):
            self.discardCard(self.hand, 0, dino, enemies, passedInVisuals, moments = [r.AtTurnEndTidying()])
    
        # Discards all cards that should be removed from play
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

        # Draws new cards for the next hand
        totalDeckDraw = self.nextHandDrawCount()
        priorLength = -1
        while ((self.hand.lengthExcludingFeathery() + self.pocket.lengthExcludingFeathery()) < totalDeckDraw
                and self.hand.length() != priorLength):
            priorLength = self.hand.length()
            self.drawCard()

        # Resets action count 
        self.actions = self.nextTurnActionCount()

        # Reset all once-a-turn variables
        self.dealtDamageThisTurn = False
        self.canGainActionsThisTurn = True

        for card in self.getLocations():
            card.resetCardState_TurnEnd()

    def takeAnotherTurnQuery(self) -> bool:
        """At Turn End, sees if an extra turn is in order, returning True if the case."""
        if self.extraTurnQueued and not self.onExtraTurn and (self.deadCardPlays == True or self.dead == False):
            h.splash("'" + self.name + "' has a 2nd Turn to take.")
            self.onExtraTurn = True
            self.extraTurnQueued = False
            return True
        else:
            self.onExtraTurn = False
            self.extraTurnQueued = False
            return False

    def plusExtraTurn(self) -> None:
        """Preps to take an extra turn if possible."""
        if self.extraTurnQueued or self.onExtraTurn:
            h.splash("FAIL_EXTRA_TURN")
        self.extraTurnQueued = True

    def findMe(self, card: "c.Card") -> bool:
        """Finds a card and returns the matching card location; returns False if unsuccessful."""
        locations = self.getIterableOfLocations()
        for location in locations:
            if card in location.getArray():
                return location
        return False

    def moveMe(
        self,
        fromLocation: h.cardLocation,
        card: "c.Card",
        toLocation: h.cardLocation,
        position: int = 0,
        printCard: bool = False,
        inputCard: bool = False,
        suppressFailText: bool = False
    ) -> bool:
        """
        Given a specific Card, tries to find it, and then moves it. Returns True if successful.
        
        Arguments:
            fromLocation: the location where the card is imagined to be located.
            card: said card.
            toLocation: the location where the card will be moved to.
            position: the index where the card will be moved to in the toLocation.
            printCard: if the moved card's information should be printed.
            inputCard: if the moved card's information should be shown via `input()`.
            suppressFailText: if the move is unsuccessful, if we should ignore the FAIL_MOVE text.
        """
        index = h.locateCardIndex(fromLocation, card)
        if index >= 0 and card.shelled == False:
            self.moveCard(
                fromLocation, 
                index, 
                toLocation, 
                position = position, 
                printCard = printCard, 
                inputCard = inputCard
            )
            return True

        if not suppressFailText:
            h.splash('FAIL_MOVE')
        return False

    def playMe(
        self, 
        fromLocation: h.cardLocation,
        card: "c.Card", 
        caster: "Entity", 
        dino: "Entity", 
        enemies: list["Entity"], 
        passedInVisuals: vis.prefabPassedInVisuals, 
        overrideToLocation: h.cardLocation | str = "null", 
        suppressFailText: bool = False
    ) -> None:
        """
        Given a specific Card, tries to find it, and then plays it.
        
        Arguments:
            fromLocation: the location where the card is imagined to be located.
            card: said card.
            caster: who is playing this card.
            dino: dino.
            enemies: the list of enemies.
            passedInVisuals: the visuals.
            overrideToLocation: if this card will not be played to `caster.play`.
                If not "null," expected parameter is a `h.cardLocation`.
            suppressFailText: if unsuccessful, if we should ignore the FAIL_MOVE text.
        """
        index = h.locateCardIndex(fromLocation, card)
        if index >= 0:
            self.playCard(
                fromLocation, 
                index, 
                caster, 
                dino, 
                enemies, 
                passedInVisuals, 
                overrideToLocation = overrideToLocation
            )
        elif suppressFailText:
            h.splash('FAIL_MOVE')

    def discardMe(
        self,
        fromLocation: h.cardLocation,
        card: "c.Card",
        dino: "Entity",
        enemies: list["Entity"],
        passedInVisuals: vis.prefabPassedInVisuals,
        moments: list[r.reactMoments] = None
    ) -> None:
        """
        Given a specific Card, tries to find it, and then discards it.
        
        Arguments:
            fromLocation: the location where the card is imagined to be located.
            card: said card.
            dino: dino.
            enemies: the list of enemies.
            passedInVisuals: the visuals.
            moments: list of current `r.reactMoments` for the purpose of reactions.

        Note:
            As opposed to `moveMe` where the toLocation is 'discard', this function calls
                unique triggers based on the fact the card was specifically "discarded".
        """
        if moments == None:
            moments = []

        success = self.moveMe(fromLocation, card, self.discard)
        if success:
            r.reactionStack = r.reactStack([
                r.reactionWindow([r.DiscardedCard(fromLocation, card)] + moments)
            ])
            r.reactionStack.react(dino, enemies, passedInVisuals)

    # Given a selected index, plays that Card. 
    def playCard(
        self,
        fromLocation: h.cardLocation,
        cardIndex: int, 
        caster: "Entity", 
        dino: "Entity", 
        enemies: list["Entity"], 
        passedInVisuals: vis.prefabPassedInVisuals, 
        overrideToLocation: h.cardLocation | str = "null", 
    ) -> None:
        """
        Given a selected index, plays that Card.
                
        Arguments:
            fromLocation: the location where the card is imagined to be located.
            cardIndex: index of the card to play.
            caster: who is playing this card.
            dino: dino.
            enemies: the list of enemies.
            passedInVisuals: the visuals.
            overrideToLocation: if this card will not be played to `caster.play`.
                If not "null," expected parameter is a `h.cardLocation`.
        """
        # Logging
        log.play_card_log(self, fromLocation, cardIndex, caster, dino, enemies)

        # Can we play this Card or is it <<inoperable>>?
        if tk.checkTokensOnThis(fromLocation.at(cardIndex), [tk.inoperable()]):
            if fromLocation.name == "hand" or fromLocation.name == "pocket":
                h.splash('FAIL_ATTEMPT_PLAY_INOPERABLE')
                return

        # Where are we playing this Card to?
        if overrideToLocation == "null":
            card = self.moveCard(fromLocation, cardIndex, self.play, position = self.play.length())
        else:
            card = self.moveCard(fromLocation, cardIndex, overrideToLocation)

        ## Reaction window for before the Card's resolution
        # r.reactionStack = r.reactStack([
        #     r.reactionWindow([r.BeforeCardPlayResolution(card)])
        # ])
        # r.reactionStack.react(dino, enemies, passedInVisuals)

        # Does this token have a <<prepare>> token?
        if tk.checkTokensOnThis(card, [tk.prepare()]):
            caster.plusActions(1)
            card.removeToken(tk.prepare())

        ## ----- Calls the onPlay of the Card -----
        card.onPlay(caster, dino, enemies, passedInVisuals)

        # Reaction window for after the Card's resolution
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.AfterCardPlayResolution(card)])
        ])
        r.reactionStack.react(dino, enemies, passedInVisuals)

        # Resets state after playing a Card
        for entity in enemies + [dino]:
            for card in entity.getLocations():
                card.resetCardState_AfterAnyCardResolves()

    def packCard(
        self,
        fromLocation: h.cardLocation,
        cardIndex: int, 
        caster: "Entity", 
        dino: "Entity", 
        enemies: list["Entity"], 
        passedInVisuals: vis.prefabPassedInVisuals, 
        overrideToLocation: h.cardLocation | str = "null", 
    ) -> None:
        """
        Given a selected index, resolves the packing text of that Card.
        
        Arguments:
            fromLocation: the location where the card is imagined to be located.
            cardIndex: index of the card to play.
            caster: who is playing this card.
            dino: dino.
            enemies: the list of enemies.
            passedInVisuals: the visuals.
            overrideToLocation: if this card will not be played to `caster.play`.
                If not "null," expected parameter is a `h.cardLocation`.
        """
        # Where are we playing this Card to?
        if overrideToLocation == "null":
            # We move in nowhere, but still need access to this card
            card = fromLocation.at(cardIndex)
        else:
            card = self.moveCard(fromLocation, cardIndex, overrideToLocation)

        ## ----- Calls the onPacking of the Card -----
        card.onPacking(caster, dino, enemies, passedInVisuals)

        # Resets state after playing a Card
        for entity in enemies + [dino]:
            for card in entity.getLocations():
                card.resetCardState_AfterAnyCardResolves()

    def drawCard(
        self,
        fromLocation: h.cardLocation | str = 'DEFAULT', 
        toLocation: h.cardLocation | str = 'DEFAULT', 
        shuffleLocation: h.cardLocation | str = 'DEFAULT', 
        printCard: bool = False, 
        inputCard: bool = False
    ) -> any:
        """
        Given a fromLocation, toLocation, and shuffleLocation, moves the next card from the fromLocation
        (unless empty, wherein we reshuffle with shuffleLocation), putting it into the toLocation.
        
        Arguments:
            fromLocation: the location where we draw from.
            toLocation: the location where we draw to.
            shuffleLocation: if the fromLocation is empty, shuffles these cards into the fromLocation.
            printCard: if the moved card's information should be printed.
            inputCard: if the moved card's information should be shown via `input()`.

        Returns:
            Either 'empty' or the Card, depending if a Card was drawn.
    
        Notes:
            If a location == 'DEFAULT', we draw from the following locations:
                fromLocation: 'draw'
                toLocation: 'hand'
                shuffleLocation: 'discard'
            If shuffleLocation == 'NONE', reshuffles nothing.

 
        """
        
        ## ----- sets default locations -----
        if fromLocation == 'DEFAULT':
            fromLocation = self.draw
        if toLocation == 'DEFAULT':
            toLocation = self.hand
        if shuffleLocation == 'DEFAULT':
            shuffleLocation = self.discard
        if shuffleLocation == 'NONE':
            shuffleLocation = h.cardLocation("Nothing")
        
        ## ----- does the drawing -----
        # Reshuffles if need be. 
        if (fromLocation.length() == 0 and shuffleLocation.length() > 0):
            if (self.enemy == False):
                input("   " + Fore.MAGENTA + " Triggered a Shuffle" + Fore.WHITE + "... ")
            shuffleLocation.shuffleTriggeredByDraw()
            for i in range(shuffleLocation.length()):
                fromLocation.append(shuffleLocation.at(i))
            shuffleLocation.clear()
        
        # Moves the Card. 
        if (fromLocation.length() > 0):
            card = self.moveCard(
                fromLocation, 
                0, 
                toLocation, 
                position = toLocation.length(), 
                printCard = printCard,
                inputCard = inputCard
            )
        
            return card
        else:
            return "empty"
    
    def destroyCard(self, location: h.cardLocation, index: int) -> None:
        """Destroys the card at the index of the location."""
        location.pop(index)
    
    def printMovedCard(self, card: "c.Card", locationName: h.cardLocation, booleanPrint: bool):
        """
        Handles UI for moving a card when printed.
        
        If booleanPrint == True, prints the UI element, otherwise `input()` it.
        """
        text = h.colorize(" | During Resolution: Moved ^" + card.name + "^ to " + locationName + ". ")
        if booleanPrint:
            print(text)
        else:
            input(text)

    def gainCard(
        self, 
        card: "c.Card", 
        toLocation: h.cardLocation, 
        position: int = 0, 
        printCard: bool = False, 
        inputCard: bool = False
    ) -> None:
        """Gains a Card to the to location at the given position."""
        fantasy = h.cardLocation("fantasy")
        fantasy.append(card)
        self.moveCard(fantasy, 0, toLocation, position, printCard, inputCard)

    def gainCopyOfCard(
        self, 
        card: "c.Card", 
        toLocation: h.cardLocation, 
        position: int = 0, 
        printCard: bool = False, 
        inputCard: bool = False
    ) -> None:
        """
        Gains a copy of a Card to the to location at the given position.
        
        Effectively the same as `gainCard` except this will `copy.deepcopy` the other card.
        """
        fantasy = h.cardLocation("fantasy")
        cardCopy = copy.deepcopy(card)
        fantasy.append(cardCopy)
        self.moveCard(fantasy, 0, toLocation, position, printCard, inputCard)

    def moveCard(
        self,
        fromLocation: h.cardLocation,
        cardIndex: int,
        toLocation: h.cardLocation,
        position: int = 0,
        printCard: bool = False,
        inputCard: bool = False,
    ) -> "c.Card":
        """
        Moves a card from one location to another; any time a card moves, it should move using this function.
        Returns the moved card.

        Arguments:
            fromLocation: the location where the card is imagined to be located.
            cardIndex: the index of the card to move.
            toLocation: the location where the card will be moved to.
            position: the index where the card will be moved to in the toLocation.
            printCard: if the moved card's information should be printed.
            inputCard: if the moved card's information should be shown via `input()`.
        
        Errors:
            Raises a RuntimeError if the card cannot be moved.
        """
        if cardIndex < fromLocation.length() and position <= toLocation.length():
            movingCard = fromLocation.at(cardIndex)

            fromLocation.pop(cardIndex)
            toLocation.insert(position, movingCard)

            if printCard == True or inputCard == True:
                booleanPrint = printCard
                self.printMovedCard(movingCard, toLocation.niceName(), booleanPrint)
            return movingCard

        else:
            raise RuntimeError(
                "moveCard did not succeed;" +
                " Card Index: " + str(cardIndex) +
                " From Location: " + fromLocation.name + 
                " Boolean if position <= len(toLocation): ", str(position <= toLocation.length()))
    
    def discardCard(
        self,
        fromLocation: h.cardLocation,
        cardIndex: int,
        dino: "Entity",
        enemies: list["Entity"],
        passedInVisuals: vis.prefabPassedInVisuals,
        moments: list[r.reactMoments] = None,
        printCard: bool = False,
        inputCard: bool = False
    ) -> "c.Card":
        """
        Given a specific cardIndex, tries to find it a card at that index and discard it.
        
        Arguments:
            fromLocation: the location where the card is imagined to be located.
            cardIndex: the index of the card to move.
            dino: dino.
            enemies: the list of enemies.
            passedInVisuals: the visuals.
            moments: list of current `r.reactMoments` for the purpose of reactions.
            printCard: if the moved card's information should be printed.
            inputCard: if the moved card's information should be shown via `input()`.

        Note:
            As opposed to `moveCard` where the toLocation is 'discard', this function calls
                unique triggers based on the fact the card was specifically "discarded".
        """
        if moments == None:
            moments = []

        movedCard = self.moveCard(fromLocation, cardIndex, self.discard, printCard = printCard, inputCard = inputCard)

        # Run any special on-discard triggers
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.DiscardedCard(fromLocation, movedCard)] + moments)
        ])
        r.reactionStack.react(dino, enemies, passedInVisuals)

    def plusUpcomingPlusCard(self, when: int, count: int) -> None:
        """
        Increases hand size `when`-turns in the future by `count.`
        
        Example: `plusUpcomingPlusCard(0, 1)` increase the hand size by 1 on the next turn.
        """
        if len(self.upcomingPlusCard) < when + 1:
            self.upcomingPlusCard.append(0)
            self.plusUpcomingPlusCard(when, count)
        else:
            self.upcomingPlusCard[when] += count

    def publishPermanentPlusCard(self, when: int, count: int) -> None:
        """
        Permanently increases hand size `when`-turns into a round by `count`.
        
        Example: `publishPermanentPlusCard(0, 1)` increase the hand size by 1 on all first turns.
        """
        if len(self.resetUpcomingPlusCard) < when + 1:
            self.resetUpcomingPlusCard.append(0)
            self.publishPermanentPlusCard(when, count)
        else:
            self.resetUpcomingPlusCard[when] += count

    def plusUpcomingPlusAction(self, when: int, count: int) -> None:
        """
        Increases action count `when`-turns in the future by `count.`
        
        Example: `plusUpcomingPlusAction(0, 1)` increase action count by 1 for the next turn.
        """
        if len(self.upcomingPlusAction) < when + 1:
            self.upcomingPlusAction.append(0)
            self.plusUpcomingPlusAction(when, count)
        else:
            self.upcomingPlusAction[when] += count

    def publishPermanentPlusAction(self, when: int, count: int) -> None:
        """
        Permanently increases action count `when`-turns into a round by `count`.
        
        Example: `publishPermanentPlusAction(0, 1)` increase action count by 1 on all first turns.
        """
        if len(self.resetUpcomingPlusAction) < when + 1:
            self.resetUpcomingPlusAction.append(0)
            self.publishPermanentPlusAction(when, count)
        else:
            self.resetUpcomingPlusAction[when] += count

    def plusActions(self, plusActions: int) -> None:
        """Attempts to give + Action, ignoring + Actions under specific debuffs."""
        if self.canGainActionsThisTurn:
            self.actions += plusActions
    
    def minusActions(self, minusActions: int) -> None:
        """Attempts to give - Action, ignoring - Actions under specific debuffs."""
        self.actions -= minusActions
        self.actions = max(self.actions, 0)
    
    def turnStart(self) -> None:
        """Handles start of this entity's turn."""
        self.turn += 1
    
    def atTriggerTurnStart(self, dino, enemies):
        """Special functionality at this moment in gameplay; planned to be deprecated."""
        pass
    
    def atTriggerTurnEnd(self, dino, enemies):
        """Special functionality at this moment in gameplay; planned to be deprecated."""
        pass
    
    def atTriggerLoseBand(self, dino, enemies):
        """Special functionality at this moment in gameplay; planned to be deprecated."""
        pass
    
    def atTriggerAnyEnemyNonfatallyDamaged(self, damageTaker, dino, enemies):
        """Special functionality at this moment in gameplay; planned to be deprecated."""
        pass
    
    def atTriggerEnemySummoned(self, summonedEnemy, dino, enemies):
        """Special functionality at this moment in gameplay; planned to be deprecated."""
        pass
    
    def atTriggerDinoPlayedCard(self, dino, enemies):
        """Special functionality at this moment in gameplay; planned to be deprecated."""
        pass
    
    def r(self) -> int:
        """Returns R health in this current band."""
        return self.hp.r
    
    def g(self) -> int:
        """Returns G health in this current band."""
        return self.hp.g

    def b(self) -> int:
        """Returns B health in this current band."""
        return self.hp.b
    
    def getBands(self) -> int:
        """Returns the number of bands in this entity's HP."""
        if self.hp == 'nil' or self.hp.isDeathHealthcons:
            return 0
        else:
            return self.hp.getBands()
        
    def getDisplayName(self) -> str:
        """Gets name for the purpose of UI."""
        returnText = self.name + " "
        if self.enemy == True:
            if self.actions == 0 or self.hand.length() == 0:
                returnText += "//"
        return returnText
    
    def destroyBand(self, dino: "Entity", enemies: list["Entity"]) -> None:
        """Destroys a band of this enemy's health."""
        if self.hp.getBands() > 0:
            self.hp = self.hp.tail
            self.atTriggerLoseBand(dino, enemies)
        self.upkeepHealth(dino, enemies)

    class DamageData():
        """
        Represents information about damage dealt; returned by `Entity.damage()`.
        
        Attributes:
            fatalDamage: if, during this damage, the entity died.
            brokeABand: if, during this damage, a band was broken.
        """
        def __init__(self):
            self.fatalDamage = False
            self.brokeABand = False

    def damage(
        self, 
        caster: "Entity", 
        dino: "Entity", 
        enemies: list["Entity"], 
        attackData: cll.Attackcons
    ) -> "Entity.DamageData":
        """Deals attackData damage to this entity."""
        # Entity value for if any damage was dealt this turn
        caster.dealtDamageThisTurn = True

        # Creates a new damageData, and creates variables used to populate it
        damageData = self.DamageData()
        alreadyDead = False
        beforeBandCount = self.getBands()

        # Deals damage, and runs all channels through rounding just in case
        self.__damage(caster, dino, enemies, attackData)
        if self.hp != 'nil':
            self.hp.r = h.roundThird(self.hp.r) 
            self.hp.g = h.roundThird(self.hp.g) 
            self.hp.b = h.roundThird(self.hp.b) 

        # Performs upkeep
        self.upkeepHealth(dino, enemies)

        # Compares the stored attributes against what occurred, populating DamageData
        if not alreadyDead:
            damageData.fatalDamage = self.dead
        if beforeBandCount > self.getBands():
            damageData.brokeABand = True

        # Reaction window for after attacking
        r.reactionStack = r.reactStack([
            r.reactionWindow([r.AfterEntityAttacked(self, caster, attackData, damageData)])
        ])
        r.reactionStack.react(dino, enemies, vis.prefabEmpty())

        # Resets flags
        self.bandBreak = False

        # Resets reaction states of cards
        for card in caster.getLocations():
            card.resetCardState_AfterAfterEntityAttacked()

        return damageData

    def getRGBChannel(
        self, 
        caster: "Entity", 
        dino: "Entity", 
        enemies: list["Entity"], 
        chl: str
    ) -> str:
        """
        Based on the input chl value (R, L, Random-notick, etc.), 
            returns one of the following core damage types:
            R, G, B, R-notick, G-notick, or B-notick.    
        """
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

        # In the case we have R, R-notick, G, G-notick, B, or B-notick,
        #   the chl is already the correct core-6 channel type!
        return chl

    def setHP(self, newHealthcons):
        """Sets the health of the entity to a new value."""
        self.hp = newHealthcons

    def heal(
        self, 
        caster: "Entity", 
        dino: "Entity", 
        enemies: list["Entity"], 
        attackData: cll.Attackcons | str
    ) -> None:
        """
        Heals this entity based on the attackData values.
        
        attackData is expected to be a `cll.Attackcons` or 'nil'.
        """
        self.upkeepHealth(dino, enemies)

        if attackData == 'nil':
            return
        if self.getBands() == 0:
            self.hp = cll.Healthcons(0, 0, 0, 'nil')

        dmg = attackData.damage
        chl = attackData.channel
        
        chl = self.getRGBChannel(caster, dino, enemies, chl)
        
        if chl == 'R' or chl == 'R-notick':
            self.hp.r += dmg
        elif chl == 'G' or chl == 'G-notick':
            self.hp.g += dmg
        elif chl == 'B' or chl == 'B-notick':
            self.hp.b += dmg
        
        self.heal(caster, dino, enemies, attackData.tail)
    
    def __damage(
        self,
        caster: "Entity", 
        dino: "Entity",
        enemies: list["Entity"],
        attackData: cll.Attackcons | str
    ) -> None:
        """
        Helper function for dealing damage.
        
        Checks if the creature is dead and if the attackData == 'nil'.
        """
        if attackData == 'nil':
            return
        if self.dead == True:
            return

        dmg = attackData.damage
        chl = attackData.channel

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

        # Iterates
        attackData = attackData.tail
        self.__damage(caster, dino, enemies, attackData)

    def __takeRDamage(self, dmg: int, dino: "Entity", enemies: list["Entity"], notick: bool = False) -> None:
        """For taking R-channel damage."""
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

    def __takeGDamage(self, dmg: int, dino: "Entity", enemies: list["Entity"], notick: bool = False) -> None:
        """For taking G-channel damage."""
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

    def __takeBDamage(self, dmg: int, dino: "Entity", enemies: list["Entity"], notick: bool = False) -> None:
        """For taking B-channel damage."""
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

    def upkeepHealth(self, dino: "Entity", enemies: list["Entity"]) -> bool:
        """
        Checks if all bands of this row are zeros AND or if HP is empty.
        Changes the value of self.dead and turns self.hp to be cll.DeadHealthcons if so.

        Returns True if the entity is dead.
        """
        if self.hp == "nil" or isinstance(self.hp, cll.DeadHealthcons):
            self.dead = True
            self.diedThisTurn = True
            self.hp = cll.DeadHealthcons()
            return True
        elif self.hp.r == 0 and self.hp.g == 0 and self.hp.b == 0:
            self.hp = self.hp.tail
            self.bandBreak = True
            self.atTriggerLoseBand(dino, enemies)
            return self.upkeepHealth(dino, enemies)
        else:
            return False
    
    def publishBandBreak(self, number: int, discardHand: bool = False, special: bool = False) -> None:
        """
        Creates a band break at the number-ith band.
        
        Arguments: 
            number: what band to break, 0-indexed.
            discardHand: if this band break specifically discards hand.
            special: if we have a special, unique band break.
        
        Notes:
            Excepts `discardHand` and `special` to not both be true.
            All calls to `channel_linked_lists.Healthcons.publishBandBreak` should
                be handed through a call to this `Entity` function.
        """
        count = 0
        if (discardHand):
            count += 1
        if (special):
            count += 1
        if count > 1:
            raise RuntimeError("Tried to add a band break," +
                               "but multiple band break types were expected!")
        
        self.hp.publishBandBreak(number, discardHand, special)