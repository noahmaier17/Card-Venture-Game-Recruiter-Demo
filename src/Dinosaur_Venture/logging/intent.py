"""
intent.py

Compares the intent of a card to what is logged. Useful for DSL card testing.
"""

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from Dinosaur_Venture.logging.log_entry import LogEntry

class Intent():
    """
    Contains a list of parameters to check if the LogEntry in the log matches this LogEntry. 
    We use this `Intent` class so we can include additional parameters beyond the LogEntry type.
    For instance, {"name": "Mangled Shrew"} can test if this LogEntry has a parameter
    "name" with a value of "Mangled Shrew"
    """
    def __init__(self, log_class: Type["LogEntry"], python_object_parameters: dict):
        self.log_class: Type["LogEntry"] = log_class
        # I used to have JSON parameters but python_object_parameters essentially covers what I want
        # self.json_parameters: dict = json_parameters
        self.python_object_parameters: dict = python_object_parameters