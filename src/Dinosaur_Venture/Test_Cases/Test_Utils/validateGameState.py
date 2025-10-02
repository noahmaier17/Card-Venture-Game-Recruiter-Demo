## Checks if two cards are equivalent
def isCardEquivalent(card, otherCard):
    return (card.uniqueID == otherCard.uniqueID)

## Checks if a card is at a specific index in a specific location.
## To be robust against deep copies (and the like), checks against the card's uniqueID.
def isCardAtIndexInLocation(card, index, location):
    if location.length() <= index:
        return False

    crosscompareCard = location.at(index)
    return isCardEquivalent(card, crosscompareCard)

## Checks if a card is in a location (at any index).
def isCardInLocation(card, location):
    for crosscompareCard in location.getArray():
        if isCardEquivalent(card, crosscompareCard):
            return True
    return False

## Checks if a card is exclusively in a location.
## As in:
## (1) Is it in the expected location?
## (2) Is it no where else to be found?
def isCardExclusivelyInLocation(card, location, dino, enemies):
    if not isCardInLocation(card, location):
        return False

    allLocations = dino.getIterableOfLocations()
    for enemy in enemies:
        allLocations += enemy.getIterableOfLocations()

    for otherLocation in allLocations:
        if otherLocation != location and isCardInLocation(card, otherLocation):
            return False
         
    return True

## Checks if a card is exclusively in a location at a certain index. 
## As in:
## (1) Is it in the expected location at the expected index?
## (2) Is it no where else to be found?
def isCardExclusivelyAtIndexInLocation(card, index, location, dino, enemies):
    ## Is this card at index in location?
    if not isCardAtIndexInLocation(card, index, location):
        return False
    
    ## Is this card in this location more than once?
    for crosscompareIndex, crosscompareCard in enumerate(location.getArray()):
        if index != crosscompareIndex and isCardEquivalent(card, crosscompareCard):
            return False
        
    ## Is this card exclusively at this single index in this single location?
    if not isCardExclusivelyInLocation(card, location, dino, enemies):
        return False
    
    return True