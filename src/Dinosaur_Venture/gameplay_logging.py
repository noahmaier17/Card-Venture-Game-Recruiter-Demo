"""
gameplay_logging.py

Logs moments in the game so they can reviewed for bug checking.
"""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Dinosaur_Venture import card as c
    from Dinosaur_Venture import helper as h
    from Dinosaur_Venture.entities import entity as e

## ----- Constants -----
# Global boolean that will force logging to be ignored (for testing)
IGNORE_GAMEPLAY_LOGGING = True

# Log file name
LOG_FILE_NAME = "Logs/" + str(datetime.now())
LOG_FILE_NAME = LOG_FILE_NAME.replace(":", ".")

## ----- Helper Functions ------
def get_card_location_spiel(cardLocation: "h.cardLocation") -> None:
    """Helper function; gets information about a `helper.cardLocation()`."""
    cardsSpiel = ""
    for card in cardLocation.getArray():
        cardsSpiel += get_card_spiel(card)
    if len(cardLocation.getArray()) == 0:
        cardsSpiel = "None"
    return "{ " + cardLocation.name + " -> " + cardsSpiel + " } "

def get_card_spiel(card: "c.Card") -> None:
    """Helper function; gets information about a `card.Card()`."""
    return "[ " + card.name + " -> tokens: " + str(card.tokens) + " ] "

## ----- Logging -----
def new_log_file() -> None:
    """Creates a new log file; done at the start of every gameplay run."""
    if not IGNORE_GAMEPLAY_LOGGING:
        open(LOG_FILE_NAME, 'x')

def write_to_log(text: str) -> None:
    """General function for writing text."""
    if not IGNORE_GAMEPLAY_LOGGING:
        with open(LOG_FILE_NAME, "a") as file:
            file.write(text + "\n")

def play_card_log(
    entity: "e.Entity",
    fromLocation: "h.cardLocation",
    cardIndex: int,
    caster: "e.Entity",
    dino: "e.Entity",
    enemies: list["e.Entity"]
) -> None:
    """Logs playing a Card."""
    write_to_log(
        "PLAY CARD: " + 
        entity.name + " plays the " + str(cardIndex) + "th card from " + get_card_location_spiel(fromLocation)
    )

def round_start_entity_log(entity: "e.Entity") -> None:
    """Logs the state of an entity at Round Start."""
    locationsSpiel = ""
    for cardLocaiton in entity.getIterableOfLocations():
        locationsSpiel += get_card_location_spiel(cardLocaiton)
    write_to_log(
        "ROUND START: " + 
        entity.name + " state: " + locationsSpiel
    )

def current_event_log(event: str) -> None:
    """Logs the current 'event'."""
    write_to_log(
        "CURRENT EVENT: " +
        event
    )