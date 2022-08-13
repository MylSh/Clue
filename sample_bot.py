"""Module sample_bot provides the "Samplebot" class, which implements
the clue AI interface
"""
from random import choice, random, seed
from clue_game import *


class SampleBot(PlayerInterface):
    """A sample implementation of the player interface"""

    def __init__(self) -> None:
        seed(1)

    def initialize(self,
                   player_ID: int,
                   num_players: int,
                   face_up_cards: list[Card],
                   face_down_cards: list[Card]) -> None:
        self.player_ID = player_ID
        self.num_players = num_players
        self.face_up_cards = face_up_cards
        self.face_down_cards = face_down_cards

    def name(self) -> str:
        return "sample_bot"

    def take_turn(self) -> Union[Suggestion, Accusation]:
        who = choice([suspect for suspect in Suspect])
        where = choice([location for location in Location])
        what = choice([weapon for weapon in Weapon])
        # 1 in 20 chance of accusing.  Otherwise just makes a suggestion.
        if(random.random() < 0.05):
            return Accusation(who, where, what)
        else:
            return Suggestion(who, where, what)

    def respond_to_suggestion(self,
                              suggestor_ID: int,
                              suggestion: Suggestion) -> Optional[Card]:
        if(suggestion.who in self.face_down_cards):
            return suggestion.who
        elif(suggestion.where in self.face_down_cards):
            return suggestion.where
        elif(suggestion.what in self.face_down_cards):
            return suggestion.what
        else:
            return None

    def receive_suggestion_result(self,
                                  suggestion: Suggestion,
                                  blocker: Optional[Tuple[int, Card]]) -> None:
        pass

    def observeSuggestion(self,
                          suggestor_ID: int,
                          suggestion: Suggestion,
                          blocker_ID: Optional[int]) -> None:
        pass

    def observeAccusation(self,
                          accusor_ID: int,
                          accusation: Accusation) -> None:
        pass
