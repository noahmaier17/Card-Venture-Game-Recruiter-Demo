from Dinosaur_Venture import gameplayLoopEvents as gameEvents

## Sets up the entityNames and cardNames
entityNames, cardNames = gameEvents.setupEntityAndCardNames()

## Simulator class.
## Every simulator class has a corresponding gameplayLoopEvents.py class. This is for simulating those
##  gameplay loop events, handing special cases which may arise from the simulated nature of the code.
class simulateGameEvent():
    def __init__(self, scriptedInput=None):
        self.scriptedInput = scriptedInput

    def sim():
        pass

## Start round
class startRound(simulateGameEvent):
    def sim(self, dino, enemies):
        gameEvents.startRound(dino, enemies)

## Dino turn start
class dinoTurnStart(simulateGameEvent):
    def sim(self, dino, enemies):
        gameEvents.dinoTurnStart(dino, enemies)

## Dino play Card
class dinoPlayCard(simulateGameEvent):
    def sim(self, dino, enemies, roundCount, clearing, event):
        gameEvents.dinoPlayCard(dino, enemies, roundCount, clearing, event, entityNames, cardNames,
                                scriptedInput_dinoPlayCard=self.scriptedInput)

## Simulates gameplay.
##  simualteGameEventsArray: an array of simulateGameEvent methods, which corresponds to the order
##  of what is simulated.
def simulate(dino, enemies, clearing, simulateGameEventsArray):
    for simulateGameEvent in simulateGameEventsArray:
        if isinstance(simulateGameEvent, startRound):
            simulateGameEvent.sim(dino, enemies)
        elif isinstance(simulateGameEvent, dinoTurnStart):
            simulateGameEvent.sim(dino, enemies)
        elif isinstance(simulateGameEvent, dinoPlayCard):
            simulateGameEvent.sim(dino, enemies, 0, clearing, "Dino Play Card")
        else:
            print(0/0) ## Very lazy error thrower
    # return (dino, enemies, clearing)