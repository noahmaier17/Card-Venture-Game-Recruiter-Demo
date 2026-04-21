# Deck-Building Card Game

A turn-based command-line card game, in which the player (named Dino) traverses across different clearings, fights monsters they meet, and improves their deck based on the enemies they defeat. Includes 13+ core subsystems designed to best scale with the introduction of new and novel card effects. Contains code for a web application ([https://app.deck-building-card-game.com/](https://app.deck-building-card-game.com/)) hosted on AWS to query and filter all 200+ cards in the game.

## File Structure

The following depicts and explains the project directory. The most important and noteworthy files/folders have been denoted by markers to highlight their role in the project.

**Legend**
- `[ENTRY]` – Project entry points that start code
- `[CORE]`  – Noteworthy core systems
- `[DATA]`  – Large collections of content and code
- `[TOOL]`  – Key development or repository tools
- `[APP]`   – Separate applications

**Files**

    Card-Venture-Game/
        .github/workflows/                      # GitHub Actions; automatically runs pytest on push/pull
            pytest.yml                          # Runs PyTest test suite
            deploy_web_backend.yml              # Deploys AWS-hosted Flask API
            deploy_web_frontend.yml             # Deploys AWS-hosted React frontend website
        ...

        scripts/
            push_to_recruiter_repo.ps1          # Merges private repo with public/recruiter-facing repo             [TOOL]
            clear_logs.py                       # Clears all logs in logs/ folder
            ...

        src/
            Dinosaur_Venture/
                cards/                          # Contains card-related files
                    depot/
                        dino_cards/*            # Contains all 165+ player cards                                    [DATA]
                        enemy_cards/*           # Contains all 40+ enemy cards                                      [DATA]
                    mechanics/
                        card_functions.py       # Handles often-repeated card on-play logic
                        card_location.py        # Array-like container for locations of cards (like play, discard, etc.)
                        card_mod_functions.py   # Allows for modification of that often-repeated on-play logic
                        card_tokens.py          # Tokens placed on cards that modify card behavior
                        card.py                 # Card class file                                                   [CORE]

                devtools/                       # Development utilities
                entities/
                    dinoes.py                   # Logic for player entity
                    enemieses.py                # Logic for all enemy entities
                    entity.py                   # Logic for entities                                                [CORE]
                logging/
                    gameplay_logging.py         # Runs a physical and in-memory logger of game events
                    intent.py                   # Creates Intent classes to compare against expected logging behavior
                    log_entry.py                # The log entries of the gameplay logger

                channel_linked_lists.py         # Health and damage Linked List implementation
                debug_run_dinosaur_venture.py   # Runs the game in a developer mode                                 [ENTRY]
                dinosaur_venture.py             # Runs the game                                                     [ENTRY]
                gameplay_loop_events.py         # Game events; closely coupled with dinosaur_venture.py and testing
                gameplay_scripted_input.py      # Simulates user input for the purpose of testing
                helper.py                       # Helper functions                                                  [DATA]
                main_visuals.py                 # Handles the command-line UI
                react.py                        # Handles when cards can react to the current game state
                ...

        tests/
            categorical_card_tests/*            # Tests cards individually based on their loot table                [CORE]
            effects/
                card_effects/*                  # Tests correctness of card behavior
                entity_effects/*                # Tests correctness of entity behavior
                helper_functions/*              # Tests correctness of helper functions found in helper.py
            test_utils/*                        # Testing utilities

        web_app/                                                                                                    [APP]
            app.py                              # AWS-hosted Flask API for card lookup                              [ENTRY]
            frontend/*                          # React-based TypeScript frontend                                   [ENTRY]
            static/scripts.js                   # Deprecated JavaScript components
            templates/view_cards.html           # Deprecated HTML component

        logs/                                   # Location of debugging logs
        
        Dockerfile                              # Dockerfile for this project
        ...


## Feature Overview

The following is a list of the the biggest features within my project with a bit of explanation for each.
- The `src/Dinosaur_Venture/dinosaur_venture/` file
    - This handles all the main logic for running the game. 
- Entities (`src/Dinosaur_Venture/entities/*`)
    - All the playable characters (found in `dinoes.py`) and enemy characters (found in `enemieses.py`) inherit `entity.py`, which contains a lot of the functionality for drawing cards, taking damage, the start of round, etc. 
- Dinosaur Cards (`src/Dinosaur_Venture/cards/depot/dino_cards/*`)
    - The player cards (called Dinosaur cards since the player was originally a dinosaur) are all found in this file. Every card is unique, and some are pretty significantly complicated. 
    - The vast majority of the `*.py` files in this folder have interesting code.
- Enemy Cards (`src/Dinosaur_Venture/cards/depot/enemy_cards/*`)
    - The list of enemy cards; all are also unique. 
- scripts (`scripts/*`)
    - `push_to_recruiter_repo.ps1` merges my personal, development repo with the public/recruiter repo. Also removes files not needed for the public-facing repo, like a TODO list. 
    - `clear_logs.py` clears the log writing for this game. In `src/Dinosaur_Venture/gameplay_logging`, I created custom logging functionality so different moments throughout a game are saved in an external location. That way, if there is some sort of buggy functionality, I can trace these logs to understand what is incorrect. This devtool clears all of those logs. 
- Test Cases (`tests/`)
    - I have been working to implement test cases for my game, which can be found within this folder.
- Simulate Cards Web Application (`web_app/`)
    - As a tool for looking at the list of all cards in the game, I have created a continuously deployed web application using Python, TypeScript, HTML, AWS, and Zappa. AWS services I utilized included API Gateway, AWS Lambda, S3, and Route 53.
    - The tool contains several checkboxes for selecting which table to include for looking at the code, and buttons for toggling certain sets of cards (like selecting all the playable characters' cards). It also contains RegEx tools for looking up cards based on their name and on their card text.
    - Web application link: [https://app.deck-building-card-game.com/](https://app.deck-building-card-game.com/)

## Most Recent Big Feature/Addition

I converted my JavaScript code to utilize TypeScript. This required adding better typing and type-checking to some of my Python backend code, and converting several files from JavaScript to TypeScript. I utilized when convenient Generative AI (Claude) to help with that process, both helping me better understand how certain React elements are typed in TS, and to best determine the implicit types I was utilizing in JavaScript. 

It was a big task and took 2 weeks to complete. 

## Current Main Focuses

- Adding more test cases
    - I have been trying to add better test coverage of my project. With 200+ cards in the game, there is a lot of work to be done to have thorough test coverage, so I have been creating tests on the most essential and most potentially-buggy features. 
- Better UI
    - Most of my focus is on the backend logic of my game, so the UI is currently command line with the `colorama` package for unique text coloring and styling. 
    - Almost all of the visual elements of this game are handled with `src/Dinosaur_Venture/main_visuals.py`, with some helper calls found in in `src/Dinosaur_Venture/helper.py`. The UI aspect of my program is well factored (almost every print statement is found in either of those two aforementioned files), so I best prepped my code to support this change. 
- Refactoring / Improved Code Style
    - Some parts of my program were coded several years ago at this point, and were programmed at a time where the direction of the project was slightly different, so I am working to refactor elements of my program. 
    - Moreover, I did not fully understand the style guide of Python when this project originally began, and so several variable/class names and function/class/file comments are more in the style of Java than of Python. 
    - Lastly, I also want to add more type hints across the entirety of my program. They are very helpful and increase my own productivity significantly in having them.  
- Adding more Cards, Clearings, Playable Characters, and Enemies
    - I am continuously working to add more content to my game. 