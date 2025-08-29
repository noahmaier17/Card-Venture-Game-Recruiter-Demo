## For functions that need to use dc and ec

## Gathers into a list all cards that contain at least 1 matching location
def getCardsByTable(crosscompareTable):
    tabulizedCards = []
    for Card in dc.DinoCard.__subclasses__() + ec.EnemyCard.__subclasses__():
        if any(i in Card().table for i in crosscompareTable):
            tabulizedCards.append(Card())
    return tabulizedCards
    