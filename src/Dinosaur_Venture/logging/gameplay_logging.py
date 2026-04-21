"""
gameplay_logging.py

Logs moments in the game so they can reviewed for bug checking.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Dinosaur_Venture.logging.log_entry import LogEntry

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

    def write_log_entry_to_log(self, LogEntry: "LogEntry") -> None:
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

    def _write(self, log_entry: "LogEntry") -> None:
        # Opens the file
        with open(self.log_file_name, "a") as file:
            # Converts the log entry into almost-JSON
            dictionary = log_entry.to_json()

            # Converts that dictionary into JSON
            JSON = json.dumps(dictionary, indent=2)

            # Writes it
            file.write(JSON + "\n")
    
    def read(self) -> str:
        with open(self.log_file_name, "a") as file:
            return file.read() 

class InMemoryLogger(Logger):
    """Logs game events in memory as Logger.Log class instances. Used for testing."""
    def __init__(self) -> None:
        self.log_crawl_index: int = 0
        self.logs: list["LogEntry"] = []

    def open(self) -> None:
        pass # Nothing needs to be opened

    def _write(self, log_entry: "LogEntry") -> None:
        # For testing VS the physical logger, we want to see if we can convert the log entry into JSON
        dictionary = log_entry.to_json()
        _ = json.dumps(dictionary, indent=2)

        self.logs.append(log_entry)
    
    def read(self) -> str:
        returnString = ""
        for line in self.logs:
            returnString.append(line + "\n")
        return returnString
    
    def get_next_log_line(self) -> "LogEntry":
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

def write_to_log(log_entry: "LogEntry") -> None:
    """General function for writing text."""
    _log.write_log_entry_to_log(log_entry)

def get_next_log_line() -> "LogEntry":
    """Crawls the log, line by line."""
    return _log.get_next_log_line()

def contains_next_log_line() -> bool:
    """Returns True if the log contains another line."""
    return _log.contains_next_log_line()