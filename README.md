# Deck-Building Card Game

A turn-based command-line game card game, in which the player (named dino) traverses across different clearings, fights the monsters they meet, and improves their deck based off the enemies they defeat. 

## File Structure

The following depicts and explains the project directory. The most important and noteworthy files/folders have been denoted by two exclamation points. 

    Card-Venture-Game/
        .github/                            # GitHub Actions; automatically runs pytest on push/pull
        ...

        scripts/
            push_to_recruiter_repo.ps1      # Script to merge private repo to public/recruiter-facing repo          !!
            clear_logs.py                   # Cleans all logs in logs/ folder
            ...

        src/
            Dinosaur_Venture/
                devtools/                   # Development utilities
                dino_cards_depot/           # Contains all player cards                                             !!
                enemy_cards_depot/          # Contains all enemy cards                                              !!
                entities/                   # Entities (including the player and enemies) logic                     !!

                card_functions.py           # Handles often-repeated card on-play logic
                card_mod_functions.py       # Allows for modification of that often-repeated on-play logic
                card_tokens.py              # Tokens placed on cards to modifer card behavior
                dinosaur_venture.py         # Runs the game                                                         !!
                gameplay_logging.py         # Logs events in the game for the purpose of debugging
                gameplay_scripted_input.py  # Simulates user input for the purpose of testing
                helper.py                   # Helper functions
                main_visuals.py             # Handles the command-line UI
                react.py                    # Handles when cards can react to the current game state
                ...

        tests/                                                                                                      !!
            test_utils/                     # Helper functions
            Files starting with "test_"     # Test cases

        web_app/                                                                                                    !!
            app.py                          # Remote-hosted Flask web app for card lookup
            static/scripts.js               # JavaScript components
            templates/view_cards.html       # HTML component

        logs/                               # Location of debugging logs
        
        Dockerfile                          # Dockerfile for this project
        ...


## Feature Overview

The following is a list of the the biggest features within my project with a bit of explanation for each.
- The `src/Dinosaur_Venture/dinosaur_venture/` file
    - This handles all the main logic for running the game. 
- Entities (`src/Dinosaur_Venture/entities/*`)
    - All the playable characters (found in `dinoes.py`) and enemy characters (found in `enemieses.py`) inherit `entity.py`, which contains a lot of the functionality for drawing cards, taking damage, the start of round, etc. 
- Dinosaur Cards (`src/Dinosaur_Venture/dino_cards_depot/*`)
    - The player cards (called Dinosaur cards since the player was originally a dinosaur) are all found in this file. Every card is unique, and some are pretty significantly complicated. 
    - The vast majority of the `*.py` files in this folder have interesting code.
    - ~150 implemented; ~20 in development. 
- Enemy Cards (`src/Dinosaur_Venture/enemy_cards_depot/enemy_cards.py`)
    - The list of enemy cards; all are also unique. 
    - ~40 implemented.
- scripts (`scripts/*`)
    - `push_to_recruiter_repo.ps1` merges my personal, development repo with the public/recruiter repo. Also removes files not needed for the public-facing repo, like a TODO list. 
    - `clear_logs.py` clears the log writing for this game. In `src/Dinosaur_Venture/gameplay_logging`, I created custom logging functionality so different moments throughout a game are saved in an external location. That way, if there is some sort of buggy functionality, I can trace these logs to understand what is incorrect. This devtool clears all of those logs. 
- Test Cases (`tests/`)
    - I have been working to implement test cases for my game, which can be found within this folder.
- Simulate Cards Web Application (`web_app/`)
    - As a tool for looking at the list of all cards in the game, I have created a small remotely-hosted web application using Python, JavaScript, and HTML.
    - The tool contains several checkboxes for selecting which table to include for looking at the code, and buttons for toggling certain sets of cards (like selecting all the playable characters' cards). It also contains RegEx tools for looking up cards based on their name and on their card text.

## Current Main Focuses

- Adding more test cases
    - I have been trying to add better test coverage of my project. With 200+ cards in the game, there is a lot of work to be done to have thourough test coverage, so I have been creating tests on the most essential and most potentially-buggy features. 
- Better UI
    - Most of my focus is on the backend logic of my game, so the UI is currently command line with the `colorama` package for unique text coloring and styling. 
    - Almost all of the visual elements of this game are handled with `src/Dinosaur_Venture/main_visuals.py`, with some helper calls found in in `src/Dinosaur_Venture/helper.py`. The UI aspect of my program is well factored (almost every print statement is found in either of those two aforementioned files), so I best prepped my code to support this change. 
- Refactoring / Improved Code Style
    - Some parts of my program were coded several years ago at this point, and were programmed at a time where the direction of the project was slightly different, so I am working to refactor elements of my program. Most recently, I split all of the player cards into files divided based on the different loot tables they belong to (see `src/Dinosaur_Venture/dino_cards_depot/`); originally, all of these cards were in a single `dinoCards.py` file. 
    - Moreover, I did not fully understand the style guide of Python, and a lot of variable/file/class names and function/class/file comments are more like Java than like Python. I have been trying to improve some of these style problems in my code. 
    - Lastly, I also want to add more type hints across the entirety of my program. They are very helpful and increase my own productivity significantly in having them.  
- Adding more Cards, Clearings, Playable Characters, and Enemies
    - I am continuously working to add more content to my game. 