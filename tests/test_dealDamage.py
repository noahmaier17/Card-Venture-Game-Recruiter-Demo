import pytest, pytest_timeout, random, copy
from Dinosaur_Venture import cardFunctions as cf, helper as h, mainVisuals as vis, gameplayScriptedInput as scriptInput, channel_linked_lists as cll
from Dinosaur_Venture.Dino_Cards_Depot import GeneralDinoCards as generalDinoCards
from Test_Utils.gameSetups import setup_getDinoEnemiesClearing

'''
    Tests for correct functionality of dealing damage.
'''

## Runs the tests.
## inputsToExpected is looking for something in the form:
## (card object, damage dealt, enemy, expected fatal damage, expected broke a band, expected remaining enemy health)
## OR:
## (card object, damage dealt, enemy, expected fatal damage, expected broke a band, (set of expected remaining enemy health tuple,))
def runTestDamageInputsToExpected(dinoes, enemieses, clearingses, inputsToExpected):
    for i, uncopiedInputToExpected in enumerate(inputsToExpected):
        ## Because some damage types are not always deterministic, if we have a set of expected
        ## remaining enemy healths, we run every test 16 times so probalistically most possible
        ## outcomes are tested.
        if isinstance(uncopiedInputToExpected[4], tuple):
            repeats = 16
        else:
            repeats = 1
        for repeat in range(repeats):
            ## Copies the inputToExpected
            inputToExpected = copy.deepcopy(uncopiedInputToExpected)

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

            ## If we have a list of expectedEnemyHealths, any of them work as a match
            allExpectedEnemyHealths = []
            if isinstance(inputToExpected[4], tuple):
                allExpectedEnemyHealths = inputToExpected[4]
            else:
                allExpectedEnemyHealths.append(inputToExpected[4])

            ## Picks a random enemies index to 
            ## Sets the starting enemy health
            enemy.setHP(startingEnemyHealth)

            ## Deals the damage
            damageData = cf.dealDamage().func(card, dino, dino, enemies, vis.prefabEmpty(), damageArray,
                                            scriptedInput_cardFunctions_dealDamage=scriptInput.script_cardFunctions_dealDamage([str(enemyIndex + 1)]))
            
            ## Do our expected values match?
            assert expectedFatalDamage == damageData.fatalDamage, str(i) + " did not have matching fatal damage values."
            assert expectedBrokeABand == damageData.brokeABand, str(i) + " did not have matching broke a band values."
            success = False
            for expectedEnemyHealths in allExpectedEnemyHealths:
                if expectedEnemyHealths.equals(enemy.hp):
                    success = True
            assert success, str(i) + " did not have matching health values."

            ## For regression, are our HP values healthcons?
            assert isinstance(enemy.hp, cll.Healthcons), str(i) + " failed."

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
            (cll.Attackcons([1, 'R'], 'nil'), cll.Healthcons(9, 9, 9, 'nil'), False, False, cll.Healthcons(8, 9, 9, 'nil')),
            (cll.Attackcons([1, 'G'], 'nil'), cll.Healthcons(9, 9, 9, 'nil'), False, False, cll.Healthcons(9, 8, 9, 'nil')),
            (cll.Attackcons([1, 'B'], 'nil'), cll.Healthcons(9, 9, 9, 'nil'), False, False, cll.Healthcons(9, 9, 8, 'nil')),

            ## Tests damaging very weak enemy with 9 points of damage
            (cll.Attackcons([9, 'R'], 'nil'), cll.Healthcons(1, 1, 1, 'nil'), False, False, cll.Healthcons(0, 1, 1, 'nil')),
            (cll.Attackcons([9, 'G'], 'nil'), cll.Healthcons(1, 1, 1, 'nil'), False, False, cll.Healthcons(1, 0, 1, 'nil')),
            (cll.Attackcons([9, 'B'], 'nil'), cll.Healthcons(1, 1, 1, 'nil'), False, False, cll.Healthcons(1, 1, 0, 'nil')),

            ## Checks for rollover damage (of which is and is not fatal)
            (cll.Attackcons([5, 'R'], 'nil'), cll.Healthcons(0, 1, 1, 'nil'), False, False, cll.Healthcons(0, 0, 1, 'nil')),
            (cll.Attackcons([5, 'G'], 'nil'), cll.Healthcons(1, 0, 1, 'nil'), False, False, cll.Healthcons(1, 0, 0, 'nil')),
            (cll.Attackcons([5, 'B'], 'nil'), cll.Healthcons(1, 1, 0, 'nil'), False, False, cll.Healthcons(0, 1, 0, 'nil')),

            (cll.Attackcons([5, 'R'], 'nil'), cll.Healthcons(0, 0, 1, 'nil'), True, True, cll.DeadHealthcons()),
            (cll.Attackcons([5, 'G'], 'nil'), cll.Healthcons(1, 0, 0, 'nil'), True, True, cll.DeadHealthcons()),
            (cll.Attackcons([5, 'B'], 'nil'), cll.Healthcons(0, 1, 0, 'nil'), True, True, cll.DeadHealthcons()),

            ## Checks for fatal damage
            (cll.Attackcons([1, 'R'], 'nil'), cll.Healthcons(1, 0, 0, 'nil'), True, True, cll.DeadHealthcons()),
            (cll.Attackcons([1, 'G'], 'nil'), cll.Healthcons(0, 1, 0, 'nil'), True, True, cll.DeadHealthcons()),
            (cll.Attackcons([1, 'B'], 'nil'), cll.Healthcons(0, 0, 1, 'nil'), True, True, cll.DeadHealthcons()),
        ]

        runTestDamageInputsToExpected(dinoes, enemieses, clearingses, inputsToExpected)

    '''
        Tests:
        1. Do R, G, and B work as expected against enemies with 2-3 bands?

        Tests a random instance of the 'setup_getDinoEnemiesClearing' instead of enumerating them in their entirety.
    '''
    def test_RGBdamageTypes_bandedEnemies(self, setup_getDinoEnemiesClearing):
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing

        ## For the purpose of having fewer hard-coded values, we will append to every inputsToExpected sets of bands

        ## Maps inputs (damage dealt, enemy HP) to expected behavior (fatal damage, broke a band, remaining enemy health)
        rootInputsToExpected = [
            ## Tests damaging very healthy enemy with 1 point of damage
            (cll.Attackcons([1, 'R'], 'nil'), cll.Healthcons(9, 9, 9, 'nil'), False, False, cll.Healthcons(8, 9, 9, 'nil')),
            (cll.Attackcons([1, 'G'], 'nil'), cll.Healthcons(9, 9, 9, 'nil'), False, False, cll.Healthcons(9, 8, 9, 'nil')),
            (cll.Attackcons([1, 'B'], 'nil'), cll.Healthcons(9, 9, 9, 'nil'), False, False, cll.Healthcons(9, 9, 8, 'nil')),

            ## Tests damaging very weak enemy with 9 points of damage
            (cll.Attackcons([9, 'R'], 'nil'), cll.Healthcons(1, 1, 1, 'nil'), False, False, cll.Healthcons(0, 1, 1, 'nil')),
            (cll.Attackcons([9, 'G'], 'nil'), cll.Healthcons(1, 1, 1, 'nil'), False, False, cll.Healthcons(1, 0, 1, 'nil')),
            (cll.Attackcons([9, 'B'], 'nil'), cll.Healthcons(1, 1, 1, 'nil'), False, False, cll.Healthcons(1, 1, 0, 'nil')),

            ## Checks for rollover damage (of which is breaks and does not break bands)
            (cll.Attackcons([5, 'R'], 'nil'), cll.Healthcons(0, 1, 1, 'nil'), False, False, cll.Healthcons(0, 0, 1, 'nil')),
            (cll.Attackcons([5, 'G'], 'nil'), cll.Healthcons(1, 0, 1, 'nil'), False, False, cll.Healthcons(1, 0, 0, 'nil')),
            (cll.Attackcons([5, 'B'], 'nil'), cll.Healthcons(1, 1, 0, 'nil'), False, False, cll.Healthcons(0, 1, 0, 'nil')),

            (cll.Attackcons([5, 'R'], 'nil'), cll.Healthcons(0, 0, 1, 'nil'), False, True, None),
            (cll.Attackcons([5, 'G'], 'nil'), cll.Healthcons(1, 0, 0, 'nil'), False, True, None),
            (cll.Attackcons([5, 'B'], 'nil'), cll.Healthcons(0, 1, 0, 'nil'), False, True, None),

            ## Checks for band-breaking damage
            (cll.Attackcons([1, 'R'], 'nil'), cll.Healthcons(1, 0, 0, 'nil'), False, True, None),
            (cll.Attackcons([1, 'G'], 'nil'), cll.Healthcons(0, 1, 0, 'nil'), False, True, None),
            (cll.Attackcons([1, 'B'], 'nil'), cll.Healthcons(0, 0, 1, 'nil'), False, True, None),
        ]

        # For all of these inputted values, we will append the following bands:
        #   [1, 0, 0]  [0, 1, 0]  [0, 0, 1]  [1, 1, 1]  [9, 9, 9]
        arrayBands = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [9, 9, 9]
        ]

        inputsToExpected = []
        # Adds to our test pool 2-length bands
        for firstArray in arrayBands:
            tailHealthcons = cll.Healthcons(
                    firstArray[0], firstArray[1], firstArray[2],
                    'nil'
                )
                
            # Does the adding
            for root in rootInputsToExpected:
                newStartingHealth = copy.deepcopy(root[1])
                newStartingHealth.append(tailHealthcons)
                
                newExpectedHealth = copy.deepcopy(root[4])
                if newExpectedHealth == None:
                    newExpectedHealth = copy.deepcopy(tailHealthcons)
                else:
                    newExpectedHealth.append(tailHealthcons)

                inputsToExpected.append((
                    copy.deepcopy(root[0]),
                    newStartingHealth,
                    copy.deepcopy(root[2]),
                    copy.deepcopy(root[3]),
                    newExpectedHealth
                ))

        # Then, adds to our pool 3-length bands through the cartesian product of
        #   the 1-length bands.
        for firstArray in arrayBands:
            for secondArray in arrayBands:
                tailHealthcons = cll.Healthcons(
                    firstArray[0], firstArray[1], firstArray[2],
                    cll.Healthcons(
                        secondArray[0], secondArray[1], secondArray[2], 
                        'nil'
                        )
                    )

                # Does the adding
                for root in rootInputsToExpected:
                    newStartingHealth = copy.deepcopy(root[1])
                    newStartingHealth.append(tailHealthcons)
                    
                    newExpectedHealth = copy.deepcopy(root[4])
                    if newExpectedHealth == None:
                        newExpectedHealth = copy.deepcopy(tailHealthcons)
                    else:
                        newExpectedHealth.append(tailHealthcons)

                    inputsToExpected.append((
                        copy.deepcopy(root[0]),
                        newStartingHealth,
                        copy.deepcopy(root[2]),
                        copy.deepcopy(root[3]),
                        newExpectedHealth
                    ))

        runTestDamageInputsToExpected(dinoes, enemieses, clearingses, inputsToExpected)

    '''
        Test:
        1. Does M work as expected?

        Tests just with 1 band, since multiple bands should be thoroughly and accurately tested with the `test_RGBdamageTypes_bandedEnemies` test.

        Tests a random instance of the 'setup_getDinoEnemiesClearing' instead of enumerating them in their entirety.
    '''
    def test_M_noBandedEnemies(self, setup_getDinoEnemiesClearing):
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing

        ## For the purpose of having fewer hard-coded values, we will append to every inputsToExpected sets of bands

        ## Maps inputs (card object, damage dealt, enemy) to expected behavior (fatal damage, broke a band, (possible remaining enemy healths,))
        inputsToExpected = [
            ## Tests 1M damage against [9, 1, 0]
            (cll.Attackcons([1, 'M'], 'nil'), cll.Healthcons(9, 1, 0, 'nil'), False, False, (
                cll.Healthcons(8, 1, 0, 'nil'),
            )),
            (cll.Attackcons([1, 'M'], 'nil'), cll.Healthcons(0, 9, 1, 'nil'), False, False, (
                cll.Healthcons(0, 8, 1, 'nil'),
            )),            
            (cll.Attackcons([1, 'M'], 'nil'), cll.Healthcons(1, 0, 9, 'nil'), False, False, (
                cll.Healthcons(1, 0, 8, 'nil'),
            )),

            ## Tests fatal 2M damage
            (cll.Attackcons([2, 'M'], 'nil'), cll.Healthcons(2, 0, 0, 'nil'), True, True, (
                cll.DeadHealthcons(),
            )),
            (cll.Attackcons([2, 'M'], 'nil'), cll.Healthcons(0, 2, 0, 'nil'), True, True, (
                cll.DeadHealthcons(),
            )),            
            (cll.Attackcons([2, 'M'], 'nil'), cll.Healthcons(0, 0, 2, 'nil'), True, True, (
                cll.DeadHealthcons(),
            )),

            ## Tests accurate 9M tie resolutions
            (cll.Attackcons([9, 'M'], 'nil'), cll.Healthcons(5, 5, 0, 'nil'), False, False, (
                cll.Healthcons(0, 5, 0, 'nil'), cll.Healthcons(5, 0, 0, 'nil'),
            )),
            (cll.Attackcons([9, 'M'], 'nil'), cll.Healthcons(0, 5, 5, 'nil'), False, False, (
                cll.Healthcons(0, 5, 0, 'nil'), cll.Healthcons(0, 0, 5, 'nil'),
            )),            
            (cll.Attackcons([9, 'M'], 'nil'), cll.Healthcons(5, 0, 5, 'nil'), False, False, (
                cll.Healthcons(5, 0, 0, 'nil'), cll.Healthcons(0, 0, 5, 'nil'),
            )),
            (cll.Attackcons([9, 'M'], 'nil'), cll.Healthcons(5, 5, 5, 'nil'), False, False, (
                cll.Healthcons(5, 5, 0, 'nil'), cll.Healthcons(0, 5, 5, 'nil'), cll.Healthcons(5, 0, 5, 'nil'),
            )),

            ## Tests accurate 1M-1M tie resolutions
            (cll.Attackcons([1, 'M'], cll.Attackcons([1, 'M'], 'nil')), cll.Healthcons(5, 5, 0, 'nil'), False, False, (
                cll.Healthcons(4, 4, 0, 'nil'),
            )),
            (cll.Attackcons([1, 'M'], cll.Attackcons([1, 'M'], 'nil')), cll.Healthcons(0, 5, 5, 'nil'), False, False, (
                cll.Healthcons(0, 4, 4, 'nil'),
            )),            
            (cll.Attackcons([1, 'M'], cll.Attackcons([1, 'M'], 'nil')), cll.Healthcons(5, 0, 5, 'nil'), False, False, (
                cll.Healthcons(4, 0, 4, 'nil'),
            )),
        ]

        runTestDamageInputsToExpected(dinoes, enemieses, clearingses, inputsToExpected)

    '''
        Test:
        1. Does L work as expected?

        Tests just with 1 band, since multiple bands should be thoroughly and accurately tested with the `test_RGBdamageTypes_bandedEnemies` test.

        Tests a random instance of the 'setup_getDinoEnemiesClearing' instead of enumerating them in their entirety.
    '''
    def test_L_noBandedEnemies(self, setup_getDinoEnemiesClearing):
        dinoes, enemieses, clearingses = setup_getDinoEnemiesClearing

        ## For the purpose of having fewer hard-coded values, we will append to every inputsToExpected sets of bands

        ## Maps inputs (card object, damage dealt, enemy) to expected behavior (fatal damage, broke a band, (possible remaining enemy healths,))
        inputsToExpected = [
            ## Tests 1L damage against [9, 1, 0]
            (cll.Attackcons([1, 'L'], 'nil'), cll.Healthcons(9, 1, 0, 'nil'), False, False, (
                cll.Healthcons(9, 0, 0, 'nil'),
            )),
            (cll.Attackcons([1, 'L'], 'nil'), cll.Healthcons(0, 9, 1, 'nil'), False, False, (
                cll.Healthcons(0, 9, 0, 'nil'),
            )),            
            (cll.Attackcons([1, 'L'], 'nil'), cll.Healthcons(1, 0, 9, 'nil'), False, False, (
                cll.Healthcons(0, 0, 9, 'nil'),
            )),

            ## Tests fatal 2M damage
            (cll.Attackcons([2, 'L'], 'nil'), cll.Healthcons(2, 0, 0, 'nil'), True, True, (
                cll.DeadHealthcons(),
            )),
            (cll.Attackcons([2, 'L'], 'nil'), cll.Healthcons(0, 2, 0, 'nil'), True, True, (
                cll.DeadHealthcons(),
            )),            
            (cll.Attackcons([2, 'L'], 'nil'), cll.Healthcons(0, 0, 2, 'nil'), True, True, (
                cll.DeadHealthcons(),
            )),

            ## Tests accurate LM tie resolutions
            (cll.Attackcons([9, 'L'], 'nil'), cll.Healthcons(5, 5, 0, 'nil'), False, False, (
                cll.Healthcons(0, 5, 0, 'nil'), cll.Healthcons(5, 0, 0, 'nil'),
            )),
            (cll.Attackcons([9, 'L'], 'nil'), cll.Healthcons(0, 5, 5, 'nil'), False, False, (
                cll.Healthcons(0, 5, 0, 'nil'), cll.Healthcons(0, 0, 5, 'nil'),
            )),
            (cll.Attackcons([9, 'L'], 'nil'), cll.Healthcons(5, 0, 5, 'nil'), False, False, (
                cll.Healthcons(5, 0, 0, 'nil'), cll.Healthcons(0, 0, 5, 'nil'),
            )),
            (cll.Attackcons([9, 'L'], 'nil'), cll.Healthcons(5, 5, 5, 'nil'), False, False, (
                cll.Healthcons(5, 5, 0, 'nil'), cll.Healthcons(0, 5, 5, 'nil'), cll.Healthcons(5, 0, 5, 'nil'),
            )),

            ## Tests accurate 1L-1L NON-tie resolutions
            (cll.Attackcons([1, 'L'], cll.Attackcons([1, 'L'], 'nil')), cll.Healthcons(5, 5, 0, 'nil'), False, False, (
                cll.Healthcons(5, 3, 0, 'nil'), cll.Healthcons(3, 5, 0, 'nil')
            )),
            (cll.Attackcons([1, 'L'], cll.Attackcons([1, 'L'], 'nil')), cll.Healthcons(0, 5, 5, 'nil'), False, False, (
                cll.Healthcons(0, 3, 5, 'nil'), cll.Healthcons(0, 5, 3, 'nil')
            )),            
            (cll.Attackcons([1, 'L'], cll.Attackcons([1, 'L'], 'nil')), cll.Healthcons(5, 0, 5, 'nil'), False, False, (
                cll.Healthcons(3, 0, 5, 'nil'), cll.Healthcons(5, 0, 3, 'nil')
            )),
            (cll.Attackcons([1, 'L'], cll.Attackcons([1, 'L'], 'nil')), cll.Healthcons(5, 5, 5, 'nil'), False, False, (
                cll.Healthcons(3, 5, 5, 'nil'), cll.Healthcons(5, 3, 5, 'nil'), cll.Healthcons(5, 5, 3, 'nil')
            )),
        ]

        runTestDamageInputsToExpected(dinoes, enemieses, clearingses, inputsToExpected)