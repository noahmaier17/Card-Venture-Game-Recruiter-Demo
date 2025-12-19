"""
intent.py

Compares the intent of a card to what is logged. Useful for DSL card testing.
"""

from typing import TYPE_CHECKING, Type

from Dinosaur_Venture.logging import log_entry

if TYPE_CHECKING:
    from Dinosaur_Venture import channel_linked_lists as cll
    from Dinosaur_Venture import helper as h

class Intent():
    """
    Contains a list of parameters to check if the LogEntry in the log matches this LogEntry. 
    We use this `Intent` class so we can include additional parameters beyond the LogEntry type.
    For instance, {"name": "Mangled Shrew"} can test if this LogEntry has a parameter
    "name" with a value of "Mangled Shrew"
    """
    def __init__(self, log_class: Type[log_entry.LogEntry], json_parameters: dict, python_object_parameters: dict):
        self.log_class: Type[log_entry.LogEntry] = log_class

        # These json parameters must use the exact name of the attributes as stored in JSON!
        self.json_parameters: dict = json_parameters

        # These python object parameters must use the exact name of the attribute in memory!
        self.python_object_parameters: dict = python_object_parameters

def entity_play_card_intent_factory(card_name: str) -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.EntityPlayCardLogEntry`, 
    forcing inclusion of key parameters.
    
    Arguments:
        card_name (str): the name of the card expected to be played.
    """
    return Intent(
        log_entry.EntityPlayCardLogEntry,
        {},
        {"playedCard.name": card_name}
    )

def entity_packing_card_intent_factory(card_name: str) -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.EntityPlayCardLogEntry`, 
    forcing inclusion of key parameters.
    
    Arguments:
        card_name (str): the name of the card expected to be played.
    """
    return Intent(
        log_entry.EntityPackingCardLogEntry,
        {},
        {"packedCard.name": card_name}
    )

def entity_damage_intent_factory(attackcons: "cll.Attackcons") -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.EntityDamage`, 
    forcing inclusion of key parameters.
    
    Arguments:
        attackcons (cll.Attackcons): the damage that was expected to be dealt.
    """
    return Intent(
        log_entry.EntityDamage,
        {},
        {"attackData": attackcons}    
    )

def entity_plus_actions_intent_factory(plus_actions: int) -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.EntityPlusActionsLogEntry`, 
    forcing inclusion of key parameters.
    
    Arguments:
        plus_actions (cll.Attackcons): the number of plus actions that was expected to be recieved.
    """
    return Intent(
        log_entry.EntityPlusActionsLogEntry,
        {},
        {"plusActions": plus_actions}
    )

def entity_draw_card_intent_factory() -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.EntityDrawCard`, 
    forcing inclusion of key parameters (of which we have none).
    """
    return Intent(
        log_entry.EntityDrawCard,
        {},
        {}
    )

def card_function_draw_until_you_have_x_cards_in_hand_intent_factory(draw_to_x_number: int) -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.CardFunctionDrawUntilYouHaveXCardsInHand`, 
    forcing inclusion of key parameters.
    
    Arguments:
        draw_to_x_number (int): the draw to x value that is expected.
    """
    return Intent(
        log_entry.CardFunctionDrawUntilYouHaveXCardsInHand,
        {},
        {"cardFunction.draw_to_x_number": draw_to_x_number}
    )

def card_function_arbitrarily_discard_card_from_location_intent_factory(location: "h.cardLocation", inputCard: bool) -> Intent:
    """
    Constructs an Intent for comparison against `log_entry.CardFunctionArbitrarilyDiscardCardFrom_Location`, 
    forcing inclusion of key parameters.
    
    Arguments:
        location (h.cardLocation): the location we will arbitrarily discard from.
        inputCard (bool): if 
    """
    return Intent(
        log_entry.CardFunctionArbitrarilyDiscardCardFrom_Location,
        {},
        {
            "cardFunction.location": location,
            "cardFunction.inputCard": inputCard
        }
    )
    