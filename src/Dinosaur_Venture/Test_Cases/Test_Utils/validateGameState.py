## Checks if a card is at a specific index in a specific location.
## To be robust against deep copies (and the like), checks against the card's uniqueID.
def isCardAtIndexInLocation(card, index, location):
    if location.length() <= index:
        return False

    crosscompareCard = location.at(index)
    return (card.uniqueID == crosscompareCard.uniqueID)