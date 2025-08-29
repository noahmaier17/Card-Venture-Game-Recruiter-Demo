"""
class corrodedWoodChipper(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Corroded Wood Chipper"
        self.bodyText = c.bb("Draw 1 more Card for your Next Hand. Move this onto Deck.")
        self.publishPacking("Draw 1 more Card for your Next Hand.")
        self.table = ["Fallow Farmland"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusUpcomingPlusCard(0, 1)
        index = h.locateCardIndex(caster.play, self)
        if index >= 0:
            caster.moveCard(caster.play, index, caster.draw, position = 0)
        else:
            h.splash('FAIL_MOVE')
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        caster.plusUpcomingPlusCard(0, 1)
"""   
   
'''
    Card Depot
'''
'''
class trampledRedent(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trampled Redent"
        self.bodyText = c.bb("1R.")
        self.publishUnpacking("1R.")
        self.table = ["Husk of an Agricultural Mech"]

    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'R'], 'nil'))

    def onUnpacking(self, caster, dino, enemies):
        super().onUnpacking(caster, dino, enemies)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'R'], 'nil'))
'''

"""
'''
    Packing Bot Cards 
'''
## +1 Action. 1G-notick / 1B-notick. 
class recycledShirt(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Recycled Shirt"
        self.bodyText = c.bb("+1 Action. 1G-notick / 1B-notick.")
        self.table = ["Packing Bot"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], h.acons([1, 'B-notick'], 'nil')))

## 2R. WTID, at the end of a Rest Stop, pick a Card that is initialized to a location other than "Draw" (the default). Change its initialization location to "Top of Draw", "Bottom of Draw", or "Discard."
class redCardboardBox(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Red Cardboard Box"
        self.bodyText = c.bb("2R.")
        self.bodyText.push("looting", "WTID, at the end of a Rest Stop: pick a Card in Deck that is initialized to a location other than 'Draw' (the default). //To it: change its initialization location to 'Top of Draw', 'Bottom of Draw', or 'Discard'.")
        self.table = ["Packing Bot"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))
    
    def atTriggerEndOfRestStop(self, caster):
        ## Checks if there is a Card that has a non-'Draw' initialization location
        containsDrawInitialization = False
        upgradeCandidates = []
        otherCards = []
        for card in caster.deck:
            if card.initialized == "Draw":
                upgradeCandidates.append(card)
                containsDrawInitialization = True
            else:
                otherCards.append(card)
        if containsDrawInitialization:
            locations = ["Top of Draw", "Bottom of Draw", "Discard"]
        
            ## Display Text
            os.system('cls')
            print("Resolving: " + Back.CYAN + Style.BRIGHT + " " + self.name + " ")
            h.splash("Change an Initialized Location from 'Draw' to: 'Top of Draw', 'Bottom of Draw', or 'Discard'.", printInsteadOfInput = True)
            
            if len(otherCards) != 0:
                index = 0
                print(" | Already have a non-'Draw' initialization Location:")
                for card  in otherCards:
                    print(" |  " + ALPHABET[index] + ". " + Back.CYAN + Style.BRIGHT 
                    + " " + card.name + " " + Back.RESET + Style.NORMAL 
                    + h.normalize("", 30 - len(card.name)) + "> " 
                    + card.niceBodyText(41, 100, supressedTypes = []))
                    index += 1
            
            print(" | Selectable:")
            index = 0
            for card in upgradeCandidates:
                print(" |  " + str(index + 1) + ". " + Back.CYAN + Style.BRIGHT 
                + " " + card.name + " " + Back.RESET + Style.NORMAL 
                + h.normalize("", 30 - len(card.name)) + "> " 
                + card.niceBodyText(41, 100, supressedTypes = []))
                index += 1
            ## Picks the Card to Change
            pickedCardIndex = h.pickValue("Pick a Card to Change", range(1, len(upgradeCandidates) + 1)) - 1
            pickedCard = upgradeCandidates[pickedCardIndex]
            ## Display Text
            os.system('cls')
            print(" | Picked: " + Back.CYAN + Style.BRIGHT + " " + pickedCard.name + " ")
            print("   " + pickedCard.niceBodyText(3, 100))
            print("")
            h.splash("Pick its new Initialized location: ", printInsteadOfInput = True)
            for i in range(len(locations)):
                h.splash(" " + str(i + 1) + ". '" + locations[i] + "'.", printInsteadOfInput = True)
            
            pickedLocationIndex = h.pickValue("Pick a Location", range(1, len(locations) + 1)) - 1
            
            pickedCard.changeInitialization(locations[pickedLocationIndex])
            ## Resets the deck with this change
            caster.deck = []
            for card in upgradeCandidates:
                caster.deck.append(card)
            for card in otherCards:
                caster.deck.append(card)
            random.shuffle(caster.deck)
        else:
            h.splash("All Cards in Deck have Initialization locations that are not 'Draw'!")

## +1 Action. +2 Cards. 
##  At the end of your Turn, if you dealt no damage, Move this onto Draw. 
##  { HH }
class forkliftCertificate(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Forklift Certificate"
        self.bodyText = c.bb("+1 Action. +2 Cards. //At the end of your Turns, if you dealt no damage during that Turn: Move this onto Draw.")
        self.bodyText.push("{}", "{ HH }")
        self.bodyText.push("[]", "[ iBottom_of_Draw ]")
        self.table = ["Packing Bot"]
        self.initialized = "Bottom of Draw"
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        for i in range(2):
            caster.drawCard()
        self.foreverLinger = True
    
    def atTriggerTurnEnd(self, caster, dino, enemies):
        if caster.dealtDamageThisTurn == False:
            h.splash("Triggered ^Forklift Certificate^ Condition: You dealt no damage this turn, so Moving this onto Draw.")
            index = h.locateCardIndex(caster.play, self)
            if index >= 0:
                caster.moveCard(caster.play, index, caster.draw, position = len(caster.draw))
            else:
                h.splash('FAIL_MOVE')

## 1B. 
class bluePipe(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Blue Pipe"
        self.bodyText = c.bb("1B.")
        self.table = ["Packing Bot"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'B'], 'nil'))

## 1G. 
class smellOfTheWild(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Smell of the Wild"
        self.bodyText = c.bb("1G.")
        self.table = ["Packing Bot"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], 'nil'))

## +1 Action. You may: +1 Action. Otherwise: Next Turn, +1 Action. 
##  { 1H }
class miscellaneousFasteners(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Miscellaneous Fasteners"
        self.bodyText = c.bb("+1 Action. //You may: +1 Action. Otherwise: Next turn, +1 Action.")
        self.bodyText.push("{}", "{ 1H }")
        self.customQueryAnswerYes = False
        self.table = ["Packing Bot"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        query = h.yesOrNo("+1 Action this Turn?")
        if query:
            self.customQueryAnswerYes = True
            caster.plusActions(1)
        else:
            self.customQueryAnswerYes = False
        self.lingering = 1
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.customQueryAnswerYes == False:
            caster.plusActions(1)

## Choose a living Enemy. To it: it discards a Card from Hand per Pair of Cards you have in Play.
##  { HH }
class zipTies(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Zip Ties"
        self.bodyText = c.bb("Choose a living Enemy. To it: it discards a Card from Hand per Pair of Cards you have in Play.")
        self.bodyText.push("{}", "{ HH }")
        self.table = ["Packing Bot"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        if len(dino.play) <= 1:
            h.splash("You have too few Cards in Play, so this does nothing.")
        else:
            index = h.pickLivingEnemy("Pick Enemy", enemies)
            if index != -1:
                enemy = enemies[index]
                numberToDiscard = math.floor(len(dino.play) / 2)
                for i in range(numberToDiscard):
                    if len(enemy.hand) > 0:
                        enemy.discardCard(enemy.hand, random.randint(0, len(enemy.hand) - 1))
        self.foreverLinger = True
        
## 3R. { 1H }.
class redBrush(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Red Brush"
        self.bodyText = c.bb("3R.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Home"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'R'], 'nil'))
        self.lingering = 1



'''
## 1M. 
class whiteVase(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "White Vase"
        self.bodyText = "1M."
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], 'nil'))
'''

## 3G. { 1H }.
class greenBrush(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Green Brush"
        self.bodyText = c.bb("3G.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], 'nil'))
        self.lingering = 1

## 3B. { 1H }.
class blueBrush(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Blue Brush"
        self.bodyText = c.bb("3B.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'B'], 'nil'))
        self.lingering = 1

## 1R / 1G. 
class redAndGreenPen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Red and Green Pen"
        self.bodyText = c.bb("1R / 1G.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'R'], h.acons([1, 'G'], 'nil')))

## 1G / 1B. 
class greenAndBluePen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Green and Blue Pen"
        self.bodyText = c.bb("1G / 1B.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], h.acons([1, 'B'], 'nil')))

## 1B / 1R. 
class blueAndRedPen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Blue and Red Pen"
        self.bodyText = c.bb("1B / 1R.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'B'], h.acons([1, 'R'], 'nil')))

## +1 Action, +2 Cards. { HH }
class familyBroom(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Family Broom"
        self.bodyText = c.bb("+1 Action, +2 Cards.")
        self.bodyText.push("{}", "{ HH }")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        for i in range(2):
            caster.drawCard()
        self.foreverLinger = True

## +1 Action. 1R-notick. 
class chewedRedPen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Chewed Red Pen"
        self.bodyText = c.bb("+1 Action. 1R-notick.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'], 'nil'))

## +1 Action. 1G-notick. 
class chewedGreenPen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Chewed Green Pen"
        self.bodyText = c.bb("+1 Action. 1G-notick.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

## +1 Action. 1B-notick. 
class chewedBluePen(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Chewed Blue Pen"
        self.bodyText = c.bb("+1 Action. 1B-notick.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'B-notick'], 'nil'))

## 1Random / 1Random. 
class reallyChewedGraphium(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Really Chewed Graphium"
        self.bodyText = c.bb("1Random / 1Random.")
        self.table = ["Home"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'Random'], 
                h.acons([1, 'Random'], 'nil')))

## +1 Action. Discard your hand, then +2 Cards.
class hopeForBetterDays(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hope For Better Days"
        self.bodyText = c.bb("+1 Action. Discard your hand, then +2 Cards.")
        self.table = ["Home"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        size = len(caster.hand)
        for i in range(size):
            caster.moveCard(caster.hand, 0, caster.discard)
        for i in range(2):
            caster.drawCard()

## +1 Action. 1Random-notick / 1Random-notick. 
class aridBrush(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Arid Brush"
        self.bodyText = c.bb("+1 Action. 1Random-notick / 1Random-notick.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'Random-notick'], 
                                        h.acons([1, 'Random-notick'], 'nil')))

## 4L. 
class yellowBoot(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Yellow Boot"
        self.bodyText = c.bb("4L.")
        self.table = ["Home"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([4, 'L'], 'nil'))

## ----- Cards from Enemies -----
## 2Random / 2Random.
##  Next turn, +1 Card. 
## { 1H }
'''
class tarnishedScythe(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tarnished Scythe"
        self.bodyText = c.bb("2Random / 2Random. //Next turn, +1 Card.") 
        self.bodyText.push("{}", "{ 1H }")
        self.table = []
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'Random'], 
                h.acons([2, 'Random'], 'nil')))
        self.lingering = 1
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        caster.drawCard()
''' 
    
## 1R. Then: 1G. Then: 1B.
class trampledRodent(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trampled Rodent"
        self.bodyText = c.bb("1R. Then: 1G. Then: 1B.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'R'], 'nil'))
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], 'nil'))
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'B'], 'nil'))

## +1 Action. 1Random / 1Random. 
##  You may move this from Play and onto Deck.  
class peelingRodent(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Peeling Rodent"
        self.bodyText = c.bb("+1 Action. 1Random / 1Random. //You may move this from Play and onto Deck.")
        self.table = ["Humming Mech Field"]

    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'Random'], h.acons([1, 'Random'], 'nil')))
        query = h.yesOrNo("Move 'Peeling Rodent' from Play and onto Deck?")
        if query:
            index = h.locateCardIndex(caster.play, self)
            if index >= 0:
                caster.moveCard(caster.play, index, caster.draw, position = len(caster.draw))
            else:
                h.splash('FAIL_MOVE')

## +1 Action. +1 Card. Next Turn: +1 Action. 
class twigRockScarecrow(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Twig Rock Scarecrow"
        self.bodyText = c.bb("+1 Action. +1 Card. //Next Turn: +1 Action.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Humming Mech Field"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()
        self.lingering = 1
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        caster.plusActions(1)

'''
## 1B / 1M. Discard front living enemy's Hand. 
##  Draw 1 less Card for your next Hand. 
class brassMuzzle(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rusted Muzzle"
        self.bodyText = c.bb("1B / 1M. Discard front living Enemy's Hand. //Draw 1 less Card for your next Hand.")
        self.table = ["Humming Mech Field"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        # caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'B'], h.acons([1, 'M'], 'nil')))
        caster.plusUpcomingPlusCard(0, -1)
        
        index = h.getFrontLivingEnemyIndex(enemies)
        if index != -1:
            enemy = enemies[index]
            size = len(enemy.hand)
            for i in range(size):
                enemy.discardCard(enemy.hand, 0)
'''

## 1G. Then: 3G.  
class harvestedGrass(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Harvested Grass"
        self.bodyText = c.bb("1G. Then: 3G.")
        self.table = ["Humming Mech Field"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], 'nil'))
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], 'nil'))

## +1 Action. 2B. 
##  Move this from Play and onto Deck. 
class blueCableCord(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Blue Cable Cord"
        self.bodyText = c.bb("+1 Action. 2B. //Move this from Play and onto Deck.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'B'], 'nil'))
        
        index = h.locateCardIndex(caster.play, self)
        if index >= 0:
            caster.moveCard(caster.play, index, caster.draw, position = len(caster.draw))
        else:
            h.splash('FAIL_MOVE')

## +1 Action. 1M / 1M. 
##  { HH }
class heavyScrapMetal(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Heavy Scrap Metal"
        self.bodyText = c.bb("+1 Action. 1M / 1M.") 
        self.bodyText.push("{}", "{ HH }")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], h.acons([1, 'M'], 'nil')))
        
        self.foreverLinger = True

## 2R / 1Random / 1Random / 1Random.
class bloodyRodentHead(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bloody Rodent Head"
        self.bodyText = c.bb("2R / 1Random / 1Random / 1Random.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 
            h.acons([1, 'Random'], 
                h.acons([1, 'Random'], 
                    h.acons([1, 'Random'], 'nil')))))

'''
## 2R / 3Random. 
class bloodyRodentLegs(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bloody Rodent Legs"
        self.bodyText = c.bb("2R / 3Random.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], h.acons([3, 'Random'], 'nil')))
'''
    
## +1 Action. +2 Cards.
##  Draw 1 less Card for your next Hand. 
class tantalizingFieldgrass(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tantalizing Fieldgrass"
        self.bodyText = c.bb("+1 Action. +2 Cards. //Draw 1 less Card for your next Hand.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        for i in range(2):
            caster.drawCard()
        caster.plusUpcomingPlusCard(0, -1)

## +1 Action. +1 Card. 
##  [ Into Hand ]
##  When replaced with new Loot: +1 Looting. 
class frolicMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Frolic Mantra"
        self.bodyText = c.bb("+1 Action. +1 Card.") 
        self.bodyText.push("[]", "[ iInto_Hand ]")
        self.bodyText.push("looting", "When replaced with new Loot: +1 Looting.")
        self.table = ["Humming Mech Field"]
        self.initialized = "Into Hand"
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()
        
    # def onLooted(self, dino):
    #     h.splash("Triggered On Looting: +1 Looting.")
    #     dino.looting += 1
    
    def onReplacedWithLoot(self, dino):
        h.splash("Triggered On Replaced with Loot: +1 Looting.")
        dino.looting += 1

## 1M. While resolving this Card, if a Band was destroyed: +1 Action.
class hiddenMineralDeposit(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hidden Mineral Deposit"
        self.bodyText = c.bb("1M. While resolving this Card, if a Band was destroyed: //+1 Action.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        totalBands = 0
        for enemy in enemies:
            totalBands += enemy.getBands()
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], 'nil'))
        crosscompareTotalBands = 0
        for enemy in enemies:
            crosscompareTotalBands += enemy.getBands()
        if crosscompareTotalBands != totalBands:
            h.splash("A Band was destroyed, so: +1 Action.")
            caster.plusActions(1)

'''
## +1 Action. Pick a living Enemy. To it: 1R; discard its hand. 
##  Draw 1 less Card for your next Hand. 
class deepClayReservoir(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Deep Clay Reservoir"
        self.bodyText = c.bb("+1 Action. Pick a living Enemy. To it: discard its hand; 1R. //Draw 1 less Card for your next Hand.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        index = h.pickLivingEnemy("Pick Enemy", enemies)
        if index != -1:
            size = len(enemies[index].hand)
            for i in range(size):
                enemies[index].discardCard(enemies[index].hand, 0)
            enemies[index].damage(caster, dino, enemies, h.acons([1, 'R'], 'nil'))
        caster.plusUpcomingPlusCard(0, -1)
'''

## +1 Action. To every Enemy: 1R-notick. 
class deepClayReservoir(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Deep Clay Reservoir"
        self.bodyText = c.bb("+1 Action. To every Enemy: 1R-notick.")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        size = len(enemies[index].hand)
        for i in range(size):
            enemies[index].dealDamage(caster, dino, enemies, h.acons([1, 'R-notick'], 'nil'))
        
## +1 Action. Draw until you have 3 Cards in Hand. 
##  { HH }
class oxidizedShovel(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Oxidized Shovel"
        self.bodyText = c.bb("+1 Action. Draw until you have 3 Cards in Hand.")
        self.bodyText.push("{}", "{ HH }")
        self.table = ["Humming Mech Field"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        drewEmpty = False
        while not(drewEmpty) and len(caster.hand) < 3:
            drawnCard = caster.drawCard()
            if drawnCard == 'empty':
                drewEmpty = True
        self.foreverLinger = True
        
'''
    The Bear Clearing
'''
## 2R. Then: 2B. 
class bearClaws(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Claws"
        self.bodyText = c.bb("2R. Then: 2B.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'B'], 'nil'))

## 3L. Then: 3L. 
##  Next turn, +2 Actions. 
class scaryBeesNest(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Scary Bees Nest"
        self.bodyText = c.bb("3L. Then: 3L. Next turn, +2 Actions.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'L'], 'nil'))
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'L'], 'nil'))
        self.lingering = 1
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        caster.plusActions(2)

## +1 Action. +3 Cards. 
##  Each Enemy heals 1M. 
class stickProddingMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Stick Prodding Mantra"
        self.bodyText = c.bb("+1 Action. +3 Cards. To each Enemy: Heal 1M.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        for i in range(3):
            caster.drawCard()
        for enemy in enemies:
            enemy.heal(caster, dino, enemies, h.acons([1, 'M'], 'nil'))

'''
## +1 Card. 2R / 2G / 2B. 
class crushingBearHug(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Crushing Bear Hug"
        self.bodyText = c.bb("+1 Card. 2R / 2G / 2B.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.drawCard(printCard = True)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 
            h.acons([2, 'G'], 
                h.acons([2, 'B'], 'nil'))))
'''

## 2M. 
##  +1 Card. Move a Card from Hand onto the Into-Hand mat.
class bearPaw(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Paw"
        self.bodyText = c.bb("2M. +1 Card. Move a Card from Hand onto the Into-Hand mat.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'M'], 'nil'))
        caster.drawCard(printCard = True)
        h.splash("Pick a Card to Move from Hand onto the Into-Hand mat.", printInsteadOfInput = True)
        caster.draftCard(dino.hand, len(dino.hand), dino.intoHand)

## Pick a living Enemy. To it: 9G; Heal 1G. 
class barringGapsBetweenTeeth(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Barring Gaps Between Teeth"
        self.bodyText = c.bb("Pick a living Enemy. To it: 9G; Heal 1M.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        index = h.pickLivingEnemy("Pick Enemy", enemies)
        if index != -1:
            enemies[index].damage(caster, dino, enemies, h.acons([9, 'G'], 'nil'))
            enemies[index].heal(caster, dino, enemies, h.acons([1, 'M'], 'nil'))

'''
## 3G / 3R. 
class tiltLeftAndConsume(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tilt Left and Consume"
        self.bodyText = c.bb("3G / 3R.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], h.acons([3, 'R'], 'nil')))
'''


## 3B / 3G. 
class tiltRightAndConsume(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tilt Right and Consume"
        self.bodyText = c.bb("3B / 3G.")
        self.table = ["New Bear Order"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'B'], h.acons([3, 'B'], 'nil')))

## +2 Actions. 
##  Next turn, +2 Actions. 
##  { 1H }
class standYourGround(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Stand Your Ground"
        self.bodyText = c.bb("+2 Actions. Next turn, +2 Actions.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(2)
        self.lingering = 1
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        caster.plusActions(2)

## 3R. Move all of Hand onto the Into-Hand mat. 
##  Next turn, +1 Action. 
##  { 1H }
class oldCampingTent(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Old Camping Tent"
        self.bodyText = c.bb("3R. Move all of Hand onto the Into-Hand mat. //Next turn, +1 Action.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))
        size = len(caster.hand)
        for i in range(size):
            caster.moveCard(caster.hand, 0, caster.intoHand)
        self.lingering = 1
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        caster.plusActions(1)

## +1 Action. 9L. 
class bigBackScratcherTree(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Big Back Scratcher Tree"
        self.bodyText = c.bb("+1 Action. 9L.")
        self.bodyText.push("[]", "[ iDiscard ]")
        self.table = ["New Bear Order"]
        self.initialized = "Discard"
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([9, 'L'], 'nil'))

## Move the top 2 Cards of Draw onto the Into Hand mat.
class rightToBearArms(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Right To Bear Arms"
        self.bodyText = c.bb("2Random. Move the top 2 Cards of Draw onto the Into-Hand mat.")
        self.table = ["New Bear Order"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'Random'], 'nil'))
        for i in range(2):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, printCard = True)
        input(" ... ")

## If it is your Turn number 1, to each Enemy that has taken 0 Turns: they discards their hand. 
class hibernation(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hibernation"
        self.bodyText = c.bb("If it is your Turn number 1, to each Enemy that has taken 0 Turns: they discard their hand.")
        self.bodyText.push("[]", "[ iTop_of_Draw ]")
        self.table = ["New Bear Order"]
        self.initialized = "Top of Draw"
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        if (caster.turn == 1):
            for enemy in enemies:
                if enemy.turn == 0:
                    size = len(enemy.hand)
                    for i in range(size):
                        enemy.discardCard(enemy.hand, 0)
                    h.splash("'" + enemy.name + "' discarded their Hand.", printInsteadOfInput = True)
            input(" ... ")
        else:
            h.splash("It is your Turn number " + str(caster.turn) + ", so ^Hibernation^ fails.")

## +1 Action. +1 Card. //At the End of Turn, per Action you have, plus that many Actions for next Turn. 
class wiseBearSkull(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Wise Bear Skull"
        self.bodyText = c.bb("+1 Action. +1 Card. //At the End of Turn, per Action you have remaining, plus that many Actions for next Turn.")
        self.table = ["New Bear Order"]
        
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()

    def atTriggerTurnEnd(self, caster, dino, enemies):
        if caster.actions > 0:
            h.splash(caster.name + " had " + str(caster.actions) + " remaining Action at Turn End, so: //plus " + str(caster.actions) + " Action(s) for next Turn.")
            caster.plusUpcomingPlusAction(0, caster.actions)
        else:
            h.splash(caster.name + " did not have a positive number of Actions, so ^Wise Bear Skull^ does nothing.")

'''
## Placeholder for copypaste
class NAMEINSERTNAMEINSERTNAMEINSERTNAME(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = 
        self.bodyText = 
        self.table = 

'''





'''
## FOR ENEMY: Pile of Garbage
## Does Nothing. { Non-Permanent, Trash }
class toTossPlastic(DinoCard):
    def __init__(self):
        self.name = "To-Toss Plastic"
        self.bodyText = "Does Nothing. //{ Non-Permanent, Trash }"
        self.table = ["Trash"]
'''
"""

