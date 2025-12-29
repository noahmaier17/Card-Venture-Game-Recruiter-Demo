"""
intent.py

Compares the intent of a card to what is logged. Useful for DSL card testing.
"""

from typing import TYPE_CHECKING, Type

from Dinosaur_Venture.logging import log_entry

if TYPE_CHECKING:
    from Dinosaur_Venture import card as c
    from Dinosaur_Venture import channel_linked_lists as cll
    from Dinosaur_Venture import helper as h

class Intent():
    """
    Contains a list of parameters to check if the LogEntry in the log matches this LogEntry. 
    We use this `Intent` class so we can include additional parameters beyond the LogEntry type.
    For instance, {"name": "Mangled Shrew"} can test if this LogEntry has a parameter
    "name" with a value of "Mangled Shrew".
    """
    def __init__(self, log_class: Type[log_entry.LogEntry], json_parameters: dict, python_object_parameters: dict):
        self.log_class: Type[log_entry.LogEntry] = log_class

        # These json parameters must use the exact name of the attributes as stored in JSON!
        self.json_parameters: dict = json_parameters

        # These python object parameters must use the exact name of the attribute in memory!
        self.python_object_parameters: dict = python_object_parameters

class IntentFactory():
    """
    For the different log_entry locations (like within entity, helper, etc.) we will have a class to contain all log_entry loactions.
    We will then populate each of them will several static methods that return lists of Intents.

    We return lists of Intents so we can easily return several Intents if need be (or modify these to return multiple Intents in the future).
    Many of these will simply return a single Intent.
    """

