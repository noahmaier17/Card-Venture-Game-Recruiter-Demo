"""
enemieses.py

Includes all the enemy entities, as well as the class by which they all inherit.
"""

import math
import random

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import getCardsByTable as gcbt
from Dinosaur_Venture import helper as h
from Dinosaur_Venture import mainVisuals as vis
from Dinosaur_Venture.entities import entity as e


class Enemy(e.Entity):
    """General enemy class; works well for testing and inheritance"""
    def __init__(self) -> None:
        super().__init__()

    def fillDeck(self, extraDrafts: h.cardLocation = h.cardLocation("extra drafts")) -> None:
        """Fills this enemy's deck based on its `damageDist` and `siftDist` values."""
        # THE IMPLEMENTATION OF EXTRA DRAFTS ALSO NEEDS AN ODDS NUMBER OR SOMETHING
        EFD = h.cardLocation("EFD")

        # Pre-processing, finding all cards that are reasonable-enough matches
        for Card in gcbt.ENEMY_CARD_POOL_UNINIT:
            card = Card(targetDamage = self.damageDist, targetSift = self.siftDist)
            deltaDamage = (card.damageDist - self.damageDist)
            deltaSift = (card.siftDist - self.siftDist)
            if (math.sqrt(deltaDamage ** 2 + deltaSift ** 2) <= 0.8):
                EFD.append(card)

        # Adds extra drafts to the list too
        for card in extraDrafts.getArray():
            EFD.append(card)

        # Selects cards randomly, and if they pass a probability check, adds them
        while (self.deck.length() < 6):
            if EFD.length() == 0:
                # Case where we cannot add any more Cards
                self.deck.append(gcbt.getCardByName("Nothing"))
            else:
                card = EFD.pop(random.randint(0, EFD.length() - 1))

                deltaDamage = (card.damageDist - self.damageDist)
                deltaSift = (card.siftDist - self.siftDist)

                if (random.random() >= math.sqrt(deltaDamage ** 2 + deltaSift ** 2)):
                    # We passed the randomness check -- adds this Card to the selection
                    self.deck.append(card)
                else:
                    # We failed the randomness check -- tries again
                    EFD.append(card)

'''
class Litterbugs(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Loiterers of nearby grime and filth, both in body and morality."
        self.name = "Litterbugs"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 0.75
        self.siftDist = 1
        super().fillDeck()
        
        self.difficulty = 1
    
    def __healthInit(self):
        hpA = [0.3, 0, 0]
        random.shuffle(hpA)
        hpB = [2, 1, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))
'''

class plainEnemy(Enemy):
    """Plain, bland enemy."""
    def __init__(self):
        super().__init__()
        self.text = "A plain Enemy."
        self.name = "Enemy"
        self.initialEnemyName = self.name

        self.damageDist = -1
        self.siftDist = -1

        self.difficulty = -1

    def plainEnemyInit(self, name, difficulty, damageDist, targetHealth, siftDist):
        super().__init__()
        self.text = "A plain Enemy."
        self.name = name
        self.initialEnemyName = self.name

        self.damageDist = damageDist
        self.siftDist = siftDist
        super().fillDeck()

        self.targetHealth = targetHealth
        self.hp = cll.Healthcons(0, 0, 0, 'nil')
        self.plainEnemyHealthInit(self.hp, targetHealth)

        self.difficulty = difficulty

    def plainEnemyHealthInit(self, hp, target):
        ## print(" -------------- ")
        self.__hpStart(hp, target)

    def __hpStart(self, hp, target):
        ## input("S: " + str(target))
        channels = [hp.r, hp.g, hp.b]
        if (target <= 0 and not max(channels) == 0):
            return

        if (target <= 0 and max(channels) == 0) or (target == 1):
            chl = random.randint(0, 2)
            if chl == 0:
                hp.r = 1
            elif chl == 1:
                hp.g = 1
            else:
                hp.b = 1
            return
        else:
            return self.__hpContinue(hp, target)

    def __hpContinue(self, hp, target):
        ## input("C: " + str(target))
        if target <= 0:
            return

        channels = [hp.r, hp.g, hp.b]
        emptyChannels = 0
        for chl in channels:
            if chl == 0:
                emptyChannels += 1

        if emptyChannels == 3:
            return self.__hpInset(hp, target)
        elif emptyChannels == 0:
            return self.__hpBand(hp, target)

        elif emptyChannels == 1:
            if random.random() < (0.85 / 2):
                return self.__hpInset(hp, target)
            return self.__hpBand(hp, target)
        else:
            if random.random() < 0.85:
                return self.__hpInset(hp, target)
            return self.__hpBand(hp, target)

    def __hpInset(self, hp, target):
        ## input("I: " + str(target))
        channels = [hp.r, hp.g, hp.b]
        emptyChannels = []
        pos = 0
        for chl in channels:
            if chl == 0:
                emptyChannels.append(pos)
            pos += 1
        chl = random.randint(0, len(emptyChannels) - 1)

        if chl == 0:
            hp.r = 1
            target -= 1
            while target > 0 and random.random() < 0.5:
                hp.r += 1
                target -= 1
        elif chl == 1:
            hp.g = 1
            target -= 1
            while target > 0 and random.random() < 0.5:
                hp.g += 1
                target -= 1
        else:
            hp.b = 1
            target -= 1
            while target > 0 and random.random() < 0.5:
                hp.b += 1
                target -= 1
        return self.__hpContinue(hp, target)

    def __hpBand(self, hp, target):
        ## input("B: " + str(target))
        target -= 1
        hp.tail = cll.Healthcons(0, 0, 0, 'nil')
        return self.__hpStart(hp.tail, target)