'''
    Fallow Farmland
'''
class scurrying(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Scurrying"
        self.bodyText = c.bb("+ Cantrip.")
        self.publishPacking("Move this onto the Into-Hand mat.")
        self.publishRoundStart("Heal 1L.")
        self.table = ["Fallow Farmland"]
        self.publishInitialization(intoHand = True)
            
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        
        success = caster.moveMe(caster.hand, self, caster.intoHand, supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, self, caster.intoHand)
        
    def atTriggerRoundStart(self, caster, dino, enemies):
        caster.heal(caster, dino, enemies, h.acons([1, 'L'], 'nil'))

class rustedScythe(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Rusted Scythe"
        self.bodyText = c.bb("2R / 1M. //You may: Discard your Hand for +2 Cards.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], h.acons([1, 'M'], 'nil')))
        query = h.yesOrNo("Discard your Hand for +2 Cards?", passedInVisuals = passedInVisuals)
        if query:
            while caster.hand.length() > 0:
                caster.moveCard(caster.hand, 0, caster.discard)
            for i in range(2):
                dino.drawCard()

class cultivator(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Cultivator"
        self.bodyText = c.bb("2M. Move this onto Deck.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'M'], 'nil'))
        caster.moveMe(caster.play, self, caster.draw, position = 0, supressFailText = True)

class brassMuzzle(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Brass Muzzle"
        self.bodyText = c.bb("Pick an Enemy. To it: 2B / 1M; Discard a Card.")
        self.table = ["Fallow Farmland"]
        
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
        if index != -1:
            enemies[index].damage(caster, dino, enemies, h.acons([2, 'B'], h.acons([1, 'M'], 'nil')))
            if enemies[index].hand.length() > 0:
                enemies[index].discardCard(enemies[index].hand, 0)

class deadHarvestedGrass(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Dead Harvested Grass"
        self.bodyText = c.bb("3G. Then: 1M.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], 'nil'))
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], 'nil'))

class gnawedCableCord(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Gnawed Cable Cord"
        self.bodyText = c.bb("+1 Action. 2B-notick. Move this onto Deck.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'B-notick'], 'nil'))
        index = h.locateCardIndex(caster.play, self)
        if index >= 0:
            caster.moveCard(caster.play, index, caster.draw, position = 0)
        else:
            h.splash('FAIL_MOVE')

class oxidizedShovel(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Oxidized Shovel"
        self.bodyText = c.bb("+ Cantrip. Draw until you have 3 Cards in Hand.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()
        priorLength = -1
        while caster.hand.length() < 3 and caster.hand.length() != priorLength:
            priorLength = caster.hand.length()
            caster.drawCard()

class grasshopperCache(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Grasshopper Cache"
        self.bodyText = c.bb("+ Cantrip.")
        self.publishPacking("3G. Move this onto Deck.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], 'nil'))
        
        success = caster.moveMe(caster.hand, self, caster.draw, position = 0, supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, self, caster.draw, position = 0)
        
"""
class fallowFieldMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Fallow Field Mantra"
        self.bodyText = c.bb("+ Cantrip. //+# Card(s); # = Number of ^Detritus^ in Hand and Play.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard(printCard = True)
        count = 0
        for card in caster.hand.getArray():
            if card.name == "Detritus":
                count += 1
        for card in caster.play.getArray():
            if card.name == "Detritus":
                count += 1 
        h.splash("Found " + str(count) + " ^Detritus^ across both Hand and Play.")
        for i in range(count):
            caster.drawCard()
    
    ''' def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        index = h.locateCardIndex(caster.hand, self)
        if index >= 0:
            caster.moveCard(caster.hand, index, caster.draw, position = 0)
        else:
            h.splash('FAIL_MOVE') '''
"""

class trampledRodent(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Trampled Rodent"
        self.bodyText = c.bb("1R-notick / 1G-notick / 1B-notick / 1M.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'R-notick'],
                                                             h.acons([1, 'G-notick'],
                                                             h.acons([1, 'B-notick'],
                                                             h.acons([1, 'M'],
                                                             'nil')))))

class twigRockScarecrow(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Twig Rock Scarecrow"
        self.bodyText = c.bb("Plus 1 Action for your Next Turn. //Move this onto Deck.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusUpcomingPlusAction(0, 1)

        index = h.locateCardIndex(caster.play, self)
        if index >= 0:
            caster.moveCard(caster.play, index, caster.draw, position = 0)
        else:
            h.splash('FAIL_MOVE')

class mangledShrew(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Mangled Shrew"
        self.bodyText = c.bb("2R-notick / 1Random / 1Random / 1Random.")
        self.table = ["Fallow Farmland"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R-notick'],
                                                             h.acons([1, 'Random'],
                                                             h.acons([1, 'Random'],
                                                             h.acons([1, 'Random'],
                                                             'nil')))))

class lastSeeds(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Last Seeds"
        self.bodyText = c.bb("+1 Action. 2L / 1M. //At the Bottom of Deck: Discard it, then Move this there.")
        self.table = ["Fallow Farmland"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'L'], h.acons([1, 'M'], 'nil')))
        
        if caster.draw.length() > 0:
            caster.discardCard(caster.draw, 0, inputCard = True)
        else:
            h.splash('FAIL_MOVE')
        
        index = h.locateCardIndex(caster.play, self)
        if index >= 0:
            caster.moveCard(caster.play, index, caster.draw, position = caster.draw.length())
        else:
            h.splash('FAIL_MOVE')

class coercionCultivator(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Coercion-Cultivator"
        self.bodyText = c.bb("Pick an Enemy. To it: 6Random. //If it is still alive, Pocket a ^Shovel^ Card.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        self.foreverLinger = True

        index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
        if index != -1:
            enemy = enemies[index]
            h.splash("To '" + enemy.name + "': 6Random.", printInsteadOfInput = True)
            enemy.damage(caster, dino, enemies, h.acons([6, 'Random'], 'nil'))
            if enemy.dead == False:
                h.splash("'" + enemy.name + "' is still alive, so Pocketing a ^Shovel^ Card.")
                dino.gainCard(shovel(), dino.pocket)
        
        ## while caster.hand.length() > 0:
        ##     caster.discardCard(caster.hand, 0)
 
class grayHubcap(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Green Hubcap"
        self.bodyText = c.bb("+1 Action. 2G. //0.85 Chance for: +1 Card.")
        self.publishPacking("Move the top Card of Draw onto the Into-Hand mat.")
        self.table = ["Bandits of the Highway"]
 
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'G'], 'nil'))
        if random.random() < 0.85:
            h.splash("Succeeded 0.85 Chance: +1 Card.")
            caster.drawCard()
        else:
            h.splash("Failed 0.85 Chance for: +1 Card.")

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)

class highwayGrassMedian(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Highway-Grass Median"
        self.bodyText = c.bb("+1 Action. 2G / 2B. //0.15 Chance for: +1 Card.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], h.acons([1, 'B'], 'nil')))
        if random.random() < 0.15:
            h.splash("Succeeded 0.15 Chance: +1 Card.")
            caster.drawCard()
        else:
            h.splash("Failed 0.15 Chance for: +1 Card.")

class metalTrashBins(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Metal Trash Bins"
        self.bodyText = c.bb("1M / 1M / 1M. Gain a ^Rubbish^.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], h.acons([1, 'M'], h.acons([1, 'M'], 'nil'))))
        caster.gainCard(rubbish(), dino.discard)

class wheelShrapnel(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Wheel Shrapnel"
        self.bodyText = c.bb("+1 Action. 2R / 2M. Discard your Hand.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], h.acons([2, 'M'], 'nil')))
        while caster.hand.length() > 0:
            caster.discardCard(caster.hand, 0)
        
class shamSpeedSign(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Sham Speed Sign"
        self.bodyText = c.bb("+2 Cards. Gain a ^Rubbish^.")
        self.publishPacking("Pocket this.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        for i in range(2):
            caster.drawCard()
        caster.gainCard(rubbish(), dino.discard)
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        success = caster.moveMe(caster.hand, self, caster.pocket, supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, self, caster.pocket)

class bandItBond(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Band-it Bond"
        self.bodyText = c.bb("Pick an Enemy. To it: Destroy a Band. //Discard your Hand.")
        self.table = ["Bandits of the Highway"]
        
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        
        index = h.pickLivingEnemy("Pick Enemy", enemies, passedInVisuals = passedInVisuals)
        if index != -1:
            enemy = enemies[index]
            h.splash("To '" + enemy.name + "': Destroy a Band.", printInsteadOfInput = True)
            enemy.destroyBand(dino, enemies)
        while caster.hand.length() > 0:
            caster.discardCard(caster.hand, 0)

        
'''
class chasedBanditPack(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Chased Bandit Pack"
        self.bodyText = c.bb("6G."
'''

class infiltratorInterrogator(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Infiltrator-Interrogator"
        self.bodyText = c.bb("+1 Action. Pocket a ^Shovel^ Card. //Move the top Card of Draw onto the Pocket Mat. Gain a ^Rubbish^.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.gainCard(shovel(), dino.pocket)
        if caster.draw.length() > 0:
            caster.moveCard(caster.draw, 0, caster.pocket)
        else:
            h.splash('FAIL_MOVE')
        
        caster.gainCard(rubbish(), dino.discard)

class raccoonHeist(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Raccoon Heist"
        self.bodyText = c.bb("Pocket a ^Shovel^ Card.")
        self.publishPacking("2B.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.gainCard(shovel(), dino.pocket)
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'B'], 'nil'))
    
class roadSignAugers(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Road Sign Augers"
        self.bodyText = c.bb("2Random.")
        self.publishRoundStart("Pocket a ^Shovel^ Card.")
        self.table = ["Bandits of the Highway"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'Random'], 'nil'))
    
    def atTriggerRoundStart(self, caster, dino, enemies):
        caster.gainCard(shovel(), caster.pocket)

class waverOver(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Waver-Over"
        self.bodyText = c.bb("+2 Actions. 2R.")
        self.table = ["Bandits of the Highway"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(2)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], 'nil'))

class carFeigning(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Car Feigning"
        self.bodyText = c.bb("1G / 1R. If your Hand is Empty: + Cantrip; + Cantrip.")
        self.publishPacking("Pocket this.")
        self.table = ["Bandits of the Highway"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], h.acons([1, 'R'], 'nil')))
        if dino.hand.length() == 0:
            h.splash("Hand is Empty, so + Cantrip, + Cantrip.")
            for i in range(2):
                caster.plusActions(1)
                caster.drawCard()
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        success = caster.moveMe(caster.hand, self, caster.pocket, supressFailText = True)
        if not success:
            caster.moveMe(caster.pocket, self, caster.pocket)

'''
    New Bear Order Cards
'''

class torchBearing(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Torch Bearing"
        self.bodyText = c.bb("+2 Actions.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(2)

class treeClimbers(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Tree Climbers"
        self.bodyText = c.bb("+1 Card. 3G / 2G.")
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.drawCard(printCard = True)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'G'], h.acons([2, 'G'], 'nil')))

class recyclingBin(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Recycling Bin"
        self.bodyText = c.bb("3B / 2G. //Discard your Hand.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'B'], h.acons([2, 'G'], 'nil')))
        while caster.hand.length() > 0:
            caster.discardCard(caster.hand, 0)

class boneGnaw(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bone-Gnaw"
        self.bodyText = c.bb("+1 Card. 1M / 1M / 1M / 1M. //Take 1M-self Damage.")
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.drawCard(printCard = True)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], h.acons([1, 'M'], h.acons([1, 'M'], h.acons([1, 'M'], 'nil')))))
        caster.damage(caster, dino, enemies, h.acons([1, 'M'], 'nil'))

class shoulderHump(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shoulder Hump"
        self.bodyText = c.bb("4Random / 3Random.")
        self.publishPacking("{ 1H } Move this into Play, for: Next Turn, +1 Action.")
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([4, 'Random'], h.acons([3, 'Random'], 'nil')))
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        self.monotonicLingering(1)
        success = caster.moveMe(caster.hand, self, caster.play, supressFailText = True)
        if not success:
            success = caster.moveMe(caster.pocket, self, caster.play)
        
        if success:
            self.custom1 = True
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if (self.turnsLingering == 1 and self.custom1 == True):
            caster.plusActions(1)
            self.custom1 = False

class honeyPot(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Honey Pot"
        self.bodyText = c.bb("Discard your Hand. //Next Turn, +2 Actions.")
        self.bodyText.heavinessText("{ 1H }")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        self.monotonicLingering(1)
        while caster.hand.length() > 0:
            caster.discardCard(caster.hand, 0)
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            caster.plusActions(2)

class hibernation(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Hibernation"
        self.bodyText = c.bb("To each Enemy that has yet to take a Turn: Discard their Hand.")
        self.publishInitialization(top = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
            
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        utterFailure = True
        for enemy in enemies:
            if enemy.turn == 0:
                utterFailure = False
                h.splash("To '" + enemy.name + "': Discarding their Hand.", printInsteadOfInput = True)
                while enemy.hand.length() > 0:
                    enemy.discardCard(enemy.hand, 0)
        if utterFailure:
            h.splash(" Does Nothing. ")

class bearClaws(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bear Claws"
        self.bodyText = c.bb("3R / 3B.")
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'R'], h.acons([3, 'B'], 'nil')))

class backScratcher(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Back Scratcher"
        self.bodyText = c.bb("+ Cantrip. 10L.")
        self.publishInitialization(discard = True)
        self.publishReshuffle(top = True)
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        caster.drawCard()
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([10, 'L'], 'nil'))

class beesNest(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Bees Nest"
        self.bodyText = c.bb("3x, to an arbitrary Enemy: 3L. //Next Turn, +1 Action.")
        self.bodyText.heavinessText("{ 1H }")
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        self.monotonicLingering(1)

        for i in range(3):
            livingEnemies = []
            for enemy in enemies:
                if enemy.dead == False:
                    livingEnemies.append(enemy)
            if len(livingEnemies) > 0:
                enemy = random.choice(livingEnemies)
                h.splash("To '" + enemy.name + "': 3L.", printInsteadOfInput = True)
                enemy.damage(caster, dino, enemies, h.acons([3, 'L'], 'nil'))
            else:
                h.splash("FAIL_FIND_ENEMY")
    
    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            caster.plusActions(1)

class leaveNoTraceMantra(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Leave No Trace Mantra"
        self.bodyText = c.bb("+2 Actions. Move an arbitrary non-^Muck^ Card from Discard into Hand.")
        self.table = ["New Bear Order"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(2)
        
        caster.discard.shuffle()
        index = 0
        match = False
        while match == False and index < caster.discard.length():
            if "Muck" not in caster.discard.getArray()[index].table:
                match = True
                caster.moveCard(caster.discard, index, caster.hand, position = caster.hand.length())
            index += 1
        if match == False:
            h.splash("FAIL_MOVE")

class rightToBearArms(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Right to Bear Arms"
        self.bodyText = c.bb("+2 Cards.")
        self.publishPacking("Move the top 2 Cards of Draw onto the Into-Hand Mat.")
        self.table = ["New Bear Order"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        for i in range(2):
            caster.drawCard()
        
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        for i in range(2):
            caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, printCard = True)

'''
    Packing Bot Cards
'''
class metalCrate(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Metal Crate"
        self.bodyText = c.bb("2M / 2M.")
        self.bodyText.heavinessText("{ HH }")
        self.bodyText.lootingText("When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        self.foreverLinger = True
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'M'], h.acons([2, 'M'], 'nil')))
        
    def onReplacedWithLoot(self, dino):
        h.splash("Triggered On Replaced with Loot: +1 Looting.")
        dino.looting += 1

class packingPeanuts(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Packing Peanuts"
        self.bodyText = c.bb("+1 Action. To all Enemies, in order: 1L.")
        self.table = ["Packing Bot"]
        
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        for enemy in enemies:
            if enemy.dead == False:
                h.splash("To '" + enemy.name + "': 1L.", printInsteadOfInput = True)
                enemy.damage(caster, dino, enemies, h.acons([1, 'L'], 'nil'))

class shippingTape(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Shipping Tape"
        self.bodyText = c.bb("2R / 1M.")
        ## self.bodyText.lootingText("WTID, when you Loot a Card, you may change its Initialization Location to: (1) Top; (2) Bottom; (3) Discard.")
        self.table = ["Packing Bot"]
        
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([2, 'R'], h.acons([1, 'M'], 'nil')))

class forkliftCertificate(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Forklift Certificate"
        self.bodyText = c.bb("+1 Action. +2 Cards. //At Turn End, if you have 2+ ^Detritus^ in Play: Move this onto Draw.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Packing Bot"]

        self.triggers.append(h.reaction(self, False, endOfDinoTurn = True))
        self.END_OF_DINO_TURN_RT = h.rt(False, "^" + self.name + "^", "2+ ^Detritus^ in Play", "Move this onto Draw")
        ## Static because: the trigger is always 100% what it says it will be. 

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        self.foreverLinger = True
        caster.plusActions(1)
        for i in range(2):
            caster.drawCard()

    def endOfDinoTurnCondition(self, caster, dino, enemies):
        detritusCount = 0
        ## Sees if Card is in desired Location
        if h.locateCardIndex(caster.play, self) >= 0:
            ## Sees if Card there exists a Detritus in Play
            for card in caster.play.getArray():
                if (card.name == "Detritus"):
                    detritusCount += 1
        return (detritusCount >= 2, self.END_OF_DINO_TURN_RT)

    def endOfDinoTurnTriggered(self, caster, dino, enemies):
        index = h.locateCardIndex(caster.play, self)
        if index >= 0:
            caster.moveCard(caster.play, index, caster.draw, position = 0)
            h.splash(self.END_OF_DINO_TURN_RT.getText(), printInsteadOfInput = True)
            # reacted = True
        else:
            h.splash('FAIL_MOVE')

class newFreshAir(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "New Fresh Air"
        self.bodyText = c.bb("+1 Action. 1G-notick.")
        self.publishPacking("1G-notick.")
        self.table = ["Packing Bot"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G-notick'], 'nil'))

class stampGun(DinoCard):
    def __init__(self): 
        super().__init__()
        self.name = "Stamp Gun"
        self.bodyText = c.bb("1G / 1B.")
        self.publishPacking("Move the top Card of Draw onto the Into-Hand mat.")
        self.table = ["Packing Bot"]
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'G'], h.acons([1, 'B'], 'nil')))
    
    def onPacking(self, caster, dino, enemies, passedInVisuals):
        super().onPacking(caster, dino, enemies, passedInVisuals)
        caster.drawCard(fromLocation = caster.draw, toLocation = caster.intoHand, shuffleLocation = caster.discard, inputCard = True)
    
class warehouseHelmet(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Warehouse Helmet"
        self.bodyText = c.bb("+3 Cards.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Packing Bot"]

    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        self.foreverLinger = True
        for i in range(3):
            caster.drawCard()

class batteryPack(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Battery Pack"
        self.bodyText = c.bb("3R.")
        ## self.table = ["Packing Bot"]
        self.table = []
    
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([3, 'R'], 'nil'))

class potpourri(DinoCard):
    def __init__(self):
        super().__init__()
        self.name = "Potpourri"
        self.bodyText = c.bb("1M.")
        ## self.bodyText.push("looting", "When Replaced with Loot: +1 Looting.")
        self.table = ["Packing Bot"]
        
    def duringPlay(self, caster, dino, enemies, passedInVisuals):
        super().duringPlay(caster, dino, enemies, passedInVisuals)
        c.dealDamage(caster, dino, enemies, passedInVisuals, h.acons([1, 'M'], 'nil'))