class EntityFactory(IntentFactory):
    @staticmethod
    def discard_card(from_location: "h.cardLocation", print_card: bool, input_card: bool) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityDiscardCard`, 
        forcing inclusion of key parameters.

        Arguments:
            from_location (h.cardLocation): where the card is expected to be discarded from.
            print_card (bool): if we want the card to be printed.
            input_card (bool): if we want the card to be input.
        """
        return [Intent(
            log_entry.EntityDiscardCard,
            {},
            {
                "fromLocation": from_location,
                "printCard": print_card,
                "inputCard": input_card
            }
        )]

    def play_card(card_name: str) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityPlayCardLogEntry`, 
        forcing inclusion of key parameters.
        
        Arguments:
            card_name (str): the name of the card expected to be played.
        """
        return [Intent(
            log_entry.EntityPlayCardLogEntry,
            {},
            {"playedCard.name": card_name}
        )]

    def packing_card(card_name: str) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityPlayCardLogEntry`, 
        forcing inclusion of key parameters.
        
        Arguments:
            card_name (str): the name of the card expected to be played.
        """
        return [Intent(
            log_entry.EntityPackingCardLogEntry,
            {},
            {"packedCard.name": card_name}
        )]

    def damage(attackcons: "cll.Attackcons") -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityDamage`, 
        forcing inclusion of key parameters.
        
        Arguments:
            attackcons (cll.Attackcons): the damage that was expected to be dealt.
        """
        return [Intent(
            log_entry.EntityDamage,
            {},
            {"attackData": attackcons}    
        )]

    def plus_upcoming_plus_action(when: int, count: int) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityPlusUpcomingPlusAction`,
        forcing inclusion of key parameters.

        Arguments:
            when (int): how many turns past the next turn the upcoming plus actions is recieved.
                A when value of 0 is next turn.
            count (int): how many plus actions to recieve.
        """
        return [Intent(
            log_entry.EntityPlusUpcomingPlusAction,
            {},
            {
                "when": when,
                "count": count
            }
        )]

    def plus_upcoming_plus_card(when: int, count: int) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityPlusUpcomingPlusCard`,
        forcing inclusion of key parameters.

        Arguments:
            when (int): how many turns past the next turn the upcoming plus cards is recieved.
                A when value of 0 is next turn.
            count (int): how many plus cards to recieve.
        """
        return [Intent(
            log_entry.EntityPlusUpcomingPlusCard,
            {},
            {
                "when": when,
                "count": count
            }
        )]

    def plus_actions(plus_actions: int) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityPlusActionsLogEntry`, 
        forcing inclusion of key parameters.
        
        Arguments:
            plus_actions (cll.Attackcons): the number of plus actions that was expected to be recieved.
        """
        return [Intent(
            log_entry.EntityPlusActionsLogEntry,
            {},
            {"plusActions": plus_actions}
        )]

    def move_me(
        from_location: "h.cardLocation", 
        card: "c.Card", 
        to_location: "h.cardLocation",
        position: int
    ) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityMoveMeLogEntry`, 
        forcing inclusion of key parameters.

        Arguments:
            from_location (h.cardLocation): the location where the card is moved from.
            card (c.Card): the card to move.
            to_location (h.cardLocation): the location where the card is moved to.
            position (int): where in the to_location this card is placed.
        """
        return [Intent(
            log_entry.EntityMoveMeLogEntry,
            {},
            {
                "fromLocation": from_location,
                "card": card,
                "toLocation": to_location,
                "position": position
            }
        )]

    def special_draw_several_cards(
        cards_to_draw: int,
        to_location: "h.cardLocation"=None,
        from_location: "h.cardLocation"=None,
        shuffle_location: "h.cardLocation"=None    
    ) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityDrawCardLogEntry`, 
        forcing inclusion of key parameters. 

        Arguments:
            cards_to_draw (int): number of cards expected to be drawn.
            to_location (h.cardLocation): location where we will draw cards to. 
                If not included, will assume the default, untested, to_location of hand.
            from_location (h.cardLocation): location where we will draw cards from. 
                If not included, will assume the default, untested, from_location of draw.
            shuffle_location (h.cardLocation): location where we will shuffle from. 
                If not included, will assume the default, untested, shuffle_location of discard.
        """
        python_object_parameters = {}

        if to_location is not None:
            python_object_parameters["toLocation"] = to_location
        if from_location is not None:
            python_object_parameters["fromLocation"] = from_location
        if shuffle_location is not None:
            python_object_parameters["shuffleLocation"] = shuffle_location

        return [Intent(
            log_entry.EntityDrawCard,
            {},
            python_object_parameters
        )] * cards_to_draw

    def draw_card(
        to_location: "h.cardLocation"=None,
        from_location: "h.cardLocation"=None,
        shuffle_location: "h.cardLocation"=None
    ) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.EntityDrawCardLogEntry`, 
        forcing inclusion of key parameters (of which we have none required).

        Arguments:
            to_location (h.cardLocation): location where we will draw cards to. 
                If not included, will assume the default, untested, to_location of hand.
            from_location (h.cardLocation): location where we will draw cards from. 
                If not included, will assume the default, untested, from_location of draw.
            shuffle_location (h.cardLocation): location where we will shuffle from. 
                If not included, will assume the default, untested, shuffle_location of discard.
        """
        python_object_parameters = {}

        if to_location is not None:
            python_object_parameters["toLocation"] = to_location
        if from_location is not None:
            python_object_parameters["fromLocation"] = from_location
        if shuffle_location is not None:
            python_object_parameters["shuffleLocation"] = shuffle_location

        return [Intent(
            log_entry.EntityDrawCard,
            {},
            python_object_parameters
        )]

class HelperFactory(IntentFactory):
    def pick_living_enemy(text: str) -> list[Intent]:
        """
        Constructs an Intent for comparison against `helper.pickLivingEnemy`, 
        forcing inclusion of key parameters.

        Arguments:
            text (str): the text string that is used for the 'pick living enemy' prompt.
        """
        return [Intent(
            log_entry.HelperPickLivingEnemy,
            {},
            {"text": text}
        )]

    def yes_or_no(text: str) -> list[Intent]:
        """
        Constructs an Intent for comparison against `helper.yesOrNo`, 
        forcing inclusion of key parameters.

        Arguments:
            text (str): the text string that is used for the 'yes or no' prompt.
        """
        return [Intent(
            log_entry.HelperYesOrNoLogEntry,
            {},
            {"text": text}
        )]

class CardFunctionFactory(IntentFactory):
    def draw_until_you_have_x_cards_in_hand(draw_to_x_number: int) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.CardFunctionDrawUntilYouHaveXCardsInHand`, 
        forcing inclusion of key parameters.
        
        Arguments:
            draw_to_x_number (int): the draw to x value that is expected.
        """
        return [Intent(
            log_entry.CardFunctionDrawUntilYouHaveXCardsInHand,
            {},
            {"cardFunction.draw_to_x_number": draw_to_x_number}
        )]

    def arbitrarily_discard_card_from_location(location: "h.cardLocation", inputCard: bool) -> list[Intent]:
        """
        Constructs an Intent for comparison against `log_entry.CardFunctionArbitrarilyDiscardCardFrom_Location`, 
        forcing inclusion of key parameters.
        
        Arguments:
            location (h.cardLocation): the location we will arbitrarily discard from.
            inputCard (bool): if the inputCard parameter of this card function is True.
        """
        return [Intent(
            log_entry.CardFunctionArbitrarilyDiscardCardFrom_Location,
            {},
            {
                "cardFunction.location": location,
                "cardFunction.inputCard": inputCard
            }
        )]