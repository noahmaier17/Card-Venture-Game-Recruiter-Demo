from Dinosaur_Venture import card as c


## Dino Cards
class DinoCard(c.Card):
    def __init__(self):
        super().__init__()

## A special Dino Card type called \\Shell\\ Cards.
##  These are not gained to Dino's Deck, but instead modify one of Dino's already-existing Cards.
class DinoShellCard(c.Card):
    def __init__(self):
        super().__init__()
        self.isShellCard = True
        self.isGainedCard = False

        self.isConfidant = False

        self.mustDestroyCardWhenLooted = False
        self.mustEnshellCardWhenLooted = True

    def onLootedEnshelling(self, dino, cardToEnshell):
        # this just exists to make adding something easy (since it is already prepped)
        pass
