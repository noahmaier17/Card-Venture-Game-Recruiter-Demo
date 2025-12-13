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

## ----- Logging Classes -----
# For CI, we need to create an in-memory logger instead of a physical logger
class Logger():
    """Abstract class for creating logging for game moments."""
    def __init__(self) -> None:
        """Creates the logger."""
        pass

    def open(self) -> None:
        """Opens the logger."""
        pass
    
    def write(self, text: str) -> None:
        """
        Writes to the logger the input text.
        Each individual write call acts as its own entry in the log.
        """
        pass

    def read(self) -> str:
        """Reads the log."""
        pass

class PhysicalLogger(Logger):
    """Physically logs game events as a file. Used throughout the game."""
    def __init__(self) -> None:
        log_file_name = "Logs/" + str(datetime.now())
        log_file_name = log_file_name.replace(":", ".")

        self.log_file_name = log_file_name

    def open(self) -> None:
        open(self.log_file_name, 'x')

    def write(self, text: str) -> None:
        with open(self.log_file_name, "a") as file:
            file.write(text + "\n")
    
    def read(self) -> str:
        with open(self.log_file_name, "a") as file:
            return file.read() 

class InMemoryLogger(Logger):
    """Logs game events in memory. Used for testing."""
    def __init__(self) -> None:
        self.logs = []

    def open(self) -> None:
        pass # Nothing needs to be opened

    def write(self, text: str) -> None:
        self.logs.append(text)
    
    def read(self) -> str:
        returnString = ""
        for line in self.logs:
            returnString.append(line + "\n")
        return returnString

## ----- Logger Variable -----
# The variable that accesses the Logger class; initialized with a new_*_log_file() call
_log = None

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

## ----- Core Logging Functions -----
def new_in_memory_log_file() -> None:
    """Creates a new in-memory log file; used for testing."""
    global _log
    _log = InMemoryLogger()

def new_physical_log_file() -> None:
    """Creates a new log file; done at the start of every gameplay run."""    
    global _log
    _log = PhysicalLogger()

def write_to_log(text: str) -> None:
    """General function for writing text."""
    _log.write(text)

## ----- Gameplay Logging -----
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