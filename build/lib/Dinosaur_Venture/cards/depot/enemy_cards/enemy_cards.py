import random

from Dinosaur_Venture import channel_linked_lists as cll
from Dinosaur_Venture import helper as h
from Dinosaur_Venture.cards.depot.dino_cards.fundamental_cards import fish
from Dinosaur_Venture.cards.depot.enemy_cards import general_enemy_cards as gec
from Dinosaur_Venture.cards.mechanics import card as c
from Dinosaur_Venture.cards.mechanics import card_functions as cf
from Dinosaur_Venture.entities import entity as e

## There is an Dinosaur_Venture.entities.enemieses import below because a card summons Shrews.
## This should be safe but I am leaving this comment here for readability.

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
class nothing(gec.EnemyCard):
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
class redAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1, siftDist = 0.5, likelihood = 0.5)
        self.name = "Red Nibble"
        self.bodyText = c.bb("1R.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.R()], 'nil'))

## 1G.
class greenAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1, siftDist = 0.5, likelihood = 0.5)
        self.name = "Green Nibble"
        self.bodyText = c.bb("1G.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.G()], 'nil'))

## 1B.
class blueAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1, siftDist = 0.5, likelihood = 0.5)
        self.name = "Blue Nibble"
        self.bodyText = c.bb("1B.")   
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.B()], 'nil'))

## 1Random.
class randomAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Frenzied Nibble"
        self.bodyText = c.bb("1Random.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.Random()], 'nil'))

## 2R.
class doubleRedAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2, siftDist = 0.5, likelihood = 0.5)
        self.name = "Red Bite"
        self.bodyText = c.bb("2R.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.R()], 'nil'))

## 2G.
class doubleGreenAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2, siftDist = 0.5, likelihood = 0.5)
        self.name = "Green Bite"
        self.bodyText = c.bb("2G.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.G()], 'nil'))

## 2B.
class doubleBlueAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2, siftDist = 0.5, likelihood = 0.5)
        self.name = "Blue Bite"
        self.bodyText = c.bb("2B.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.B()], 'nil'))

## 2Random.
class doubleRandomAttack(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Frenzied Bite"
        self.bodyText = c.bb("2Random.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Random()], 'nil'))

## 1M. 
class smallMaw(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Small Maw"
        self.bodyText = c.bb("1M.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.M()], 'nil'))

## 2M. 
class maw(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2.25, siftDist = 0.5, likelihood = 0.5)
        self.name = "Maw"
        self.bodyText = c.bb("2M.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.M()], 'nil'))

## Next turn, +1 Action. 
class prepare(gec.EnemyCard):
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
class redNip(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.67, siftDist = 1, likelihood = 0.5)
        self.name = "Red Nip"
        self.bodyText = c.bb("1R-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.Rnotick()], 'nil'))

## 1G-notick. 
class greenNip(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.67, siftDist = 1, likelihood = 0.5)
        self.name = "Green Nip"
        self.bodyText = c.bb("1G-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.Gnotick()], 'nil'))

## 1B-notick. 
class blueNip(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.67, siftDist = 1, likelihood = 0.5)
        self.name = "Blue Nip"
        self.bodyText = c.bb("1B-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.Bnotick()], 'nil'))

## 2R-notick. 
class redPeck(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.67, siftDist = 1, likelihood = 0.5)
        self.name = "Red Peck"
        self.bodyText = c.bb("2R-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Rnotick()], 'nil'))

## 2G-notick. 
class greenPeck(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.67, siftDist = 1, likelihood = 0.5)
        self.name = "Green Peck"
        self.bodyText = c.bb("2G-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Gnotick()], 'nil'))

## 2B-notick. 
class bluePeck(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.67, siftDist = 1, likelihood = 0.5)
        self.name = "Blue Peck"
        self.bodyText = c.bb("2B-notick.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Bnotick()], 'nil'))

## 2R-notick. +1 Card.
class RedTrot(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.85, siftDist = 1.5, likelihood = 0.5)
        self.name = "Red Trot"
        self.bodyText = c.bb("2R-notick. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Rnotick()], 'nil'))
            caster.drawCard()

## 2G-notick. +1 Card.
class GreenTrot(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.85, siftDist = 1.5, likelihood = 0.5)
        self.name = "Green Trot"
        self.bodyText = c.bb("2G-notick. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Gnotick()], 'nil'))
            caster.drawCard()

## 2B-notick. +1 Card.
class BlueTrot(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 1.85, siftDist = 1.5, likelihood = 0.5)
        self.name = "Blue Trot"
        self.bodyText = c.bb("2B-notick. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Bnotick()], 'nil'))
            caster.drawCard()

## 2L. 
class scaredSlash(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2.5, siftDist = 1, likelihood = 0.5)
        self.name = "Scared Slash"
        self.bodyText = c.bb("2L.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.L()], 'nil'))

## +1 Action. 
class unrehearsed(gec.EnemyCard):
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
class talkingStick(gec.EnemyCard):
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
class redGash(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.R()], 'nil'))
        
    def atTriggerTurnStart(self, caster, dino, enemies):
        h.splash("Resolution of: Turn Start %Red Gash.%", printInsteadOfInput = True)
        h.splash("Inflicting:  1R.", printInsteadOfInput = True)
        dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.R()], 'nil'))

## 1G. Next Turn, 1G.
class greenGash(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.G()], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        h.splash("Resolution of: Turn Start %Green Gash.%", printInsteadOfInput = True)
        h.splash("Inflicting:  1G.", printInsteadOfInput = True)
        dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.G()], 'nil'))

## 1B. Next Turn, 1B.
class blueGash(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.B()], 'nil'))

    def atTriggerTurnStart(self, caster, dino, enemies):
        h.splash("Resolution of: Turn Start %Blue Gash.%", printInsteadOfInput = True)
        h.splash("Inflicting:  1B.", printInsteadOfInput = True)
        dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.B()], 'nil'))

## +1 Action. + Cantrip.
'''
class lastStand(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 2 - 0.5, 
'''

## Dinosaur may Discard a Card. If Dinosaur did not, 2R.
class redGrowl(gec.EnemyCard):
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
                    dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.R()], 'nil'))
            else:
                h.splash('FAIL_PICK_CARD')
                h.splash("Inflicting:  2R.")
                dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.R()], 'nil'))

