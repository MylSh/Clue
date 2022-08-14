"""The framework for a clue game.
Users will have to create their own Player objects that fulfill
the PlayerInterface
"""
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import NamedTuple, Optional, Union
import random


###############################################################################
# Card definitions
###############################################################################


class Suspect(IntEnum):
    """Suspects"""
    MISS_SCARLETT = 1
    COLONEL_MUSTARD = 2
    MRS_WHITE = 3
    REVEREND_GREEN = 4
    MRS_PEACOCK = 5
    PROFESSOR_PLUM = 6


class Location(IntEnum):
    """Location"""
    KITCHEN = 7
    CONSERVATORY = 8
    DINING_ROOM = 9
    BALLROOM = 10
    STUDY = 11
    HALL = 12
    LOUNGE = 13
    LIBRARY = 14
    BILLIARD_ROOM = 15


class Weapon(IntEnum):
    """Weapons"""
    REVOLVER = 16
    DAGGER = 17
    LEAD_PIPE = 18
    ROPE = 19
    CANDLESTICK = 20
    WRENCH = 21


Card = Union[Suspect, Weapon, Location]


###############################################################################
# Scenario definitions
###############################################################################

class Scenario(NamedTuple):
    """A possible crime scenario.
    Combination of who, where, and with what.

    Members:
    who: A Suspect card.
    where: A Location card.
    what: A Weapon card.
    """
    who: Suspect
    where: Location
    what: Weapon

    def __str__(self) -> str:
        return (self.who.name + " in the " +
                self.where.name + " with the "
                + self.what.name)


class Suggestion(Scenario):
    """A suggestion"""


class Accusation(Scenario):
    """An accusation"""


class Counterevidence(NamedTuple):
    """Information that disproves a Suggestion.

    Members:
    refuter_id: The id of the player who provided the evidence.
    evidence: the card that disproves the Suggestion
    """
    refuter_id: int
    evidence: Card


###############################################################################
# Player Interface
###############################################################################


class PlayerInterface(ABC):
    """An interface to create player objects.  Not meant to be instantiated
    directly.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Constructor is essentially a no-op.
        Initialization is delayed to the self.initialize() method.
        """
        raise NotImplemented

    @abstractmethod
    def initialize(self,
                   player_id: int,
                   num_players: int,
                   face_up_cards: list[Card],
                   face_down_cards: list[Card]) -> None:
        """Method to lazily initialize the object.

        Preconditions:
        player_id: 0<=player_id<num_players
        num_players: 3<=num_players<=6

        Parameters:
        player_id: The absolete position of self in the game.
        num_players: The number of players in the game.
        face_up_cards: The cards that are face up and known to all players.
        face_down_cards: The cards that are only known to self.
        """
        raise NotImplemented

    @abstractmethod
    def name(self) -> str:
        """Returns the name of the current player.

        Returns:
        Name of current player.
        """
        raise NotImplemented

    @abstractmethod
    def take_turn(self) -> Union[Suggestion, Accusation]:
        """Returns either a Suggestion, or an Accusation.

        Returns:
        Either a Suggestion, or an Accusation.
        """
        raise NotImplemented

    @abstractmethod
    def respond_to_suggestion(self,
                              suggestor_id: int,
                              suggestion: Suggestion) -> Optional[Card]:
        """Returns a card in the intersection of the Suggestion and the
        facedown cards of self.

        Preconditions:
        self: self.initialize() has already been called.
        suggestor_id: 0 <= suggestor_id < numPlayers

        Parameters:
        suggestor_id:  The absolute position of the player who made the
        suggestion.
        suggestion: A Suspect, a Location, and a Weapon card.

        Returns: A card that is in the intersection of the suggestion,
        and the facedown cards of self. If not such intersection exists,
        returns `None`.
        """
        raise NotImplemented

    @abstractmethod
    def receive_suggestion_result(self,
                                  suggestion: Suggestion,
                                  result: Optional[Counterevidence]) -> None:
        """Receives information about the suggestion that was previously made
        by the current player. Expected to be called immediately after a
        Suggestion was returned by "takeTurn()"

        Preconditions:
        self: self.initialize() has already been called.

        Parameters:
        suggestion: A Suspect, a Location, and a Weapon card.
        result: Either one of the cards in the suggestion, along with the
        index of the player who has that card, or None. If it's a card and
        player index, than no player between self and that player index
        (incrementing, and wrapping around at numPlayers to 0) has any of
        the cards in suggestion. If it's None, then no other player has any
        of the cards in suggestion.
        """
        raise NotImplemented

    @abstractmethod
    def observe_suggestion(self,
                           suggestor_id: int,
                           suggestion: Suggestion,
                           blocker_id: Optional[int]) -> None:
        """Used to observe a turn where a bot made a suggestion.

        Preconditions:
        self: self.initialize() has already been called.
        suggestor_id: 0 <= suggestor_id < numPlayers
        blocker_id: 0 <= blocker_id < numPlayers or blockerID is None

        Parameters:
        suggestor_id: The absolute position of the player who made the
        suggestion.
        suggestion: A Suspect, a Location, and a Weapon card.
        blocker_id: The absolute position of the player who has a card
        that blocked the suggestion.
        If no non-suggesting player could block it, then a value of
        `None` will be used.
        """
        raise NotImplemented

    @abstractmethod
    def observe_accusation(self,
                           accusor_id: int,
                           accusation: Accusation) -> None:
        """Used to observe a turn where a bot made an accusation.
        This will only ever be called if the accusation is wrong.
        Otherwise the game would already be over.

        Preconditions:
        self: self.initialize() has already been called.
        accusor_id: 0 <= accusor_id < numPlayers

        Parameters:
        accusor_id: The absolute position of the player who made the
        accusation.
        accusation:  A Suspect, a Location, and a Weapon card.
        """
        raise NotImplemented

