import unittest
from Dinosaur_Venture import entity as e, getCardsByTable as gcbt

class Test_TwigExclamation_onPlay(unittest.TestCase):

    def setUp(self):
        dino = e.Dinosaur() ## Empty Player Character
        dino.gainCard(gcbt.getCardByName("Twig!"), dino.deck)


    ## def tearDown(self): 

    def test_twigExclamation_expectedBehavior(self):
        pass
        ## self.assertTrue(True == (not False))

if __name__ == '__main__':
    unittest.main()