# Deck-Building Card Game

A turn-based command-line game card game, in which the player (named dino) traverses across different clearings, fights the monsters they meet, and improves their deck based off the enemies they defeat. 

## File Structure

The following includes the most important and noteworthy files/folders in my project.

    Card-Venture-Game/
        .github/                        # GitHub Actions; automatically runs pytest on push/pull
        ...

    src/
        Dinosaur_Venture/
            devtools/                   # Development utilities
            dino_cards_depot/           # Contains all player cards
            entities/                   # Entities (including the player and enemies) logic

            cardFunctions.py            # Handles often-repeated card on-play logic
            cardModFunctions.py         # Allows for modification of that often-repeated on-play logic
            cardTokens.py               # Tokens placed on cards that modify them
            dinosaur_venture.py         # Runs the game
            gameplay_logging.py         # Logs events in the game for the purpose of debugging
            gameplayScriptedInput.py    # Simulates user input for the purpose of testing
            helper.py                   # Helper functions
            mainVisuals.py              # Handles the command-line UI
            react.py                    # Handles when cards can react to the current game state
            ...

    tests/
        test_utils/                     # Helper functions
        Files starting with "test_"     # Test cases

    web_app/
        app.py                          # Web Application for looking at card tables
        ...

    logs/                               # Location of debugging logs
    ...

## Feature Overview

The following is a list of the most interesting aspects of my code.  
- The `src/Dinosaur_Venture/dinosaur_venture/` file
    - This handles all the main logic for running the game. 
- Entities (`src/Dinosaur_Venture/entities/*`)
    - All the playable characters (found in `dinoes.py`) and enemy characters (found in `enemieses.py`) inherit `entity.py`, which contains a lot of the functionality for drawing cards, taking damage, the start of round, etc. 
- Dinosaur Cards (`src/Dinosaur_Venture/dino_cards_depot/*`)
    - The player cards (called Dinosaur cards since the player was originally a dinosaur) are all found in this file. Every card is unique, and some are pretty significantly complicated. 
    - ~150 implemented; ~20 in development.
- Enemy Cards (`src/Dinosaur_Venture/enemyCards.py`)
    - The list of enemy cards; all are also unique. 
    - ~40 implemented.
- devtools (`src/Dinosaur_Venture/devtools/*`)
    - `clearLogs.py` clears the log writing for this game. In `src/Dinosaur_Venture/gameplay_logging`, I created custom logging functionality so different moments throughout a game are saved in an external location. That way, if there is some sort of buggy functionality, I can trace these logs to understand what is incorrect. This devtool clears all of those logs. 
    - `simulateCards.py` lets a developer look up cards. It supports looking up cards based on their loot table (e.g. if they are found in the clearing named "New Bear Order"), and based on some sort of RegEx condition. 
- Test Cases (`tests/`)
    - I have been working to implement test cases for my game, which can be found within this folder.
- Simulate Cards Web Application (`web_app/`)
    - As a tool for looking at the list of all cards in the game, I have created a small locally-hosted web application using JavaScript and HTML.
    - The tool contains several checkboxes for selecting which table to include for looking at the code, and buttons for toggling certain sets of cards (like selecting all the playable characters' cards). 

## Current Main Focus

- Adding more test cases
    - I have been focused on testing if cards work in and of themselves (IE, if a card can successfully deal the damage it is meant to deal) and if they work in the broader scope of the game (IE, if a card can be successfully picked from hand and then played). I want to expand on this, adding more tests of card functionality and to test other aspects of my game. 
    - My game is pretty big, so there are several more aspects which could make effective use of test cases. 
- Better UI
    - Most of my focus is on the backend logic of my game, so the UI is currently done through command line in tandem with the `colorama` package for unique text coloring and styling. 
    - Almost all of the visual elements of this game are handled with `src/Dinosaur_Venture/mainVisuals.py`, with some helper calls found in in `src/Dinosaur_Venture/helper.py`. The UI aspect of my program is well factored (almost every print statement is found in either of those two aforementioned files), so I best prepped my code to support this change. 
- Refactoring / Improved Code Style
    - Some parts of my program were coded several years ago at this point, and were programmed at a time where the direction of the project was slightly different, so I am working to refactor elements of my program. Most recently, I split all of the player cards into files divided based on the different loot tables they belong to (see `src/Dinosaur_Venture/dino_cards_depot/`); originally, all of these cards were in the same `dinoCards.py` file.
    - Moreover, I did not fully understand the style guide of Python, and a lot of variable/file/class names and function/class/file comments are more like Java than like Python. I have been trying to improve some of these style problems in my code. 
    - Lastly, I also want to add more type hints across the entirety of my program. They are very helpful and increase my own productivity significantly in having them.  
- Adding more Cards, Clearings, Playable Characters, and Enemies
    - I am always working to add more content to my game! 