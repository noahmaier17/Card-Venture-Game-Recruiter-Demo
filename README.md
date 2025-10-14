# Deck-Building Card Game

A command-line game, in which the player (named dino) traverses across different clearings, fights the monsters they meet, and improves their deck based off the enemies they defeat. 

The player continuously fights these clearings until they beat them all!

## Feature Overview

- Clearings (`src/Dinosaur_Venture/clearing.py`)
    - The player character fights 4 battles in a clearing. After the first two, they heal and can loot a card from the clearing.
    - Each clearing has a unique 12-card loot pool; that loot pool is designed to have unique themes and specific strengths/weaknesses when compared to the other clearings. 
    - 6 implemented; ~3 currently in development.
- Dinosaur Cards (`src/Dinosaur_Venture/Dino_Cards_Depot/*`)
    - The player cards (called Dinosaur cards since the player was originally a dinosaur) are all found in this file. 
    - Every card is unique. 
    - ...
- Enemy Cards (`src/Dinosaur_Venture/enemyCards.py`)
    - ...
- devtools (`src/Dinosaur_Venture/devtools/*`)
    - `clearLogs.py` clears the log writing for this game. In `src/Dinosaur_Venture/gameplayLogging`, I created custom logging functionality so different moments throughout a game are saved in an external location. That way, if there is some sort of buggy functionality, I can trace these logs to understand what is incorrect. This devtool clears all of those logs.
    - `simulateCards.py` lets a developer look up cards. It supports looking up cards based on their loot table (e.g. if they are found in the clearing named "New Bear Order"), and based on some sort of RegEx condition. 
    - ...
    - ...
- ...

## Current Main Focus

- Adding more test cases
    - I am currently working
    - ...
- Better UI
    - Most of my focus is on the backend logic of my game, so the UI is currently done through command line in tandem with the `colorama` package for unique text coloring and styling. 
    - Almost all of the visual elements of this game are handled with `src/Dinosaur_Venture/mainVisuals.py`, with some helper calls found in in `src/Dinosaur_Venture/helper.py`. The UI aspect of my program is well factored (almost every print statement is found in either of those two aforementioned files), so I best prepped my code to support this change. 
- More trigger support
    - In `src/Dinosaur_Venture/react.py`, all of the instances of `reactMoments` are the currently supported trigger moments for cards. To support other cards I have planned, I am going to expand on the number of possible trigger moments. 
    - Additionally, only card triggers are currently supported. Entities need to have trigger support (EG, if I want to have an enemy that does something like "When this is defeated, spawn 2 minions").           ...
    - ...
- Refactoring
    - Some parts of my program were coded years ago at this point, and were programmed at a time where the direction of the project was slightly different, so I am working to refactor elements of my program. Most recently, I split all of the player cards into files divided based on the different loot tables they belong to; originally, all of these cards were in the same `dinoCards.py` file.
- Adding more cards and clearings
    - I am always working to add more content to my game! 

## Installation
...