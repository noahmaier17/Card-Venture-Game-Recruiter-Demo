'''
    Enables scripted input, used for automated test cases. 
    Most gameplayLoopEvents.py functions have a corresponding gameplayScriptInput.py function. 
'''

## Parent class. 
## The expected input is an array.
class gameplayScriptInput():
    def __init__(self, input):
        self.input = input
    
    def getNextValue(self):
        if len(self.input) > 0:
            return self.input.pop(0)
        else:
            raise Exception("gameplayScriptInput does not have enough values")


## Script for gameplayLoopEvents.dinoPlayCard
## The getNextValue call asks for all the input values of gameplayLoopEvents.dinoPlayCard to enable other functionality
class script_DinoPlayCard(gameplayScriptInput):
    def getNextValue(self, dino, enemies, roundCount, clearing, event, entityNames, cardNames):
        return super().getNextValue()

## Script for gameplayLoopEvents.dinoPlayCard
## Special functionality: based on the input value, looks for a card in hand/pocket with that name.
##  If such a card exists, plays the index of its location (as if a human looked for the card name). 
##  If no such card exists, types into the console whatever that input value happened to be.
class script_DinoPlayCard_attemptPlayCardByName(script_DinoPlayCard):
    def getNextValue(self, dino, enemies, roundCount, clearing, event, entityNames, cardNames):
        if len(self.input) > 0:
            nextValue = self.input.pop(0)

            ## Is this next value the name of a card in play?
            for index, card in enumerate(dino.pocket.getArray() + dino.hand.getArray()):
                index += 1 ## Hand and pocket are 1-indexed

                if nextValue.lower() == card.name.lower():
                    return index
        
            ## We did not find such a match
            self.input.insert(0, nextValue)
        
        return super.getNextValue()
