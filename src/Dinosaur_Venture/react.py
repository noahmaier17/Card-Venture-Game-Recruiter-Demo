from Dinosaur_Venture import card as c, cardTokens as tk, helper as h

## The reaction stack
reactionStack = []

## An object that contains a pointer to the entity, its type, if it currently is available to react, and its reaction text.
class reactor():
    def __init__(self, caster, aviator, canReact, rt, optional, responseAndTrigger):
        self.caster = caster
        self.aviator = aviator
        self.canReact = canReact
        self.rt = rt
        self.optional = optional
        self.responseAndTrigger = responseAndTrigger

    def resolveTrigger(self, dino, enemies):
        if isinstance(self.aviator, c.Card):
            self.responseAndTrigger.trigger(self.aviator, self.caster, dino, enemies)

## The layers upon layers of Reactions, of which can contain several parallel Reaction Windows.
class reactStack():
    def __init__(self, arrayReactionWindows):
        self.arrayReactionWindows = arrayReactionWindows

    def react(self, dino, enemies, prefabVisualFunction, environments = []):
        pool = []

        for rw in self.arrayReactionWindows:
            for entity in [dino] + enemies:
                pool += rw.cullAviators(entity, dino, enemies)

        if len(pool) > 0:
            prefabVisualFunction.display()
            preamble = []

            currentMomentText = "Resolve Triggers ("
            for rw in self.arrayReactionWindows:
                for index, moment in enumerate(rw.moments):
                    currentMomentText += moment.name
                    if index != len(rw.moments) - 1:
                        currentMomentText += ", "
            preamble.append(currentMomentText + "):")

            allOptional = True
            index = 1
            for reactor in pool:
                preamble.append(reactor.rt.getText(prefixText = str(index) + ". "))
                if reactor.optional == False:
                    allOptional = False
                index += 1

            if allOptional:
                pick = h.pickValue("Pick a Trigger to Resolve", range(1, len(pool) + 1), preamble = preamble, canPass = True, passedInVisuals = prefabVisualFunction)
            else:
                pick = h.pickValue("Pick a Trigger to Resolve", range(1, len(pool) + 1), preamble = preamble, passedInVisuals = prefabVisualFunction)
            ## print("")

            if pick < 0:
                pool = []
            else:
                pool[pick - 1].resolveTrigger(dino, enemies)

                ## You can layer on some reactions here
                self.react(dino, enemies, prefabVisualFunction, environments)
        else:
            return

## The Reaction Window, consisting of reactions of its type!
class reactionWindow():
    def __init__(self, moments):
        self.moments = moments

    def cullAviators(self, caster, dino, enemies):
        pool = []

        ## Iterates across all Cards
        for cardAviator in caster.getLocations():
            ## Checks triggers on Cards
            for trigger in cardAviator.triggers:
                reactor = trigger.reactionCheck(caster, dino, enemies, self.moments)
                if reactor.canReact:
                    pool.append(reactor)

            ## Checks triggers Cards on Tokens
            for token in cardAviator.tokens:
                for trigger in token.triggers:
                    reactor = trigger.reactionCheck(caster, dino, enemies, self.moments)
                    if reactor.canReact:
                        pool.append(reactor)

        return pool

## The check with whatever would be triggered
class responseAndTrigger():
    def __init__(self):
        ## Slew of default variables
        self.reacted_1 = False

    def response(self, card, caster, dino, enemies, moments):
        pass

    def trigger(self, card, caster, dino, enemies):
        pass

    ## We need a list of reset moments that we can override
    def resetState_TurnEnd(self):
        pass

    def resetState_AfterAnyCardResolves(self):
        pass

    def resetState_AfterAfterEntityAttacked(self):
        pass

## For Cards
class card_responseAndTrigger(responseAndTrigger):
    pass

## For Tokens
class token_responseAndTrigger(responseAndTrigger):
    pass

