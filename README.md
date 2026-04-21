# Card Venture — Deck-Building Card Game & Card Query Web Service

A turn-based, deck-building card game built in Python over 5+ years, including a live AWS-hosted web service for querying and filtering all 200+ in-game cards. 

**See the card querying application:** [app.deck-building-card-game.com](app.deck-building-card-game.com).

## What is this?

Card Venture Game is a command-line, deck-building rogue-like where the player traverses clearings, fights monsters, and refines their deck through combat rewards. The project has 12,000+ lines of Python across 13+ interacting subsystems, all designed from the ground up to scale robustly as new and novel cards, enemies, and mechanics are added.

Alongside the game itself, this repository contains a full-stack web application for browsing and filtering every card in the game. It is utilized as both a development tool and as a way to demonstrate the scope of this project.

---
 
## Projects at a Glance
 
| Project | Stack | Link |
|---|---|---|
| Deck-Building Card Game | Python, PyTest, Docker, GitHub Actions, PowerShell | This repo |
| [Card Query Web Service](#card-query-web-service) | React, TypeScript, Tailwind CSS, Flask, AWS Lambda, Zappa, S3, API Gateway | [app.deck-building-card-game.com](https://app.deck-building-card-game.com/) |
 
## Technical Highlights

### Layered Card Architecture
Cards are split into two distinct layers:
1. A **base card class** that defines default behavior ([`card.py`](src/Dinosaur_Venture/cards/mechanics/card.py)) including often-repeated card functionality (`card_functions.py`).
2. A **runtime modification layer** ([`card_mod_functions.py`](src/Dinosaur_Venture/cards/mechanics/card_mod_functions.py), [`card_tokens.py`](src/Dinosaur_Venture/cards/mechanics/card_tokens.py)) that allows behavior to be overridden, altered, or introduced mid-game. 

This separation streamlines introduction of complex, novel card effects without altering the core Card logic, helping the project scale easily and robustly. 

### Card Reaction System
Cards can react to specific game state conditions, allowing cards to be upgraded mid-combat. [`react.py`](src/Dinosaur_Venture/react.py) coordinates these event systems to enable this functionality, requiring cleanly-designed and well-communicated functionality across the card, game state, and enemy subsystems, keeping each well-bounded while enabling complex and dynamic interactions.

**Examples:** many of `The Pier` cards in [`the_pier_cards.py`](src/Dinosaur_Venture/cards/depot/dino_cards/the_pier_cards.py) react to game state conditions. Look for cards that create a `r.card_responseAndTrigger` object, which each have a `response` (returns an object denoting if the game state conditions are met) and a `trigger` (the "upgrade" that occurs when the game state conditions are met).

### Custom Gameplay Logging and Testing Framework
Rather than relying solely on unit tests to test for correctness of these cards, a **custom logging system** ([`gameplay_logging.py`](src\Dinosaur_Venture\logging\gameplay_logging.py)) stores records of game events in memory and disk throughout the play. These test suites (`categorical_card_tests/`) use `Intent` objects to check if the sequence of logged behavior matches that of intended behavior. It enables verification of gameplay correctness (for instance, did this card actually deal damage?) rather than simply testing function outputs. It automates and permanently maintains the manual verification of new or changed card behavior. 

This testing framework is layered on top of standard PyTest unit testing (`tests/effects/`) and are run automatically with GitHub actions on every push. 

### Serverless RESTful API with CI/CD
The card browser backend is a **Flask API deployed as an AWS Lambda function with Zappa** using an API Gateway, fully serverless. The frontend is a React/TypeScript application hosted on AWS S3. Both are deployed with **GitHub Actions pipelines using AWS IAM OIDC authentication**, meaning there are no stored AWS credentials anywhere for deploying this web service. 

To best test this web service in development, a PowerShell script (`run_developer_website.ps1`) is used to automate and remove errors from the process of spinning up the developer backend and frontend. 

More info available in [Card Query Web Service](#card-query-web-service) section.

### Repo Management Tools

A PowerShell script ([`push_to_recruiter_repo.ps1`](scripts/push_to_recruiter_repo.ps1)) automates merging of the private development repository into this public-facing repository, removing any internal or private files (like TODO lists). Removes error-prone manual repository merging and automates the process.

## Architecture Overview


```
Card-Venture-Game/
├── .github/workflows/
│   ├── pytest.yml                     # Runs full PyTest suite on push/pull request
│   ├── deploy_web_backend.yml         # Deploys Flask API to AWS Lambda
│   └── deploy_web_frontend.yml        # Deploys React frontend to AWS S3
│
├── scripts/
│   └── push_to_recruiter_repo.ps1     # Merges private dev repo to public repo
│   └── run_developer_website.ps1      # Spins up dev instances of the backend/frontend
│
├── src/Dinosaur_Venture/
│   ├── cards/
│   │   ├── depot/
│   │   │   ├── dino_cards/            # 165+ unique player cards
│   │   │   └── enemy_cards/           # 40+ unique enemy cards
│   │   └── mechanics/
│   │       ├── card.py                # Base card class
│   │       ├── card_functions.py      # Shared and modifiable on-play logic
│   │       ├── card_mod_functions.py  # Runtime card behavior of `card_functions.py`
│   │       ├── card_tokens.py         # Token system for card state mutation
│   │       └── card_location.py       # Array-like container for card location tracking
│   │
│   ├── entities/
│   │   ├── entity.py                  # Base entity
│   │   ├── dinoes.py                  # Playable characters logic
│   │   └── enemieses.py               # Enemy logic
│   │
│   ├── logging/
│   │   ├── gameplay_logging.py        # In-memory + disk event logger
│   │   ├── intent.py                  # Intent objects for testing of logs
│   │   └── log_entry.py               # Log entries structure
│   │
│   ├── channel_linked_lists.py        # Custom linked list for health/damage channels
│   ├── react.py                       # Card upgrade/reaction system
│   ├── dinosaur_venture.py            # Main game loop entry point
│   ├── debug_run_dinosaur_venture.py  # Developer mode entry point
│   ├── gameplay_loop_events.py        # Game events
│   ├── gameplay_scripted_input.py     # Simulates user input for testing
│   ├── main_visuals.py                # All command-line rendering with `colorama`
│   └── helper.py                      # Shared utility functions
│
├── tests/
│   ├── categorical_card_tests/        # Card correctness testing
│   ├── effects/
│   │   ├── card_effects/              # `cards/` behavior testing (excluding cards themselves)
│   │   ├── entity_effects/            # `entity/` behavior testing
│   │   └── helper_functions/          # `helper.py` behavior testing
│   └── test_utils/                    # Testing utilities
│
├── web_app/
│   ├── app.py                         # Flask API Backend
│   └── frontend/                      # React/TypeScript Frontend
│
└── Dockerfile                         # Containerizes the game
```

## Running the Game
### With Docker:
```
docker build -t card-game .
docker run -it card-game
```

### Locally:
```
pip install -e .
python src/Dinosaur_Venture/dinosaur_venture.py
```

### Run tests:
```
pytest
```

## Card Query Web Service

The card browser ([app.deck-building-card-game.com](https://app.deck-building-card-game.com/)) lets users query and filter all 200+ cards in the game. 

### Features:

- **Regex searching** by both card name and card text.
- **Table filtering** to select which card pools to include or exclude.
- **Group-select buttons** to select groups of tables, like all player cards.
- **Color coding** of card text that matches how cards are displayed in game, like how 'Cards' is colored green or 'Action' is colored blue, keeping the website consistent with gameplay.

### Infrastructure:
- Frontend: React, TypeScript, and Tailwind CSS hosted on AWS S3
- Backend: [Python Flask API](web_app/app.py), deployed as an AWS Lambda function using Zappa accessed with API Gateway
- DNS: AWS Route 53
- Deployment: Automated [frontend deployment](.github/workflows/deploy_web_frontend.yml) and [backend deployment](.github/workflows/deploy_web_backend.yml) with GitHub Actions using AWS IAM OIDC

## Current Development Focus
 
- **Test coverage**: With 200+ unique cards, developing testing is a continuous process. Priority is placed the most complex and most failure-prone card interactions. 
- **UI**: The game currently runs in the command line with `colorama` styling. All visual logic is cleanly isolated and handled in `main_visuals.py`, making graphical user interface migration in the future straightforward.
- **Refactoring with Python style**: Updating older code to follow Python conventions (naming, type hints, docstrings) is a big focus. Core files like `card.py` and `entity.py` have been updated as such, with the goal to update more of the older code accordingly.
- **More web page content**: Moving a rules document to the website, along with other useful information like information about different enemies is a current focus.
- **New content**: Continuously adding cards, clearings, enemies, playable characters, and mechanics.

## Why This Project Exists
 
This project began in 2020 as a way for me to develop and showcase software engineering skills and build something I would actually enjoy playing. Over the last 6 years, it has grown from a simple 1-page script into a multi-subsystem project with automated testing, a live web service hosted on AWS, and with CI/CD infrastructure. Every major design decision, including the layered card system, log-based testing, and AWS deployment, was driven by a real problem I had run into and had to solve. 