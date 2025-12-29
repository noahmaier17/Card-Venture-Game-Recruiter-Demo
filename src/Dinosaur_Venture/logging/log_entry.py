"""
log_entry.py

Creates entries within the log for specific game events.
Each LogEntry is coupled with specific classes/function calls.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Dinosaur_Venture import card as c
    from Dinosaur_Venture import card_functions as cf
    from Dinosaur_Venture import channel_linked_lists as cll
    from Dinosaur_Venture import helper as h
    from Dinosaur_Venture import main_visuals as vis
    from Dinosaur_Venture.entities import entity as e
    from Dinosaur_Venture import react as r

def serialize_object(object):
    """
    Helper method. Seralizes the object into JSON.
    """
    # Do we have a basic data type?
    if object is None or isinstance(object, (int, float, str, bool)):
        return object

    # Do we have a list/tuple we must recurse across?            
    elif isinstance(object, (list, tuple)):
        return_object = []
        for value in object:
            return_object.append(serialize_object(value))
        
        if isinstance(object, tuple):
            return tuple(return_object)
        else:
            return return_object
    
    # Do we have a dictionary?
    elif isinstance(object, dict):
        return_object = {}
        for key, value in object.items():
            return_object[key] = serialize_object(value)
        return return_object
    
    # Do we have an object with logIdentity or log_identity call?
    elif hasattr(object, "logIdentity") and callable(object.logIdentity):
        return serialize_object(object.logIdentity())
    elif hasattr(object, "log_identity") and callable(object.log_identity):
        return serialize_object(object.log_identity())

    raise Exception("Cannot serialize parameter " + str(object))
    
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
        # We need to both include a JSON entry for this type of log...
        log_json = {
            "log_type": self._LOG_TYPE
        }

        # ... and serialize the remaining attributes
        return log_json | serialize_object(self.__dict__)

class EntityLogEntry(LogEntry):
    """
    Log Entries found within functions within `entity.py`.
    The purpose of this inheritance is mostly for code quality.
    """

class EntityDiscardCard(EntityLogEntry):
    """
    Log for discarding a card.
    Employed in `entity.discardCard()`.
    """
    _LOG_TYPE = "Entity Discard Card"

    def __init__(
        self,
        fromLocation: "h.cardLocation",
        cardIndex: int,
        dino: "e.Entity",
        enemies: list["e.Entity"],
        passedInVisuals: "vis.prefabPassedInVisuals",
        moments: list["r.reactMoments"],
        printCard: bool,
        inputCard: bool
    ) -> None:
        self.fromLocation = fromLocation
        self.cardIndex = cardIndex
        self.dino = dino
        self.enemies = enemies
        self.passedInVisuals = passedInVisuals
        self.moments = moments
        self.printCard = printCard
        self.inputCard = inputCard

class EntityDamage(EntityLogEntry):
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

class EntityPlusActionsLogEntry(EntityLogEntry):
    """
    Log for + Actions.
    Employed in `entity.plusActions()`.
    """
    _LOG_TYPE = "Entity Plus Actions"

    def __init__(self, entity: "e.Entity", plusActions: int) -> None:
        self.entity = entity
        self.plusActions = plusActions

class EntityMoveMeLogEntry(EntityLogEntry):
    """
    Log for moving a card by card object.
    Employed in `entity.moveMe()`.
    """
    _LOG_TYPE = "Entity Move Me"

    def __init__(
        self,
        entity: "e.Entity",
        fromLocation: "h.cardLocation",
        card: "c.Card",
        toLocation: "h.cardLocation",
        position: int,
        printCard: bool,
        inputCard: bool,
        suppressFailText: bool
    ) -> None:
        self.entity = entity
        self.fromLocation = fromLocation
        self.card = card
        self.toLocation = toLocation
        self.position = position
        self.printCard = printCard
        self.inputCard = inputCard
        self.suppressFailText = suppressFailText

class EntityPlayCardLogEntry(EntityLogEntry):
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

class EntityDrawCard(EntityLogEntry):
    """
    Log for drawing a Card.
    Employed in `entity.drawCard()`.
    """
    _LOG_TYPE = "Entity Draw Card"

    def __init__(
        self,
        entity: "e.Entity",
        fromLocation: "h.cardLocation", 
        toLocation: "h.cardLocation", 
        shuffleLocation: "h.cardLocation", 
        printCard: bool, 
        inputCard: bool
    ) -> None:
        self.fromLocation = fromLocation
        self.toLocation = toLocation
        self.shuffleLocation = shuffleLocation
        self.printCard = printCard
        self.inputCard = inputCard

class EntityPackingCardLogEntry(EntityLogEntry):
    """
    Log for playing a Card.
    Employed in `entity.packCard()`.
    """    
    _LOG_TYPE = "Entity Packing Card"

    def __init__(
        self,
        entity: "e.Entity",
        fromLocation: "h.cardLocation",
        cardIndex: int,
        caster: "e.Entity",
        dino: "e.Entity",
        enemies: list["e.Entity"]
    ) -> None:
        self.packedCard = fromLocation.at(cardIndex) # Customly added for ease of log parsing
        self.entity = entity
        self.fromLocation = fromLocation
        self.cardIndex = cardIndex
        self.caster = caster
        self.dino = dino
        self.enemies = enemies

class EntityPlusUpcomingPlusAction(EntityLogEntry):
    """
    Log for playing a Card.
    Employed in `entity.plusUpcomingPlusAction()`.
    """    
    _LOG_TYPE = "Entity Plus Upcoming Plus Action"

    def __init__(
        self,
        caster: "e.Entity",
        when: int, 
        count: int
    ) -> None:
        self.caster = caster
        self.when = when
        self.count = count

class EntityPlusUpcomingPlusCard(EntityLogEntry):
    """
    Log for playing a Card.
    Employed in `entity.plusUpcomingPlusCard()`.
    """    
    _LOG_TYPE = "Entity Plus Upcoming Plus Card"

    def __init__(
        self,
        caster: "e.Entity",
        when: int, 
        count: int
    ) -> None:
        self.caster = caster
        self.when = when
        self.count = count

class HelperFunctionLogEntry(LogEntry):
    """
    Log Entries found within functions within `helper.py` (or similar helper-method files).
    The purpose of this inheritance is mostly for code quality.
    """

class HelperPickLivingEnemy(LogEntry):
    """
    Log for picking a living enemy.
    Employed in `helper.pickLivingEnemy()`
    """
    _LOG_TYPE = "Helper Pick Living Enemy"

    def __init__(
        self,
        text: str, 
        enemies: list["e.Enemies"], 
        preamble: list[str], 
        passedInVisuals: "vis.prefabPassedInVisuals"
    ) -> None:
        self.text = text
        self.enemies = enemies
        self.preamble = preamble
        self.passedInVisuals = passedInVisuals

class HelperYesOrNoLogEntry(LogEntry):
    """
    Log for answering Yes or No.
    Employed in `helper.yesOrNo()`
    """
    _LOG_TYPE = "Helper Yes or No Log Entry"

    def __init__(
        self,
        text: str,
        preamble: list,
        passedInVisuals: "vis.prefabPassedInVisuals"
    ) -> None:
        self.text = text
        self.preamble = preamble
        self.passedInVisuals = passedInVisuals

class CardFunctionLogEntry(LogEntry):
    """
    Log Entries found within functions within `card_functions.py`.
    The purpose of this inheritance is mostly for code quality.
    """

class CardFunctionDrawUntilYouHaveXCardsInHand(CardFunctionLogEntry):
    """
    Log for drawing until you have X Card(s) in Hand.
    Employed in `card_functions.drawUntilYouHaveXCardsInHand()`.
    """    
    _LOG_TYPE = "Card Function Draw To X in Hand"

    def __init__(
        self,
        cardFunction: "cf.cardFunctions",
        card: "c.Card", 
        caster: "e.Entity", 
        dino: "e.Entity", 
        enemies: list["e.Entity"], 
        passedInVisuals: "vis.prefabPassedInVisuals"
    ) -> None:
        self.cardFunction = cardFunction
        self.card = card
        self.caster = caster
        self.dino = dino
        self.enemies = enemies
        self.passedInVisuals = passedInVisuals

class CardFunctionArbitrarilyDiscardCardFrom_Location(CardFunctionLogEntry):
    """
    Log for discarding an arbitrary card from [ location ].
    Employed in `card_functions.arbitrarilyDiscardCardFrom_Location()`.
    """    
    _LOG_TYPE = "Arbitrarily Discard Card From Location"

    def __init__(
        self,
        cardFunction: "cf.cardFunctions",
        card: "c.Card", 
        caster: "e.Entity", 
        dino: "e.Entity", 
        enemies: list["e.Entity"], 
        passedInVisuals: "vis.prefabPassedInVisuals"
    ) -> None:
        self.cardFunction = cardFunction
        self.card = card
        self.caster = caster
        self.dino = dino
        self.enemies = enemies
        self.passedInVisuals = passedInVisuals
    