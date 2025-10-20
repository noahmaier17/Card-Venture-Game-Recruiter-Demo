'''
## -- SHREW CARDS --
## +1 Action. Next turn, discard this and +3 Cards.
class musterCourage(EnemyCard):
    def __init__(self):
        super().__init__(damageDist = 0.5, siftDist = 1.5, likelihood = 1)
        self.name = "Muster Courage"
        self.bodyText = c.bb("+1 Action. //Next turn, discard this from play, and +3 Cards.")
        self.table = ["Enemy"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.actions = caster.actions + 1
        self.lingering = 1

    def atTriggerTurnStart(self, caster, dino, enemies):
        # input(h.colorize(" Discarding 'Muster Courage' from play, and +3 Cards."))
        cardIndex = h.locateCardIndex(caster.play, self)
        if cardIndex >= 0:
            caster.moveCard(caster.play, cardIndex, caster.discard)
        for i in range(3):
            caster.drawCard()

## -- ENSHRINED CAPYBARA CARDS --
## +1 Action. 1M. 0.75Chance 1M. 
class twoMetalTeeth(EnemyCard):
    def __init__(self):
        super().__init__(damageDist = 1.95, siftDist = 0.5, likelihood = 2)
        self.name = "Two Metal Teeth"
        self.bodyText = c.bb("+1 Action. 1M. //0.45Chance for 1M.")
        self.table = ["Enemy"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        dino.damage(caster, dino, enemies, cll.Attackcons([1, 'M'], 'nil'))
        if random.random() < 0.45:
            h.splash("Succeeded 0.45Chance, so 1M.")
            dino.damage(caster, dino, enemies, cll.Attackcons([1, 'M'], 'nil'))

## If caster has only 1 Band left: 1Random / 1Random. 
##  Otherwise, +1 Action. 
class frightened1(EnemyCard):
    def __init__(self):
        super().__init__(damageDist = 1.5, siftDist = 0.5, likelihood = 2)
        self.name = "Frightened"
        self.bodyText = c.bb("If caster has only 1 Band left: 1Random / 1Random. //Otherwise: +1 Action.")
        self.table = ["Enemy"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        if caster.getBands() == 1:
            h.splash("Caster had 1 Band, so: 1Random / 1Random.")
            dino.damage(caster, dino, enemies, cll.Attackcons([1, 'Random'], 
                    cll.Attackcons([1, 'Random'], 'nil')))
        else:
            h.splash("Caster does not have 1 Band, so: +1 Action.")
            caster.plusActions(1)
            
## Per turn taken + 1: 1L. 
class yellowPadResearch(EnemyCard):
    def __init__(self):
        super().__init__(damageDist = 1.5, siftDist = 0.5, likelihood = 1)
        self.name = "Yellow Pad Research"
        self.bodyText = c.bb("Per turn taken: 1L.")
        self.table = ["Enemy"]

    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        numberOfTurns = caster.turn
        h.splash(str(numberOfTurns) + " times over: 1L.")
        for i in range(numberOfTurns):
            dino.damage(caster, dino, enemies, cll.Attackcons([1, 'L'], 'nil'))

## +1 Action. 
##  To the next positioned living Enemy: +1 Card. 
class loosePapers(EnemyCard):
    def __init__(self):
        super().__init__(damageDist = 0.5, siftDist = 1, likelihood = 1)
        self.name = "Loose Papers"
        self.bodyText = c.bb("+1 Action. To the next positioned living Enemy: +1 Card.")
        self.table = ["Enemy"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        index = h.getNextLivingEnemyIndex(enemies, caster.index)
        if index != -1:
            enemies[index].drawCard()
        else:
            h.splash("FAIL_FIND_ENEMY")

## Summon a Shrew. 
class shearedCreature(EnemyCard):
    def __init__(self):
        super().__init__(damageDist = 0.5, siftDist = 1, likelihood = 0.8)
        self.name = "Sheared Creature"
        self.bodyText = c.bb("Summon a 'Shrew'.")
        self.table = ["Enemy"]
    
    def onPlay(self, caster, dino, enemies, passedInVisuals):
        super().onPlay(caster, dino, enemies, passedInVisuals)
        caster.plusActions(1)
        summonedEnemy =enemieses.Shrew()
        summonedEnemy.roundStart()
        enemies.append(summonedEnemy)
        for enemy in enemies:
            enemy.atTriggerEnemySummoned(summonedEnemy, dino, enemies)
'''