## Dinosaur may Discard a Card. If Dinosaur did not, 2G.
class greenGrowl(gec.EnemyCard):
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
                    dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.G()], 'nil'))
            else:
                h.splash('FAIL_PICK_CARD')
                h.splash("Inflicting:  2G.")
                dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.G()], 'nil'))

## Dinosaur may Discard a Card. If Dinosaur did not, 2B.
class blueGrowl(gec.EnemyCard):
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
                    dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.B()], 'nil'))
            else:
                h.splash('FAIL_PICK_CARD')
                h.splash("Inflicting:  2B.")
                dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.B()], 'nil'))

## Next Turn, 2R-notick.
class redLeapingAttack(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Rnotick()], 'nil'))

## Next Turn, 2G-notick.
class greenLeapingAttack(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Gnotick()], 'nil'))

## Next Turn, 2B-notick.
class blueLeapingAttack(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([2, cll.Bnotick()], 'nil'))

## +1 Action. Next Turn, +3 Cards.
class musterCourage(gec.EnemyCard):
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
class redCanter(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.R()], 'nil'))
            caster.drawCard()

## 1G. +1 Card.
class greenCanter(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.G()], 'nil'))
            caster.drawCard()

## 1B. +1 Card.
class blueCanter(gec.EnemyCard):
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
            dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.B()], 'nil'))
            caster.drawCard()

## Rocky Vase
class rockyVase(gec.EnemyCard):
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
                caster.drawCard(caster.discard, shuffleLocation = e.Entity.NO_CARD_LOCATION)

## +1 Action. Heal 1L.
class craveFishMantra(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 6)
        self.name = "Crave Fish Mantra"
        self.bodyText = c.bb("+1 Action. Heal 1L. +1 Card.")
        self.table = ["Enemy", "Enemy Card Pool"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            caster.heal(caster, dino, enemies, cll.Attackcons([1, cll.L()], 'nil'))
            caster.drawCard()

## + Cantrip. Top-Text Upgrade the Top Card of Draw with: //> +1 Action.
class prepareToFly(gec.EnemyCard):
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
                if isinstance(cardToEnshell, gec.EnemyCard):
                    cardToEnshell.likelihood += 3
            else:
                h.splash("FAIL_FIND_CARD")

## +1 Action. Redistribute the HP in this current Band Arbitrarily.
class goingNuts(gec.EnemyCard):
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

# +1 Action. To every Entity: Gain a ^Fish^ onto Draw.
class fishFrenzy(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 6)
        self.name = "Fish Frenzy"
        self.bodyText = c.bb("+1 Action. To every Entity: Gain a ^Fish^ onto Draw.")
        self.table = ["Enemy"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            caster.plusActions(1)
            dino.gainCard(fish(), dino.draw)
            for enemy in enemies:
                enemy.gainCard(fish(), enemy.draw)

## Summon a Shrew; it gets -1 Action. 
class soapboxStump(gec.EnemyCard):
    def __init__(self, targetDamage = 0, targetSift = 0):
        super().__init__(damageDist = 0.5, siftDist = 0.5, likelihood = 3)
        self.name = "Soapbox Stump"
        self.bodyText = c.bb("Summon a 'Shrew'; it gets -1 Action.")
        self.bodyText.heavinessText("{ HH }")
        self.publish_initialization_muck()
        self.table = ["Enemy"]
        self.bundle(throwCardFunction = self.duringPlay())

    class duringPlay(cf.cardFunctions):
        def func(self, card, caster, dino, enemies, passedInVisuals):
            from Dinosaur_Venture.entities.enemieses import Shrew

            card.foreverLinger = True
            summonedEnemy = Shrew()
            summonedEnemy.roundStart()
            summonedEnemy.minusActions(1)
            enemies.append(summonedEnemy)

## Next turn, per non-Carcass Enemy: 1Random.
class demandingInheritance(gec.EnemyCard):
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
                    dino.damage(caster, dino, enemies, cll.Attackcons([1, cll.Random()], 'nil'))

