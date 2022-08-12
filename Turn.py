from Cards import *


class Turn():
    def __init__(self, who: Suspect, where: Location, what: Weapon, ):
        self.who = who
        self.where = where
        self.what = what


class Suggestion(Turn):
    pass


class Accusation(Turn):
    pass