class Fisherman(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Ravenous Fisherman"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Crave Fish Mantra"))
        self.damageDist = 1.8
        self.siftDist = 0.75
        super().fillDeck()

        self.difficulty = 3

    def __healthInit(self):
        hpA = [1, 1, 2]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class FishingCaravan(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Fishing Caravan"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Fish Frenzy"))
        if random.random() < 0.25:
            self.deck.append(gcbt.getCardByName("Fish Frenzy"))
            if random.random() < 0.1:
                self.deck.append(gcbt.getCardByName("Fish Frenzy"))
        self.damageDist = 1.35
        self.siftDist = 1.25
        super().fillDeck()

        self.difficulty = 6.75

    def __healthInit(self):
        hpA = [0, 2, 2]
        random.shuffle(hpA)
        hpB = [0, 2, 2]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

class FlyingSquirrel(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Flying Squirrel"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Prepare To Fly"))
        self.damageDist = 0.8
        self.siftDist = 1.2
        super().fillDeck()

        self.difficulty = 3

    def __healthInit(self):
        hpA = [2, 2, 2]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')


class MalabarGiantSquirrel(Enemy):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.name = "Malabar Giant Squirrel"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.deck.append(gcbt.getCardByName("Going Nuts"))
        self.damageDist = 1
        self.siftDist = 1
        super().fillDeck()

        self.difficulty = 2.75

    def __healthInit(self):
        hpA = [5, 0, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class Copperals(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Small copper critters, fighting for what is right."
        self.name = "Copperals"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.damageDist = 0.75
        self.siftDist = 1
        super().fillDeck()

        self.difficulty = 2

    def __healthInit(self):
        hpA = [2, 2, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class Rusterials(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "The forgotten, disillusioned, and angry."
        self.name = "Rusterials"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        self.publishBandBreak(1, discardHand = True)

        self.damageDist = 2
        self.sistDist = 1
        super().fillDeck()

        self.difficulty = 4.75

    def __healthInit(self):
        hpA = [4, 2, 0]
        hpB = [1, 0, 0]
        random.shuffle(hpA)
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)

class Karkit(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A baby Skunk."
        self.name = "Karkit"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.damageDist = 0.75
        self.siftDist = 1.5
        super().fillDeck()

        self.difficulty = 0.75

    def __healthInit(self):
        hpA = [2, 0, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')

class Skunk(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "They reek."
        self.name = "Skunk"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 1
        self.siftDist = 1.25
        super().fillDeck()
        
        self.difficulty = 1.75
    
    def __healthInit(self):
        hpA = [1, 0, 0]
        random.shuffle(hpA)
        hpB = [2, 2, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

class RaccoonBandit(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Bandits of the Night, first you must unmask them in order to chase them away."
        self.name = "Raccoon Bandit"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        ## self.publishBandBreak(1, discardHand = True)
    
        self.damageDist = 1.25
        self.siftDist = 1.25
        super().fillDeck()
        
        self.difficulty = 2.75
    
    def __healthInit(self):
        hpA = [2, 0, 0]
        random.shuffle(hpA)
        hpB = [2, 0, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))
    
    ''' def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)
    '''

## Hoard of Shrews
class HoardOfShrews(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A Legion of Shrews, jealous of each other, far more feral in a pack than alone."
        self.name = "Hoard Of Shrews"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        self.publishBandBreak(1, discardHand = True)

        self.damageDist = 1.45
        self.siftDist = 1
        super().fillDeck()
        
        self.difficulty = 2.75
    
    def __healthInit(self):
        hpA = [2, 1, 0]
        random.shuffle(hpA)
        hpB = [2, 1, 0]
        random.shuffle(hpB)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))
    
    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)

## Shrew -- A timid creature, easily frightened. 
class Shrew(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A timid creature, easily frightened."
        self.name = "Shrew"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()

        self.damageDist = 0.67
        self.siftDist = 0.5
        super().fillDeck()

        self.difficulty = 1.75

    def __healthInit(self):
        hpA = [2, 1, 0]
        random.shuffle(hpA)
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 'nil')
    
    def atTriggerTargetedToTakeDamage(self, dino, enemies):
        chance = random.random()
        if (chance <= 0.1 and not self.dead):
            h.splash("Triggered Gimmick: [ 0.1 Chance when Targeted to Take Damage ] ARR [ Discard Hand ].")
            while (self.hand.length() > 0):
                self.discardCard(self.hand, 0, dino, enemies, vis.prefabEmpty)

## Torch Bear -- It calls to the wild for apostles of the new order. 
class CinnamonBear(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "It calls to the wild for apostles of what can become of a New Order; only 'Shrews' heed the call."
        self.name = "Torch Bearer"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        self.publishBandBreak(1, discardHand = True)

        self.deck.append(gcbt.getCardByName("Soapbox Stump"))
        self.damageDist = 1.1
        self.siftDist = 1.1
        super().fillDeck()
        
        self.difficulty = 7.25

    def __healthInit(self):
        hp = [0, 2, 3]
        random.shuffle(hp)
        return cll.Healthcons(hp[0], hp[1], hp[2], cll.Healthcons(hp[2], hp[1], hp[0], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Band Broken: '" + self.name + "' Discarding Hand.")
            
            while self.hand.length() > 0:
                self.moveCard(self.hand, 0, self.discard)

## Babybear -- The upcoming new beneficiary, disillusioned by how small of land they shall inherit. 
class Babybear(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "The upcoming new beneficiary, disillusioned by how small of a land they shall inherit."
        self.name = "Babybear"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(gcbt.getCardByName("Demanding Inheritance"))
        self.damageDist = 1
        self.siftDist = 1
        super().fillDeck()
        
        self.difficulty = 1.45
    
    def __healthInit(self):
        hp = [3, 0, 0]
        random.shuffle(hp)
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')



"""
## Torchbearer -- Eventually, its facade of leadership and pride shall falter, in which its once-was followers will turn on it. 
class Torchbearer(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "It gives off a boastful presence, at least until it falls from its prideful rock and is turned on by its once-were followers. //Special Gimmick: At Turn End, if 'Torchbearer' has 2 Bands: 'Torchbearer' gets 1 additional Action next turn. //Special Gimmick: When 'Torchbearer' loses a Band, -1 Actions, and per each living Enemy: self-damage 2M."
        self.name = "Torchbearer"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 1
        self.siftDist = 0.5
        super().fillDeck()
        
        self.difficulty = 8

    def __healthInit(self):
        hpA = [2, 2, 0]
        random.shuffle(hpA)
        hpB = [2, 2, 2]
        
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Triggered Special Gimmick: When 'Torchbearer' loses a Band, -1 Actions, and per each living Enemy: self-damage 2M.")
            self.minusActions(1)
            count = 0
            for enemy in enemies:
                if enemy.dead == False:
                    count += 1
            for i in range(count):
                self.damage(self, dino, enemies, cll.Attackcons([2, 'M'], 'nil'))
    
    def atTriggerTurnEnd(self, dino, enemies):
        if self.getBands() == 2:
            h.splash("Triggered Special Gimmick: At Turn End, if 'Torchbearer' has 2 Bands: 'Torchbearer' gets 1 additional Action next turn.")
            self.plusUpcomingPlusAction(0, 1)
    
## Discarded Plastic -- 
##  Focus: Helps with +Actions, hurts medium sifting. 
class DiscardedPlastic(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Discarded Plastic"
        self.initialEnemyName = self.name 
        self.hp = self.__healthInit()
        
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
        self.deck.append(ec.nothing())
    
        self.difficulty = 1
    
    def __healthInit(self):
        return cll.Healthcons(0, 0, 0, 'nil')
    
    def atTriggerDinoPlayedCard(self, dino, enemies):
        if len(dino.play) > 1 and self.didOnceARoundAtTriggerDinoPlayedCard == False and self.dead == False:
            self.didOnceARoundAtTriggerDinoPlayedCard = True
            h.splash("Triggered Special Gimmick: Once a Round, while 'Discarded Plastic' is Alive: if '" + str(dino.name) + "' has more than 1 Card in play: Dino gains 'To-Toss Plastic,' and draws 1 additional Card next Turn.")
            dino.discard.append(gcbt.getCardByName("To-Toss Plastic"))
            dino.plusUpcomingPlusCard(0, 1)

## Grizzly -- More than any other bear does it despise what has come of the species. 
class Grizzly(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "More than any other Bear does it despise what has come of the species. //Special Gimmick: While Alive, at Turn End, 'Grizzly' heals 1L and self-damages 1M."
        self.name = "Grizzly"
        self.initialEnemyName = self.name 
        self.hp = self.__healthInit()
        
        self.damageDist = 1.25
        self.siftDist = 0.8
        super().fillDeck()
        
        self.difficulty = 7

    def __healthInit(self):
        hp = [0, 2, 4]
        random.shuffle(hp)
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')
    
    ''' def atTriggerTurnEnd(self, dino, enemies):
        if self.dead == False:
            # h.splash("Triggered Special Gimmick: While Alive, at Turn End, 'Grizzly' heals 1L and self-damages 1M.")
            self.heal(self, dino, enemies, cll.Attackcons([1, 'L'], 'nil'))
            self.damage(self, dino, enemies, cll.Attackcons([1, 'M'], 'nil')) '''
    
## Shrew -- A small, puny rodent, easily frightened. 
class Shrew(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "A small, puny rodent, trying to be courageous."
        self.name = "Shrew"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.musterCourage())
        self.damageDist = 0.6
        self.siftDist = 0.6
        super().fillDeck()
        
        self.difficulty = 1

    def __healthInit(self):
        hp = [0, 0, 0]
        hp[random.randint(0, 2)] = 1
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

## Belly-Filled Shrew -- That small, puny rodent, now full of grass in its stomach. 
class BellyFilledShrew(Shrew):
    def __init__(self):
        super().__init__()
        self.name = "Belly-Filled Shrew"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 0.7
        self.siftDist = 0.5
        super().fillDeck()
        
        self.difficulty = 1.5
    
    def __healthInit(self):
        hp = [0, 0, 0]
        hp[random.randint(0, 2)] = 2
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

## Enshrined Capybara -- Enveloped in metal, with metal-sharpened teeth. 
##  Special Gimmick: When it loses a band and only has 1 remaining, it discards its hand. 
class EnshrinedCapybara(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Enveloped in thin metal, with metal-sharpened teeth. //Special Gimmick: When 'Enshrined Capybara' loses a Band and has only 1 left, it discards its hand."
        self.name = "Enshrined Capybara"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.twoMetalTeeth())
        self.deck.append(ec.frightened1())
        self.damageDist = 0.3
        self.siftDist = 0.3
        super().fillDeck()
        
        self.difficulty = 4.75
    
    def __healthInit(self):
        hpA = [0, 0, 0]
        hpA[random.randint(0, 2)] = 1
        
        hpB = [2, 2, 2]
        hpB[random.randint(0, 2)] = 0
        return cll.Healthcons(hpA[0], hpA[1], hpA[2],
            cll.Healthcons(hpB[0], hpB[1], hpB[2], 'nil'))

    def atTriggerLoseBand(self, dino, enemies):
        if self.getBands() == 1:
            h.splash("Triggered Special Gimmick: 'Enshrined Capybara' lost a Band and has only 1 left, so: discard Hand.")
            size = len(self.hand)
            for i in range(size):
                self.moveCard(self.hand, 0, self.discard)

## Prairie Watch Dog -- Defends its kind with its life. 
class PrairieWatchDog(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "It defends its kind with its life. //Special Gimmick: Once a Turn, while 'Prairie Watch Dog' is alive: when an Enemy is damaged non-fatally: +1 Action, play a Card from Hand, and self-damage 1M."
        self.name = "Prairie Watch Dog"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.damageDist = 0.85
        self.siftDist = 0.45
        super().fillDeck()
        
        self.difficulty = 2

    def __healthInit(self):
        hp = [1, 1, 1]
        hp[random.randint(0, 2)] = 0
        
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

    def atTriggerAnyEnemyNonfatallyDamaged(self, damageTaker, dino, enemies):
        if self.didOnceATurnAtTriggerNonfatalDamageTaken == False and self.dead == False:
            h.splash("Triggered Special Gimmick: Once a Turn, while 'Prairie Watch Dog' is alive: when an Enemy is damaged non-fatally: +1 Action, play a Card from Hand, and self-damage 1M.")
            self.didOnceATurnAtTriggerNonfatalDamageTaken = True
            
            self.plusActions(1)
            cardIndex = self.cardIntellect()
            if cardIndex != "nil":
                card = self.hand[cardIndex]
                print(" | Resolution of: " + Back.RED + Fore.BLACK + " " + card.name + " ")
                print(" |  > " + card.niceBodyText(3, 100))
                input(" | ... ")
                self.playCard(self.hand, cardIndex, self, dino, enemies)
            else:
                h.splash("It could not play any Cards.")
        
            self.damage(self, dino, enemies, cll.Attackcons([1, 'M'], 'nil'))

## Squirrel Researcher -- Trying to better understand this forsaken place. 
class SquirrelResearcher(Enemy):
    def __init__(self):
        super().__init__()
        self.text = "Trying to better understand this forsaken place."
        self.name = "Squirrel Researcher"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.yellowPadResearch())
        self.deck.append(ec.loosePapers())
        self.damageDist = 1.5
        self.siftDist = 0.5
        super().fillDeck()
        
        self.difficulty = 3

    def __healthInit(self):
        hp = [1, 1, 1]
        hp[random.randint(0, 2)] = 2
        
        return cll.Healthcons(hp[0], hp[1], hp[2], 'nil')

class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.difficulty = 5

class TheMoltOfHundreds(BossEnemy):
    def __init__(self):
        super().__init__()
        self.text = "The nectar of a sun-melted Mech lured the naive who believed its false promise of immortality."
        self.name = "The Molt of Hundreds!"
        self.initialEnemyName = self.name
        self.hp = self.__healthInit()
        
        self.deck.append(ec.shearedCreature())
        self.damageDist = 2
        self.siftDist = 0.5
        super().fillDeck()
        
    def __healthInit(self):
        hpA = [2, 2, 2]
        
        hpB = [2, 2, 2]
        hpB[random.randint(0, 2)] = 0

        hpC = [0, 0, 0]
        hpC[random.randint(0, 2)] = 2
        
        return cll.Healthcons(hpA[0], hpA[1], hpA[2], 
            cll.Healthcons(hpB[0], hpB[1], hpB[2], 
                cll.Healthcons(hpC[0], hpC[1], hpC[2], 'nil')))

    def atTriggerLoseBand(self, dino, enemies):
        h.splash("Triggered Special Gimmick: Lost a Band, so: Summoning a 'Shrew.'")
        summonedEnemy = Shrew()
        summonedEnemy.roundStart()
        enemies.append(summonedEnemy)
        for enemy in enemies:
            enemy.atTriggerEnemySummoned(summonedEnemy, dino, enemies)
"""