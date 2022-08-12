from enum import IntEnum
from typing import Union
import random


class Suspect(IntEnum):
    MISS_SCARLETT = 1
    COLONEL_MUSTARD = 2
    MRS_WHITE = 3
    REVEREND_GREEN = 4
    MRS_PEACOCK = 5
    PROFESSOR_PLUM = 6


class Weapon(IntEnum):
    REVOLVER = 7
    DAGGER = 8
    LEAD_PIPE = 9
    ROPE = 10
    CANDLESTICK = 11
    WRENCH = 12


class Location(IntEnum):
    KITCHEN = 13
    CONSERVATORY = 14
    DINING_ROOM = 15
    BALLROOM = 16
    STUDY = 17
    HALL = 18
    LOUNGE = 19
    LIBRARY = 20
    BILLIARD_ROOM = 21


Card = Union[Suspect, Weapon, Location]
