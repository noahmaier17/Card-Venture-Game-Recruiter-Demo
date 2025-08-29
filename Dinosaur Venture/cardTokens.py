import random
import react as r

## Checks for tokens. If the token parameter equals True, it will check if that token exists.
##  Of all checked-for Tokens, if one is not part of this Card, return False.
##  Otherwise (meaning, all checks were passed), returns True.
## Tokens is a List of Tokens
def checkTokensOnThis(card, tokens):
    allTokensExist = True
    tokensToCheck = []
    for token in tokens:
        tokensToCheck.append(token.name)
    tokensOnCard = []
    for token in card.tokens:
        tokensOnCard.append(token.name)

    for toCheck in tokensToCheck:
        if toCheck not in tokensOnCard:
            allTokensExist = False

    return allTokensExist

## Connected directly by the "publishToken" function in Card.py
## Token in a singular token
##  --> NEVER CALL THIS
def publishTokenOnThis(card, token):
    if not checkTokensOnThis(card, [token]):
        card.tokens.append(token)

## Removes a token from a location. Returns TRUE if that token was removed, FALSE otherwise.
##  --> NEVER CALL THIS
def removeToken(card, tokenToRemove):
    if not checkTokensOnThis(card, [tokenToRemove]):
        return False

    tokensToKeep = []
    for token in card.tokens:
        if token.name != tokenToRemove.name:
            tokensToKeep.append(token)

    card.tokens = tokensToKeep
    return True

'''
    Things ABOVE here are functions used to check/publish tokens on Cards.
'''

class token():
    ## Creates a token.
    def __init__(self, name):
        self.name = name
        self.displayByName = True

        self.displayWithThrowText = False
        self.throwText = ""

        self.triggers = []

    def getThrowText(self):
        return self.throwText

## <<feathery>>
##  When having an effect that says "Draw to [ # ] Cards in [ Location ]",
##  these Cards do not count in the total card count of that Location.
class feathery(token):
    def __init__(self):
        super().__init__("feathery")

## <<alliance>>
##  At Turn Start, with this in Hand or Pocket, +1 Action.
class alliance(token):
    def __init__(self):
        super().__init__("alliance")

## <<mutated>>
##  Means the Card was mutated; does not have any inherent special mechanic.
class mutated(token):
    def __init__(self):
        super().__init__("new")

## <<inoperable>>
##  You cannot Play <<inoperable>> Cards from Hand nor Pocket. 
class inoperable(token):
    def __init__(self):
        super().__init__("inoperable")

        # self.displayWithThrowText = True
        # self.throwText = "! <<inoperable>> ARR Cannot Play this from Hand nor Pocket."

## <<prepared>>
## When Played, Before Resolution: +1 Action, and Remove this Token.
class prepare(token):
    def __init__(self):
        super().__init__("prepared")

        # self.displayWithThrowText = True
        # self.throwText = "! <<prepared>> ARR When Played, Before Resolution: +1 Action."

## <<confidant>>
## When looting a //confidant//, only cards without the <<confidant>> token can be modified by this //confidant//.
class confidant(token):
    def __init__(self):
        super().__init__("confidant")

'''
        self.triggers.append(r.reaction(self, True, self.trigger_1(self)))

    class trigger_1(r.token_responseAndTrigger):
        def __init__(self, card):
            self.END_OF_DINO_TURN_RT = r.rt(False,
                                            "^" + card.name + "^",
                                            "Before Resolution",
                                            "+1 Action; Remove <<prepared>>")

        def response(self, card, caster, dino, enemies, moments):
            ## Checks for correct trigger time
            if not r.moments_isLeftInRight([r.BeforeCardPlayResolution], moments):
                return (False, r.EMPTY_RT)

            

            return (h.locateCardIndex(caster.play, card) >= 0
                and card.reacted_1 == False
                and caster.actions >= 1, self.END_OF_DINO_TURN_RT)

        def trigger(self, card, caster, dino, enemies):
            card.reacted_1 = True
            cf.dealDamage().func(card, caster, dino, enemies, "null", h.acons([1, 'M'], 'nil'))
'''




