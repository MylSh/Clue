import abc
from typing import Optional, Tuple
from Cards import *
from Turn import *


class IClueAI:
    # constructor.  Majority of work is delay initialized
    def __init__(self) -> None:
        pass

    # numPlayers: the total number of players in the game
    # PRECOND: 3<=numPlayers<=6
    # playerID: The absolute position of the current player at the table.  0-based counting
    # PRECOND: 0<=player<numPlayers
    # faceUpCards are cards that are face up and known to all players
    # faceDownCards are cards that are only known to the current player
    def initialize(self, playerID: int, numPlayers: int, faceUpCards: list[Card], faceDownCards: list[Card]) -> None:
        pass


    # Give name of current player
    def name(self) -> str:
        pass

    # Returns a Turn object, which can be either a Suggestion or an Accusation
    def takeTurn(self) -> Turn:
        pass

    # Returns a card is in the intersection of the Suggestion (person, place, and thing) and the facedown cards of the current player.
    # If no such card exists, then `None` will be returned.
    # suggestorID is the absolute position of the player who made the suggestion.  0-based counting
    # PRECOND: 0<=suggestorID<numPlayers
    # PRECOND: suggestorID!= current player ID
    # POSTCOND: return value is in the intersection of the Suggestion (person, place, and thing) and the facedown cards, or is `None`
    def respondToSuggestion(self, suggestorID: int, suggestion:Suggestion) -> Optional[Card]:
        pass

   # Receives information about the suggestion that was previously made by the current player.  Expected to be called immediately after
   # a Suggestion was returned by "takeTurn()"
    def observe(self, suggestion: Suggestion, blocker: Optional[Tuple[int, Card]]) -> None:
        pass

   # suggestorID is the absolute position of the player who made the suggestion.  0-based counting
   # PRECOND: 0<=suggestorID<numPlayers
   # blockerID is the absolute position of the player who has a card that blocked the suggestion.  0-based counting.
   #   If no non-suggesting player could block it, then a value of `None` will be used
   # PRECOND: 0<=blockerID<numPlayers  OR blockerID==sentinelValue
    def observe(self, suggestorID: int, suggestion: Suggestion, blockerID: Optional[int]) -> None:
        pass

   # accusorIDis the absolute position of the player who made the suggestion.  0-based counting
   # PRECOND: 0<=accusorID<numPlayers
   # This will only ever be called if the accusation is wrong.  Otherwise the game would already be over.
    def observe(self, accusorID: int, accusation: Accusation) -> None:
        pass