## The cool Reaction Text.
class rt():
    def __init__(self, optional, aviatorName, trigger, event):
        self.optional = optional
        self.aviatorName = aviatorName
        self.trigger = trigger
        self.event = event
    
    def getText(self, prefixText = ""):
        prefixText += self.aviatorName + ": "
        ## if len(prefixText) % 2 == 1:
        ##     prefixText += " "
        pad = 42 - 5

        if self.optional:
            lb = "[ "
            rb = " ]"
        else:
            lb = "{ "
            rb = " }"

        text = []

        ## Gets every line of the trigger effect name
        lefthandLines = [" "]
        nextBloc = ""
        carrotWord = False

        for index, word in enumerate(h.splinterize(prefixText)):
            nextBloc += word
            ## If we only have spaces or nothing in this nextBloc, we do not care about it yet
            if nextBloc.isspace() or nextBloc == "":
                continue

            ## If we currently have a '^' symbol, we need to add a trailing '^'
            if len(word) > 0 and word[0] == '^':
                carrotWord = True

            if len(lefthandLines[-1]) + len(nextBloc) + len("  ") > pad:
                ## Depending on the number of preceeding spaces, we must append a padded number of spaces
                nextBloc = nextBloc.lstrip()
                lefthandLines.append("  ")

                ## We need to add and remove a '^' if we have a carrot word
                if carrotWord:
                    ## We must remove trailing spaces
                    lefthandLines[-2].rstrip()
                    lefthandLines[-2] += '^'
                    lefthandLines[-1] += '^'

            lefthandLines[-1] += nextBloc
            nextBloc = ""

            ## If we no longer have a '^', removes such a symbol
            if len(word) > 0 and word[-1] == '^':
                carrotWord = False

        ## Gets each line of each trigger trigger text and event text
        righthandLines = [""]
        for word in h.splinterize(lb + self.trigger + rb) + ["  ARR  "] + h.splinterize(lb + self.event + rb):
            ## Are we at max capacity?
            if len(righthandLines[-1]) + len(word) > h.WIDTH - pad - 12:
                word = word.lstrip()
                righthandLines.append("  ")

            ## Do we have a new line symbol we must accomodate?
            if word == "//":
                if righthandLines[-1].isspace():
                    righthandLines.pop()
                righthandLines.append("  ")
            else:
                righthandLines[-1] += word

        ## Concatenates the both of them
        arrayIndex = 0
        text = []
        padding = ". "
        while arrayIndex < len(lefthandLines) or arrayIndex < len(righthandLines):
            text.append("")

            if len(lefthandLines) == arrayIndex:         ## Not enough lefthandLines length
                lefthandLines.append("")
                padding = "  "
            if len(righthandLines) == arrayIndex:        ## Not enough righthandLines length
                righthandLines.append("")
                padding = "  "

            ## Makes padding spacing evenly aligned
            if len(lefthandLines[arrayIndex]) % 2 == 1:
                lefthandLines[arrayIndex] += " "

            text[-1] += h.normalize(lefthandLines[arrayIndex], pad + 5, separator = padding)
            text[-1] += righthandLines[arrayIndex]

            arrayIndex += 1

        returnString = ""
        for index, line in enumerate(text):
            returnString += line
            if index != len(text) - 1:
                returnString += " // "

        return returnString

## Empty rt
EMPTY_RT = rt(True, "No Name", "No Trigger", "No Event")

## A Reaction!
class reaction():
    ## Creates the reaction w/reactor. 
    def __init__(self, aviator, optional, responseAndTrigger, endOfDinoTurn = False):
        self.aviator = aviator
        self.optional = optional
        self.responseAndTrigger = responseAndTrigger

        ## Types of reactions
        self.endOfDinoTurn = endOfDinoTurn

    def reactionCheck(self, caster, dino, enemies, moments):
        response = [False, EMPTY_RT]

        ## Checks Card Aviators
        if isinstance(self.aviator, c.Card):
            response = self.responseAndTrigger.response(self.aviator, caster, dino, enemies, moments)
            return reactor(caster,
                           self.aviator,
                           response[0],
                           response[1],
                           self.optional,
                           self.responseAndTrigger)

        if isinstance(self.aviator, tk.token):
            response = self.responseAndTrigger.response(self.aviator, caster, dino, enemies, moments)
            return reactor(caster,
                           self.aviator,
                           response[0],
                           response[1],
                           self.optional,
                           self.responseAndTrigger)

            ## Check the Caster
            # tbd 2 / 12 / 2024

## Times where triggers can happen.
##  These should be times that have no checks, and basically just parts of turn order sequencing.
class reactMoments():
    def __init__(self, name):
        self.name = name

class AtTurnEnd(reactMoments):
    def __init__(self):
        super().__init__("Turn End")

class DinoTurn(reactMoments):
    def __init__(self):
        super().__init__("Your Turn")

class AtTurnEndTidying(reactMoments):
    def __init__(self):
        super().__init__("Turn End Tidying")

class BeforeCardPlayResolution(reactMoments):
    def __init__(self, cardToResolve):
        super().__init__("Before Card Play Resolution")
        self.cardToResolve = cardToResolve

class AfterCardPlayResolution(reactMoments):
    def __init__(self, cardThatWasResolved):
        super().__init__("After Card Play Resolution")
        self.cardThatWasResolved = cardThatWasResolved

class DiscardedCard(reactMoments):
    def __init__(self, fromLocation, cardThatWasDiscarded):
        super().__init__("Discarded Card")
        self.fromLocation = fromLocation
        self.cardThatWasDiscarded = cardThatWasDiscarded

class AfterEntityAttacked(reactMoments):
    def __init__(self, attackedEnemy, damageCaster, AttackData, DamageData):
        super().__init__("After Entity Attacked")
        self.attackedEnemy = attackedEnemy
        self.damageCaster = damageCaster
        self.AttackData = AttackData
        self.DamageData = DamageData

## Checks to see if we are at the right moment
def moments_isLeftInRight(leftMoments, rightMoments):
    typedRightMoments = []
    for rightMoment in rightMoments:
        typedRightMoments.append(type(rightMoment))

    for leftMoment in leftMoments:
        if leftMoment not in typedRightMoments:
            return False

    return True

## Gets the moment; returns None if does not exist
def moments_fetchInRight(leftMoments, rightMoments):
    typedRightMoments = []
    for rightMoment in rightMoments:
        typedRightMoments.append(type(rightMoment))

    for leftMoment in leftMoments:
        if leftMoment in typedRightMoments:
            for i, typedRightMoment in enumerate(typedRightMoments):
                if leftMoment == typedRightMoment:
                    return rightMoments[i]

    return None







