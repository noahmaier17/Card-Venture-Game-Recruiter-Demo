"""
gameplay_logging.py

Logs moments in the game so they can reviewed for bug checking.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from Dinosaur_Venture import card as c
    from Dinosaur_Venture import channel_linked_lists as cll
    from Dinosaur_Venture import helper as h
    from Dinosaur_Venture.entities import entity as e

## ----- Gameplay Logging -----
class LogEntry(ABC):
    """
    Parent class of LogEntry classes.
    """
    _LOG_TYPE: str # Must implement for each LogEntry class

    @abstractmethod
    def __init__(self) -> None:
        """
        Creates a log entry.
        """

    def to_json(self) -> dict:
        """Transforms all attributes of this class into JSON."""
        def serialize(object):
            # Do we have a basic data type?
            if object is None or isinstance(object, (int, float, str, bool)):
                return object

            # Do we have a list/tuple we must recurse across?            
            elif isinstance(object, (list, tuple)):
                return_object = []
                for value in object:
                    return_object.append(serialize(value))
                
                if isinstance(object, tuple):
                    return tuple(return_object)
                else:
                    return return_object
            
            # Do we have a dictionary?
            elif isinstance(object, dict):
                return_object = {}
                for key, value in object.items():
                    return_object[key] = serialize(value)
                return return_object
            
            # Do we have an object with logIdentity or log_identity call?
            elif hasattr(object, "logIdentity") and callable(object.logIdentity):
                return serialize(object.logIdentity())
            elif hasattr(object, "log_identity") and callable(object.log_identity):
                return serialize(object.log_identity())

            raise Exception("Cannot serialize parameter " + str(object))
        
        # We need to both include a JSON entry for this type of log...
        log_json = {
            "log_type": self._LOG_TYPE
        }

        # ... and serialize the remaining attributes
        return log_json | serialize(self.__dict__)

class EntityDamage(LogEntry):
    """
    Log for dealing damage.
    Employed in `entity.damage()`.
    """
    _LOG_TYPE = "Entity Damage"

    def __init__(
        self,
        caster: "e.Entity", 
        dino: "e.Entity", 
        enemies: list["e.Entity"], 
        attackData: "cll.Attackcons"
    ) -> None:
        self.caster = caster
        self.dino = dino
        self.enemies = enemies
        self.attackData = attackData

class EntityPlusActionsLogEntry(LogEntry):
    """
    Log for + Actions.
    Employed in `entity.plusActions()`.
    """
    _LOG_TYPE = "Entity Plus Actions"

    def __init__(self, entity: "e.Entity", plusActions: int) -> None:
        self.entity = entity
        self.plusActions = plusActions

class EntityPlayCardLogEntry(LogEntry):
    """
    Log for playing a Card.
    Employed in `entity.playCard()`.
    """    
    _LOG_TYPE = "Entity Play Card"

    def __init__(
        self,
        entity: "e.Entity",
        fromLocation: "h.cardLocation",
        cardIndex: int,
        caster: "e.Entity",
        dino: "e.Entity",
        enemies: list["e.Entity"]
    ) -> None:
        self.playedCard = fromLocation.at(cardIndex) # Customly added for ease of log parsing
        self.entity = entity
        self.fromLocation = fromLocation
        self.cardIndex = cardIndex
        self.caster = caster
        self.dino = dino
        self.enemies = enemies

class Intent():
    """
    Contains a list of parameters to check if the LogEntry in the log matches this LogEntry. 
    We use this `Intent` class so we can include additional parameters beyond the LogEntry type.
    For instance, {"name": "Mangled Shrew"} can test if this LogEntry has a parameter
    "name" with a value of "Mangled Shrew"
    """
    def __init__(self, log_class: Type[LogEntry], python_object_parameters: dict):
        self.log_class: Type[LogEntry] = log_class
        # I used to have JSON parameters but python_object_parameters essentially covers what I want
        # self.json_parameters: dict = json_parameters
        self.python_object_parameters: dict = python_object_parameters

## ----- Logger Classes -----
# For CI, we need to create an in-memory logger instead of a physical logger
class Logger(ABC):
    """Abstract class for creating logging for game moments."""
    @abstractmethod
    def __init__(self) -> None:
        """Creates the logger."""

    @abstractmethod
    def open(self) -> None:
        """Opens the logger."""

    @abstractmethod
    def _write(self, text: str) -> None:
        """
        Writes to the logger the input log_entry.
        Each individual write call acts as its own entry in the log.
        """

    @abstractmethod
    def read(self) -> str:
        """Reads the log."""

    def write_log_entry_to_log(self, LogEntry: LogEntry) -> None:
        """
        Enters the log information, including what type of log we are using.
        """
        self._write(LogEntry)

class PhysicalLogger(Logger):
    """Physically logs game events to a file in JSON. Used throughout the game."""
    def __init__(self) -> None:
        log_file_name = "Logs/" + str(datetime.now())
        log_file_name = log_file_name.replace(":", ".") + ".jsonl"

        self.log_file_name = log_file_name

    def open(self) -> None:
        open(self.log_file_name, 'x')

    def _write(self, log_entry: LogEntry) -> None:
        # Opens the file
        with open(self.log_file_name, "a") as file:
            # Converts the log entry into almost-JSON
            dictonary = log_entry.to_json()

            # Converts that dictionary into JSON
            JSON = json.dumps(dictonary, indent=2)

            # Writes it
            file.write(JSON + "\n")
    
    def read(self) -> str:
        with open(self.log_file_name, "a") as file:
            return file.read() 

class InMemoryLogger(Logger):
    """Logs game events in memory as Logger.Log class instances. Used for testing."""
    def __init__(self) -> None:
        self.log_crawl_index: int = 0
        self.logs: list[LogEntry] = []

    def open(self) -> None:
        pass # Nothing needs to be opened

    def _write(self, log_entry: LogEntry) -> None:
        self.logs.append(log_entry)
    
    def read(self) -> str:
        returnString = ""
        for line in self.logs:
            returnString.append(line + "\n")
        return returnString
    
    def get_next_log_line(self) -> LogEntry:
        """
        Crawls the log LogEntry by LogEntry.
        """
        if not self.contains_next_log_line():
            assert Exception("Out of bounds error for log crawling")

        returnLogEntry = self.logs[self.log_crawl_index]
        self.log_crawl_index += 1
        return returnLogEntry
    
    def contains_next_log_line(self) -> bool:
        """
        Returns True if the log contains another line.
        """
        return self.log_crawl_index < len(self.logs)

## ----- Logger Variable -----
# The variable that accesses the Logger class; initialized with a new_*_log_file() call
_log = None

## ----- Core Logging Functions -----
def new_in_memory_log_file() -> None:
    """Creates a new in-memory log file; used for testing."""
    global _log
    _log = InMemoryLogger()

def new_physical_log_file() -> None:
    """Creates a new log file; done at the start of every gameplay run."""    
    global _log
    _log = PhysicalLogger()

def write_to_log(log_entry: LogEntry) -> None:
    """General function for writing text."""
    _log.write_log_entry_to_log(log_entry)

def get_next_log_line() -> LogEntry:
    """Crawls the log, line by line."""
    return _log.get_next_log_line()

def contains_next_log_line() -> bool:
    """Returns True if the log contains another line."""
    return _log.contains_next_log_line()

## ----- Gameplay Logging -----
'''
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
'''