import Dinosaur_Venture.cards.mechanics.card as c


## Initiates all enemy cards
class EnemyCard(c.Card):
    def __init__(self, damageDist, siftDist, likelihood):
        super().__init__(likelihood, damageDist, siftDist)