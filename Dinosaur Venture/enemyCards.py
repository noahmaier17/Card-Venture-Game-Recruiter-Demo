import math, random, os
import card as c
import helper as h
import entity as e
import getCardsByTable as gcbt
import cardFunctions as cf

## Initiates all enemy cards
class EnemyCard(c.Card):
    def __init__(self, damageDist, siftDist, likelihood):
        super().__init__(likelihood, damageDist, siftDist)

## -- Parameters for difficulty --
## Cards that do something next turn get taxed based on the virtue that
##  what is upcoming can be accounted for.
TAX_NEXT_TURN = 0.67

## Cards that give +1 Action have target damage values based on average
##  expected card output multiplied by same tax value.
TAX_PLUS_ONE_ACTION = 1

## Calculations:
"""
    This all uses the calculations found in the Google Doc. I have made it so some parameters
    can be manually adjusted quickly. In the future, I could make everything a tune-able parameter,
    but I like the system I have in place and want to test it out first.
"""

## -- GENERAL ENEMY CARDS --
## Does nothing.
class nothing(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = -1, siftDist = 0, likelihood = 0.15)
        self.name = "Nothing"
        self.bodyText = c.bb("Does Nothing.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            pass

## 1R.
class redAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1, siftDist = 0.5, likelihood = 0.5)
        self.name = "Red Nibble"
        self.bodyText = c.bb("1R.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'R'], 'nil'))

## 1G.
class greenAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1, siftDist = 0.5, likelihood = 0.5)
        self.name = "Green Nibble"
        self.bodyText = c.bb("1G.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'G'], 'nil'))

## 1B.
class blueAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1, siftDist = 0.5, likelihood = 0.5)
        self.name = "Blue Nibble"
        self.bodyText = c.bb("1B.")   
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'B'], 'nil'))

