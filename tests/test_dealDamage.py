import pytest, pytest_timeout, random, copy
from Dinosaur_Venture import cardFunctions as cf, helper as h, mainVisuals as vis, gameplayScriptedInput as scriptInput
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as generalDinoCards
from Test_Utils.gameSetups import setup_getDinoEnemiesClearing

'''
    Tests for correct functionality of dealing damage.
'''

class TestSuite():
    '''
        Tests:
        1. Do R, G, and B work as expected against enemies with 1 band?

        Tests a random instance of the 'setup_getDinoEnemiesClearing' instead of enumerating them in their entirety.
    '''
    @pytest.mark.timeout(5)
    def test_RGBdamageTypes_noBandedEnemies(self, setup_getDinoEnemiesClearing):
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing

        ## Maps inputs (card object, damage dealt, enemy) to expected behavior (fatal damage, broke a band, remaining enemy health)
        inputsToExpected = [
            ## Tests damaging very healthy enemy with 1 point of damage
            (h.acons([1, 'R'], 'nil'), h.healthcons(9, 9, 9, 'nil'), False, False, h.healthcons(8, 9, 9, 'nil')),
            (h.acons([1, 'G'], 'nil'), h.healthcons(9, 9, 9, 'nil'), False, False, h.healthcons(9, 8, 9, 'nil')),
            (h.acons([1, 'B'], 'nil'), h.healthcons(9, 9, 9, 'nil'), False, False, h.healthcons(9, 9, 8, 'nil')),

            ## Tests damaging very weak enemy with 9 points of damage
            (h.acons([9, 'R'], 'nil'), h.healthcons(1, 1, 1, 'nil'), False, False, h.healthcons(0, 1, 1, 'nil')),
            (h.acons([9, 'G'], 'nil'), h.healthcons(1, 1, 1, 'nil'), False, False, h.healthcons(1, 0, 1, 'nil')),
            (h.acons([9, 'B'], 'nil'), h.healthcons(1, 1, 1, 'nil'), False, False, h.healthcons(1, 1, 0, 'nil')),

            ## Checks for rollover damage (of which is and is not fatal)
            (h.acons([5, 'R'], 'nil'), h.healthcons(0, 1, 1, 'nil'), False, False, h.healthcons(0, 0, 1, 'nil')),
            (h.acons([5, 'G'], 'nil'), h.healthcons(1, 0, 1, 'nil'), False, False, h.healthcons(1, 0, 0, 'nil')),
            (h.acons([5, 'B'], 'nil'), h.healthcons(1, 1, 0, 'nil'), False, False, h.healthcons(0, 1, 0, 'nil')),

            (h.acons([5, 'R'], 'nil'), h.healthcons(0, 0, 1, 'nil'), True, True, h.deadHealthcons()),
            (h.acons([5, 'G'], 'nil'), h.healthcons(1, 0, 0, 'nil'), True, True, h.deadHealthcons()),
            (h.acons([5, 'B'], 'nil'), h.healthcons(0, 1, 0, 'nil'), True, True, h.deadHealthcons()),

            ## Checks for fatal damage
            (h.acons([1, 'R'], 'nil'), h.healthcons(1, 0, 0, 'nil'), True, True, h.deadHealthcons()),
            (h.acons([1, 'G'], 'nil'), h.healthcons(0, 1, 0, 'nil'), True, True, h.deadHealthcons()),
            (h.acons([1, 'B'], 'nil'), h.healthcons(0, 0, 1, 'nil'), True, True, h.deadHealthcons()),
        ]

        ## Enumerates every test
        for inputToExpected in inputsToExpected:
            ## Gets an arbitrary dino, enemy, and clearing of all imported
            dino = copy.deepcopy(dinoes[random.randint(0, len(dinoes) - 1)])
            enemies = copy.deepcopy(enemieses[random.randint(0, len(enemieses) - 1)])
            enemyIndex = random.randint(0, len(enemies) - 1)
            enemy = enemies[enemyIndex]
            clearing = copy.deepcopy(clearingses[random.randint(0, len(clearingses) - 1)])

            ## Simply uses a basic dino card
            card = generalDinoCards.DinoCard()

            ## Maps all the inputToExpected values to variable names
            damageArray = inputToExpected[0]
            startingEnemyHealth = inputToExpected[1]
            expectedFatalDamage = inputToExpected[2]
            expectedBrokeABand = inputToExpected[3]
            expectedEnemyHealth = inputToExpected[4]

            ## Picks a random enemies index to 
            ## Sets the starting enemy health
            enemy.setHP(startingEnemyHealth)

            ## Deals the damage
            damageData = cf.dealDamage().func(card, dino, dino, enemies, vis.prefabEmpty(), damageArray,
                                              scriptedInput_cardFunctions_dealDamage=scriptInput.script_cardFunctions_dealDamage([str(enemyIndex + 1)]))
            
            ## Do our expected values match?
            assert expectedFatalDamage == damageData.fatalDamage
            assert expectedBrokeABand == damageData.brokeABand
            assert expectedEnemyHealth.equals(enemy.hp)

            ## For regression, are our HP values healthcons?
            assert isinstance(expectedEnemyHealth, h.healthcons)
            assert isinstance(enemy.hp, h.healthcons)

    '''
        Tests:
        1. Do R, G, and B work as expected against enemies with 2-3 bands?

        Tests a random instance of the 'setup_getDinoEnemiesClearing' instead of enumerating them in their entirety.
    '''

    def test_RGBdamageTypes_bandedEnemies(self, setup_getDinoEnemiesClearing):
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing

        ## For the purpose of having fewer hard-coded values, we will append to every inputsToExpected sets of bands

        ## Maps inputs (card object, damage dealt, enemy) to expected behavior (fatal damage, broke a band, remaining enemy health)
        rootInputsToExpected = [
            ## Tests damaging very healthy enemy with 1 point of damage
            (h.acons([1, 'R'], 'nil'), h.healthcons(9, 9, 9, 'nil'), False, False, h.healthcons(8, 9, 9, 'nil')),
            (h.acons([1, 'G'], 'nil'), h.healthcons(9, 9, 9, 'nil'), False, False, h.healthcons(9, 8, 9, 'nil')),
            (h.acons([1, 'B'], 'nil'), h.healthcons(9, 9, 9, 'nil'), False, False, h.healthcons(9, 9, 8, 'nil')),

            ## Tests damaging very weak enemy with 9 points of damage
            (h.acons([9, 'R'], 'nil'), h.healthcons(1, 1, 1, 'nil'), False, False, h.healthcons(0, 1, 1, 'nil')),
            (h.acons([9, 'G'], 'nil'), h.healthcons(1, 1, 1, 'nil'), False, False, h.healthcons(1, 0, 1, 'nil')),
            (h.acons([9, 'B'], 'nil'), h.healthcons(1, 1, 1, 'nil'), False, False, h.healthcons(1, 1, 0, 'nil')),

            ## Checks for rollover damage (of which is breaks and does not break bands)
            (h.acons([5, 'R'], 'nil'), h.healthcons(0, 1, 1, 'nil'), False, False, h.healthcons(0, 0, 1, 'nil')),
            (h.acons([5, 'G'], 'nil'), h.healthcons(1, 0, 1, 'nil'), False, False, h.healthcons(1, 0, 0, 'nil')),
            (h.acons([5, 'B'], 'nil'), h.healthcons(1, 1, 0, 'nil'), False, False, h.healthcons(0, 1, 0, 'nil')),

            (h.acons([5, 'R'], 'nil'), h.healthcons(0, 0, 1, 'nil'), False, True, None),
            (h.acons([5, 'G'], 'nil'), h.healthcons(1, 0, 0, 'nil'), False, True, None),
            (h.acons([5, 'B'], 'nil'), h.healthcons(0, 1, 0, 'nil'), False, True, None),

            ## Checks for band-breaking damage
            (h.acons([1, 'R'], 'nil'), h.healthcons(1, 0, 0, 'nil'), False, True, None),
            (h.acons([1, 'G'], 'nil'), h.healthcons(0, 1, 0, 'nil'), False, True, None),
            (h.acons([1, 'B'], 'nil'), h.healthcons(0, 0, 1, 'nil'), False, True, None),
        ]

        ## For all of these inputted values, we will append the following bands:
        ##  [1, 0, 0]  [0, 1, 0]  [0, 0, 1]  [1, 1, 1]  [9, 9, 9]
        ##  And, we will append 2 of these (for a sum-total of 3 bands)
        followingBandsOneInstance = [
            h.healthcons(1, 0, 0, 'nil'), 
            h.healthcons(0, 1, 0, 'nil'), 
            h.healthcons(0, 0, 1, 'nil'), 
            h.healthcons(1, 1, 1, 'nil'), 
            h.healthcons(9, 9, 9, 'nil'), 
        ]

        followingBandsTwoInstances = []
        for healthcon in followingBandsOneInstance:
            healthcon = copy.deepcopy(healthcon)
            for anotherHealthcon in followingBandsOneInstance:
                anotherHealthcon = copy.deepcopy(anotherHealthcon)
                newHealthcon = copy.deepcopy(healthcon)
                newHealthcon.append(anotherHealthcon)
                followingBandsTwoInstances.append(newHealthcon)

        inputsToExpected = []
        for followingBands in followingBandsOneInstance + followingBandsTwoInstances:
            followingBands = copy.deepcopy(followingBands)
            for instance in rootInputsToExpected:
                value0 = copy.deepcopy(instance[0])
                startingHealthcons = copy.deepcopy(instance[1])
                value2 = copy.deepcopy(instance[2])
                value3 = copy.deepcopy(instance[3])
                expectedHealthcons = copy.deepcopy(instance[4])

                startingHealthcons.append(followingBands)

                if expectedHealthcons == None:
                    inputsToExpected.append(
                        (value0, startingHealthcons, value2, value3, followingBands)
                    )
                else:
                    expectedHealthcons.append(followingBands)
                    inputsToExpected.append(
                        (value0, startingHealthcons, value2, value3, expectedHealthcons)
                    )

        ## Enumerates every test
        for inputToExpected in inputsToExpected:
            ## Gets an arbitrary dino, enemy, and clearing of all imported
            dino = copy.deepcopy(dinoes[random.randint(0, len(dinoes) - 1)])
            enemies = copy.deepcopy(enemieses[random.randint(0, len(enemieses) - 1)])
            enemyIndex = random.randint(0, len(enemies) - 1)
            enemy = enemies[enemyIndex]
            clearing = copy.deepcopy(clearingses[random.randint(0, len(clearingses) - 1)])

            ## Simply uses a basic dino card
            card = generalDinoCards.DinoCard()

            ## Maps all the inputToExpected values to variable names
            damageArray = inputToExpected[0]
            startingEnemyHealth = inputToExpected[1]
            expectedFatalDamage = inputToExpected[2]
            expectedBrokeABand = inputToExpected[3]
            expectedEnemyHealth = inputToExpected[4]

            ## Picks a random enemies index to 
            ## Sets the starting enemy health
            enemy.setHP(startingEnemyHealth)

            ## Deals the damage
            damageData = cf.dealDamage().func(card, dino, dino, enemies, vis.prefabEmpty(), damageArray,
                                              scriptedInput_cardFunctions_dealDamage=scriptInput.script_cardFunctions_dealDamage([str(enemyIndex + 1)]))
            
            ## Do our expected values match?
            assert expectedFatalDamage == damageData.fatalDamage
            assert expectedBrokeABand == damageData.brokeABand
            assert expectedEnemyHealth.equals(enemy.hp)

            ## For regression, are our HP values healthcons?
            assert isinstance(expectedEnemyHealth, h.healthcons)
            assert isinstance(enemy.hp, h.healthcons)

