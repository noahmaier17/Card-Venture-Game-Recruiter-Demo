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
class script_DinoPlayCard(gameplayScriptInput):
    pass