## 1Random.
class randomAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Frenzied Nibble"
        self.bodyText = c.bb("1Random.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'Random'], 'nil'))

## 2R.
class doubleRedAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2, siftDist = 0.5, likelihood = 0.5)
        self.name = "Red Bite"
        self.bodyText = c.bb("2R.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'R'], 'nil'))

## 2G.
class doubleGreenAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2, siftDist = 0.5, likelihood = 0.5)
        self.name = "Green Bite"
        self.bodyText = c.bb("2G.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'G'], 'nil'))

## 2B.
class doubleBlueAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2, siftDist = 0.5, likelihood = 0.5)
        self.name = "Blue Bite"
        self.bodyText = c.bb("2B.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'B'], 'nil'))

## 2Random.
class doubleRandomAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Frenzied Bite"
        self.bodyText = c.bb("2Random.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'Random'], 'nil'))

## 1M. 
class smallMaw(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Small Maw"
        self.bodyText = c.bb("1M.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'M'], 'nil'))

## 2M. 
class maw(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Maw"
        self.bodyText = c.bb("2M.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'M'], 'nil'))

## Next turn, +1 Action. 
class prepare(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = (targetDamage * TAX_PLUS_ONE_ACTION) * (TAX_NEXT_TURN ** 1),
            siftDist = 0.5,
            likelihood = 0.5)
        self.name = "Prepare"
        self.bodyText = c.bb("Next Turn, +1 Action.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        caster.plusActions(1)

## 1R-notick. 
class redNip(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.67, siftDist = 1, likelihood = 0.5)
        self.name = "Red Nip"
        self.bodyText = c.bb("1R-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'R-notick'], 'nil'))

## 1G-notick. 
class greenNip(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.67, siftDist = 1, likelihood = 0.5)
        self.name = "Green Nip"
        self.bodyText = c.bb("1G-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'G-notick'], 'nil'))

## 1B-notick. 
class blueNip(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.67, siftDist = 1, likelihood = 0.5)
        self.name = "Blue Nip"
        self.bodyText = c.bb("1B-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'B-notick'], 'nil'))

## 2R-notick. 
class redPeck(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.67, siftDist = 1, likelihood = 0.5)
        self.name = "Red Peck"
        self.bodyText = c.bb("2R-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'R-notick'], 'nil'))

## 2G-notick. 
class greenPeck(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.67, siftDist = 1, likelihood = 0.5)
        self.name = "Green Peck"
        self.bodyText = c.bb("2G-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'G-notick'], 'nil'))

## 2B-notick. 
class bluePeck(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.67, siftDist = 1, likelihood = 0.5)
        self.name = "Blue Peck"
        self.bodyText = c.bb("2B-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'B-notick'], 'nil'))

## 2R-notick. +1 Card.
class RedTrot(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.85, siftDist = 1.5, likelihood = 0.5)
        self.name = "Red Trot"
        self.bodyText = c.bb("2R-notick. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'R-notick'], 'nil'))
            caster.drawCard()

## 2G-notick. +1 Card.
class GreenTrot(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.85, siftDist = 1.5, likelihood = 0.5)
        self.name = "Green Trot"
        self.bodyText = c.bb("2G-notick. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'G-notick'], 'nil'))
            caster.drawCard()

## 2B-notick. +1 Card.
class BlueTrot(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.85, siftDist = 1.5, likelihood = 0.5)
        self.name = "Blue Trot"
        self.bodyText = c.bb("2B-notick. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'B-notick'], 'nil'))
            caster.drawCard()

## 2L. 
class scaredSlash(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2.5, siftDist = 1, likelihood = 0.5)
        self.name = "Scared Slash"
        self.bodyText = c.bb("2L.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([2, 'L'], 'nil'))

## +1 Action. 
class unrehearsed(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = (targetDamage * TAX_PLUS_ONE_ACTION),
            siftDist = 0.5,
            likelihood = 0.15)
        self.name = "Unrehearsed"
        self.bodyText = c.bb("+1 Action.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.actions = caster.actions + 1

## +1 Action.
##  To the next positioned living Enemy: +1 Card.
class talkingStick(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = (targetDamage * TAX_PLUS_ONE_ACTION),
            siftDist = 1.5,
            likelihood = 3)
        self.name = "Talking Stick"
        self.bodyText = c.bb("+1 Action. To the next positioned living Enemy: +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            index = h.getNextLivingEnemyIndex(enemies, caster.index)
            if index != -1:
                enemies[index].drawCard()
            else:
                h.splash("FAIL_FIND_ENEMY")

## 1R. Next Turn, 1R.
class redGash(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1 + (1) ** TAX_NEXT_TURN,
            siftDist = 0.5,
            likelihood = 0.5)
        self.name = "Red Gash"
        self.bodyText = c.bb("1R. //Next Turn, 1R.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            dino.damage(caster, dino, enemies, h.acons([1, 'R'], 'nil'))
        
    def atTriggerTurnStart(self, caster, dino, enemies):
        h.splash("Resolution of: Turn Start %Red Gash.%", printInsteadOfInput = True)
        h.splash("Inflicting:  1R.", printInsteadOfInput = True)
        dino.damage(caster, dino, enemies, h.acons([1, 'R'], 'nil'))

## 1G. Next Turn, 1G.
class greenGash(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1 + (1) ** TAX_NEXT_TURN,
            siftDist = 0.5,
            likelihood = 0.5)
        self.name = "Green Gash"
        self.bodyText = c.bb("1G. //Next Turn, 1G.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            dino.damage(caster, dino, enemies, h.acons([1, 'G'], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        h.splash("Resolution of: Turn Start %Green Gash.%", printInsteadOfInput = True)
        h.splash("Inflicting:  1G.", printInsteadOfInput = True)
        dino.damage(caster, dino, enemies, h.acons([1, 'G'], 'nil'))

## 1B. Next Turn, 1B.
class blueGash(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1 + (1) ** TAX_NEXT_TURN,
            siftDist = 0.5,
            likelihood = 0.5)
        self.name = "Blue Gash"
        self.bodyText = c.bb("1B. //Next Turn, 1B.")
        self.bodyText.push("{}", "{ 1H }")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            dino.damage(caster, dino, enemies, h.acons([1, 'B'], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        h.splash("Resolution of: Turn Start %Blue Gash.%", printInsteadOfInput = True)
        h.splash("Inflicting:  1B.", printInsteadOfInput = True)
        dino.damage(caster, dino, enemies, h.acons([1, 'B'], 'nil'))

## +1 Action. + Cantrip.
'''
class lastStand(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2 - 0.5, 
'''

## Dinosaur may Discard a Card. If Dinosaur did not, 2R.
class redGrowl(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2 - 0.5, siftDist = 0.65, likelihood = 0.5)
        self.name = "Red Growl"
        self.bodyText = c.bb("Dinosaur may Discard a Card. If Dinosaur did not, 2R.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            if dino.hand.length() > 0:
                index = 1
                preamble = []
                preamble.append("These are the Cards in Hand:")
                for card in dino.hand.getArray():
                    preamble.append(str(index) + ": ^" + card.name + "^.")
                    index += 1
                pick = h.pickValue("Optionally Pick a Card from Hand to Discard",
                                    range(1, index),
                                    preamble = preamble,
                                    passedInVisuals = passedInVisuals,
                                    canPass = True) - 1
                if pick != -2:
                    dino.discardCard(dino.hand, pick, dino, enemies, passedInVisuals)
                else:
                    h.splash("Inflicting:  2R.")
                    dino.damage(caster, dino, enemies, h.acons([2, 'R'], 'nil'))
            else:
                h.splash('FAIL_PICK_CARD')
                h.splash("Inflicting:  2R.")
                dino.damage(caster, dino, enemies, h.acons([2, 'R'], 'nil'))

## Dinosaur may Discard a Card. If Dinosaur did not, 2G.
class greenGrowl(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2 - 0.5, siftDist = 0.65, likelihood = 0.5)
        self.name = "Green Growl"
        self.bodyText = c.bb("Dinosaur may Discard a Card. If Dinosaur did not, 2G.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            if dino.hand.length() > 0:
                index = 1
                preamble = []
                preamble.append("These are the Cards in Hand:")
                for card in dino.hand.getArray():
                    preamble.append(str(index) + ": ^" + card.name + "^.")
                    index += 1
                pick = h.pickValue("Optionally Pick a Card from Hand to Discard",
                                    range(1, index),
                                    preamble = preamble,
                                    passedInVisuals = passedInVisuals,
                                    canPass = True) - 1
                if pick != -2:
                    dino.discardCard(dino.hand, pick, dino, enemies, passedInVisuals)
                else:
                    h.splash("Inflicting:  2G.")
                    dino.damage(caster, dino, enemies, h.acons([2, 'G'], 'nil'))
            else:
                h.splash('FAIL_PICK_CARD')
                h.splash("Inflicting:  2G.")
                dino.damage(caster, dino, enemies, h.acons([2, 'G'], 'nil'))

## Dinosaur may Discard a Card. If Dinosaur did not, 2B.
class blueGrowl(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2 - 0.5, siftDist = 0.65, likelihood = 0.5)
        self.name = "Blue Growl"
        self.bodyText = c.bb("Dinosaur may Discard a Card. If Dinosaur did not, 2B.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            if dino.hand.length() > 0:
                index = 1
                preamble = []
                preamble.append("These are the Cards in Hand:")
                for card in dino.hand.getArray():
                    preamble.append(str(index) + ": ^" + card.name + "^.")
                    index += 1
                pick = h.pickValue("Optionally Pick a Card from Hand to Discard",
                                    range(1, index),
                                    preamble = preamble,
                                    passedInVisuals = passedInVisuals,
                                    canPass = True) - 1
                if pick != -2:
                    dino.discardCard(dino.hand, pick, dino, enemies, passedInVisuals)
                else:
                    h.splash("Inflicting:  2B.")
                    dino.damage(caster, dino, enemies, h.acons([2, 'B'], 'nil'))
            else:
                h.splash('FAIL_PICK_CARD')
                h.splash("Inflicting:  2B.")
                dino.damage(caster, dino, enemies, h.acons([2, 'B'], 'nil'))

## Next Turn, 2R-notick.
class redLeapingAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1.67 * TAX_NEXT_TURN,
            siftDist = 0.75,
            likelihood = 0.5)
        self.name = "Red Leaping Attack"
        self.bodyText = c.bb("Next Turn, 2R-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            h.splash("During Turn Start: 2R-notick.")
            dino.damage(caster, dino, enemies, h.acons([2, 'R-notick'], 'nil'))

## Next Turn, 2G-notick.
class greenLeapingAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1.67 * TAX_NEXT_TURN,
            siftDist = 0.75,
            likelihood = 0.5)
        self.name = "Green Leaping Attack"
        self.bodyText = c.bb("Next Turn, 2G-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            h.splash("During Turn Start: 2G-notick.")
            dino.damage(caster, dino, enemies, h.acons([2, 'G-notick'], 'nil'))

## Next Turn, 2B-notick.
class blueLeapingAttack(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1.67 * TAX_NEXT_TURN,
            siftDist = 0.75,
            likelihood = 0.5)
        self.name = "Blue Leaping Attack"
        self.bodyText = c.bb("Next Turn, 2B-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            h.splash("During Turn Start: 2B-notick.")
            dino.damage(caster, dino, enemies, h.acons([2, 'B-notick'], 'nil'))

## +1 Action. Next Turn, +3 Cards.
class musterCourage(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = (targetDamage * TAX_PLUS_ONE_ACTION),
            siftDist = 1.75,
            likelihood = 3)
        self.name = "Muster Courage"
        self.bodyText = c.bb("+1 Action. //Next Turn: +3 Cards.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)
            caster.plusActions(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            h.splash("During Turn Start: +3 Cards.")
            for i in range(3):
                caster.drawCard()

## 1R. +1 Card.
class redCanter(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1.15,
            siftDist = 1.25,
            likelihood = 1)
        self.name = "Red Canter"
        self.bodyText = c.bb("1R. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'R'], 'nil'))
            caster.drawCard()

## 1G. +1 Card.
class greenCanter(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1.15,
            siftDist = 1.25,
            likelihood = 1)
        self.name = "Green Canter"
        self.bodyText = c.bb("1G. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'G'], 'nil'))
            caster.drawCard()

## 1B. +1 Card.
class blueCanter(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1.15,
            siftDist = 1.25,
            likelihood = 1)
        self.name = "Blue Canter"
        self.bodyText = c.bb("1B. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, h.acons([1, 'B'], 'nil'))
            caster.drawCard()

## Rocky Vase
class rockyVase(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(
            damageDist = 1,
            siftDist = 1.5,
            likelihood = 2.5)
        self.name = "Rocky Vase"
        self.bodyText = c.bb("+ Cantrip. Discard an Arbitrary Card. //2x, Draw a Card from Discard.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.drawCard()
            cf.arbitrarilyDiscardCardFrom_Location(caster.hand).func(self, caster, dino, enemies, passedInVisuals)
            for i in range(2):
                caster.drawCard(caster.discard, shuffleLocation = 'NONE')

## +1 Action. Heal 1L.
class craveFishMantra(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 6)
        self.name = "Crave Fish Mantra"
        self.bodyText = c.bb("+1 Action. Heal 1L. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.heal(caster, dino, enemies, h.acons([1, 'L'], 'nil'))
            caster.drawCard()

class fishFrenzy(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 6)
        self.name = "Fish Frenzy"
        self.bodyText = c.bb("+1 Action. To every Entity: Gain a ^Fish^ onto Draw.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            dino.gainCard(gcbt.getCardByName("Fish"), dino.draw)
            for enemy in enemies:
                enemy.gainCard(gcbt.getCardByName("Fish"), enemy.draw)

## + Cantrip. Top-Text Upgrade the Top Card of Draw with: //> +1 Action.
class prepareToFly(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 3)
        self.name = "Prepare To Fly"
        self.bodyText = c.bb("+ Cantrip. Top-Text Upgrade the Top Card of Draw with: //> +1 Action.")
        self.bodyText.heavinessText("{ HH }")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            caster.plusActions(1)
            caster.drawCard()
            if caster.draw.length() > 0:
                cardToEnshell = caster.draw.at(0)

                cardToEnshell.name = "Flying " + cardToEnshell.name
                cardToEnshell.publishShell(aboveThrowTextWrapper = cf.shellTextWrapper("+1 Action.", cf.plusXActions(1)))
                if isinstance(cardToEnshell, EnemyCard):
                    cardToEnshell.likelihood += 3
            else:
                h.splash("FAIL_FIND_CARD")

## +1 Action. Redistribute the HP in this current Band Arbitrarily.
class goingNuts(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 3)
        self.name = "Going Nuts"
        self.bodyText = c.bb("+1 Action. Redistribute the HP in this current Band Arbitrarily.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            if (caster.hp.getBands() == 0):
                h.splash('FAIL_NO_BANDS')
                return

            firstBand = caster.hp.toArray()[0]
            summedHp = sum(firstBand)

            newHp = [0, 0, 0]
            while (summedHp > 0):
                newHp[random.randint(0, 2)] += 1
                summedHp -= 1

            caster.hp.replaceBand(0, newHp)

## Summon a Shrew; it gets -1 Action. 
class soapboxStump(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 3)
        self.name = "Soapbox Stump"
        self.bodyText = c.bb("Summon a 'Shrew'; it gets -1 Action.")
        self.bodyText.heavinessText("{ HH }")
        self.publishInitialization(muck = True)
        self.table = ["Enemy"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.foreverLinger = True
            summonedEnemy = e.Shrew()
            summonedEnemy.roundStart()
            summonedEnemy.minusActions(1)
            enemies.append(summonedEnemy)

## Next turn, per non-Carcass Enemy: 1Random.
class demandingInheritance(EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 1)
        self.name = "Demanding Inheritance"
        self.bodyText = c.bb("Next Turn, per Living Enemy: 1Random.")
        self.bodyText.heavinessText("{ 1H }")
        self.table = ["Enemy"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            card.monotonicLingering(1)

    def atTriggerTurnStart(self, caster, dino, enemies):
        if self.turnsLingering == 1:
            count = 0
            for enemy in enemies:
                if enemy.dead == False:
                    count += 1
            if count > 0:
                h.splash("Resolving: Turn Start 'Demanding Inheritance.'", printInsteadOfInput = True)
                h.splash(str(count) + " times over: 1Random.")
                for i in range(count):
                    dino.damage(caster, dino, enemies, h.acons([1, 'Random'], 'nil'))