###############################################################################
# Game object
###############################################################################


class ClueGame():
    """An object to manage a game of Clue.  It will shuffle and distribute
    cards, ensure everyone gets their cards, confirm no one is cheating,
    and make sure information is shared when appropriate.  It will also
    document the game by logging relevant information to the output.
    """

    class __PlayerInfo():
        """A helper struct with relevant player info for the ClueGame class.
        Used to verify that players aren't cheating, and whether or not they
        can still take turns.

        Members:
        player: A player object.
        face_down_cards: A copy of the facedown cards that the player has.
        can_take_turns: Whether the current player can continue to take turns,
        or whether they have made an incorrect accusation and can only sit and
        respond to suggestions.
        """

        def __init__(self,
                     player: PlayerInterface,
                     face_down_cards: list[Card]):
            self.player = player
            self.face_down_cards = face_down_cards
            self.can_take_turns: bool = True

    def __init__(self,
                 players: list[PlayerInterface]):
        """Constructs the ClueGame object.  Shuffles and deals the cards.

        Preconditions:
        players: 3 <= len(players) <= 6

        Parameters:
        players: The players that will participate in this game.
        """
        self.num_players: int = len(players)
        assert(self.num_players >= 3 and self.num_players <= 6)
        print("\nStarting a game of Clue with " +
              str(self.num_players) + " players.\n")

        random.seed()

        # divide up the card types
        suspects: list[Suspect] = [suspect for suspect in Suspect]
        random.shuffle(suspects)

        locations: list[Location] = [location for location in Location]
        random.shuffle(locations)

        weapons: list[Weapon] = [weapon for weapon in Weapon]
        random.shuffle(weapons)

        # populate the mystery envelope with a random card of each type
        self.envelope = Scenario(suspects.pop(),
                                 locations.pop(),
                                 weapons.pop())

        print("The final solution is: " +
              str(self.envelope) + "\n")

        # now create the deck with the remainder
        deck: list[Card] = suspects + locations + weapons
        assert len(deck) == 18
        random.shuffle(deck)

        self.face_up_cards: list[Card] = []
        num_faceup_cards = int(len(deck) % self.num_players)

        for i in range(num_faceup_cards):
            self.face_up_cards.append(deck.pop())

        assert len(deck) % self.num_players == 0

        # Deal cards and initialize each player.
        # Also, remember what each player has.
        print("The players are:")
        num_cards_per_player = int(len(deck)/self.num_players)
        self.player_infos: list[self.__PlayerInfo] = []
        for i in range(self.num_players):
            player_id: int = len(self.player_infos)
            face_down_cards: list[Card] = []
            for _ in range(num_cards_per_player):
                face_down_cards.append(deck.pop())
            self.player_infos.append(self.__PlayerInfo(players[i],
                                                       face_down_cards))
            player_info = self.player_infos[player_id]
            player_info.player.initialize(player_id, self.num_players,
                                          self.face_up_cards,
                                          player_info.face_down_cards)
            player_name: str = (str(player_id) + ": " +
                                player_info.player.name())
            player_cards: str = (', '.join([card.name for card
                                            in face_down_cards]))
            print("   " + player_name + "(" + player_cards + ")")
        print()
        if len(self.face_up_cards) == 0:
            print("There are no face up cards.\n")
        else:
            print("The face up cards are:")
            for card in self.face_up_cards:
                print("   " + card.name)
            print()

    def __handleSuggestion(self,
                           suggestor_id: int,
                           suggestion: Suggestion) -> None:
        """Handle a Suggestion made by the player at suggestor_id.

        Preconditions:
        suggestor_id: 0 <= suggestor_id <= self.num_players

        Parameters:
        suggestor_id: The id of the player that made the suggestion.
        suggestion: The Suggestion made by the player.
        """
        suggestor = self.player_infos[suggestor_id].player
        suggestor_name = (str(suggestor_id) + ": " + suggestor.name())
        print(suggestor_name + " is making a suggestion: \"" +
              str(suggestion) + ".\"")

        # Go around the table and see if any of the other players
        # can block this suggestion.
        blocker_id: int = None
        for i in range(self.num_players-1):
            maybe_blocker_id: int = (suggestor_id + i + 1) % self.num_players
            maybe_blocker_info = self.player_infos[maybe_blocker_id]
            maybe_blocker = maybe_blocker_info.player
            maybe_blockers_cards = maybe_blocker_info.face_down_cards

            if (suggestion.who in maybe_blockers_cards
                    or suggestion.where in maybe_blockers_cards
                    or suggestion.what in maybe_blockers_cards):
                blocker_id = maybe_blocker_id
                blocker = maybe_blocker
                print("    " + str(blocker_id) + ": " + blocker.name() +
                      " has at least one of those cards")
                # Blocker has at least one card.
                # Ask them which they'd like to show.
                card = blocker.respond_to_suggestion(suggestor_id, suggestion)
                assert card is not None
                result = Counterevidence(blocker_id, card)
                suggestor.receive_suggestion_result(suggestion, result)
                break
        if blocker_id is None:
            print("    No other player had any of those cards.")
            suggestor.receive_suggestion_result(suggestion, None)

        for player_info in self.player_infos:
            player_info.player.observe_suggestion(suggestor,
                                                  suggestion,
                                                  blocker_id)

    def __handleAccusation(self,
                           accusor_id: int,
                           accusation: Accusation) -> bool:
        """Handle an Accusation made by the player at accusor_id.
        If they are correct, the game is over.

        Preconditions:
        accusor_id: 0 <= accusor_id <= self.num_players

        Parameters:
        accusor_id: The id of the player that made the suggestion.
        accusation: The Accusation made by the player.

        Returns:
        Returns whether the game is over.
        """
        accusor = self.player_infos[accusor_id].player
        accusor_name = (str(accusor_id) + ": " + accusor.name())
        print(accusor_name + " is making an accusation: \"" +
              str(accusation) + ".\"")
        if(accusation.who is self.envelope.who
           and accusation.where is self.envelope.where
           and accusation.what is self.envelope.what):
            print("    " + accusor_name + " has won!")
            return True
        else:
            print("    " + accusor_name + " was wrong.")
            self.player_infos[accusor_id].can_take_turns = False
            active_player_exists = False
            for player_info in self.player_infos:
                player_info.player.observe_accusation(accusor_id, accusation)
                if player_info.can_take_turns:
                    active_player_exists = True
            if active_player_exists:
                return False
            print("All players were eliminated.")

    def __giveTurn(self,
                   player_id: int) -> bool:
        """ Give a turn to the player at the specified index.
        If they make a correct accusation, the game is over.

        Preconditions:
        player_id: 0 <= player_id <= self.num_players
        and self.player_infos[player_id].canTakeTurns

        Parameters:
        player_id: The id of the player that should take a turn

        Returns:
        Returns whether the game is over.
        """
        assert self.player_infos[player_id].can_take_turns

        player = self.player_infos[player_id].player
        scenario = player.take_turn()
        if isinstance(scenario, Suggestion):
            self.__handleSuggestion(player_id, scenario)
            return False
        else:
            assert isinstance(scenario, Accusation)
            return self.__handleAccusation(player_id, scenario)

    def execute(self) -> None:
        """The main method of the ClueGame class.
        This method gets all of the players to take turns and share relevant
        information.
        """
        number_of_possible_solutions: int = 324
        for _ in range(number_of_possible_solutions):
            for player_id in range(self.num_players):
                if self.player_infos[player_id].can_take_turns:
                    gameIsOver = self.__giveTurn(player_id)
                    if gameIsOver:
                        exit()
        print("Time's up. No one wins.")
