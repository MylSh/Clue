"""Module sample_bot provides the "Samplebot" class, which implements
the clue AI interface
"""
from random import choice, randint
from typing import Union, Optional
from clue_game import *


class SampleBot(PlayerInterface):
    """A sample implementation of the player interface"""

    def __init__(self) -> None:
        self.player_id = None
        self.num_players = None
        self.face_up_cards = None
        self.face_down_cards = None

    def initialize(self,
                   player_id: int,
                   num_players: int,
                   face_up_cards: list[Card],
                   face_down_cards: list[Card]) -> None:
        self.player_id = player_id
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
        if randint(1, 20) == 20:
            return Accusation(who, where, what)
        else:
            return Suggestion(who, where, what)

    def respond_to_suggestion(self,
                              suggestor_id: int,
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
                                  result: Optional[Counterevidence]) -> None:
        pass

    def observe_suggestion(self,
                           suggestor_id: int,
                           suggestion: Suggestion,
                           blocker_id: Optional[int]) -> None:
        pass

    def observe_accusation(self,
                           accusor_id: int,
                           accusation: Accusation) -> None:
        pass
