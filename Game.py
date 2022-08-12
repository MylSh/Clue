from Cards import *
from IClueAI import *
from typing import Set, NamedTuple
import random


class Envelope(NamedTuple):
    who: Suspect
    where: Location
    what: Weapon


class PlayerInfo():
    def __init__(self, player: IClueAI, faceDownCards: list[Card]):
        self.player = player
        self.faceDownCards = faceDownCards
        self.canTakeTurns: bool = True


class Game():
    def __init__(self, players: list[IClueAI]):
        self.numPlayers: int = len(players)
        assert(self.numPlayers >= 3 and self.numPlayers <= 6)
        print("\nStarting a game of Clue with " +
              str(self.numPlayers) + " players.\n")

        random.seed()

        # divide up the card types
        suspects: list[Suspect] = [suspect for suspect in Suspect]
        random.shuffle(suspects)

        locations: list[Location] = [location for location in Location]
        random.shuffle(locations)

        weapons: list[Weapon] = [weapon for weapon in Weapon]
        random.shuffle(weapons)

        # populate the mystery envelope with a random card of each type
        self.envelope = Envelope(
            suspects.pop(), locations.pop(), weapons.pop())

        print("The final solution is: " + self.envelope.who.name + " in the " +
              self.envelope.where.name + " with the " + self.envelope.what.name + "\n")

        # now create the deck with the remainder
        deck: list[Card] = suspects + locations + weapons
        assert (len(deck) == 18)
        random.shuffle(deck)

        self.faceUpCards: list[Card] = []
        numFaceup: int = len(deck) % self.numPlayers

        for i in range(numFaceup):
            self.faceUpCards.append(deck.pop())

        assert (len(deck) % self.numPlayers == 0)

        # deal cards and initialize each player.  Also, remember what each player has.
        numCardsPerPlayer: int = int(len(deck)/self.numPlayers)
        self.playerInfos: list[PlayerInfo] = []
        for i in range(self.numPlayers):
            playerID: int = len(self.playerInfos)
            self.playerInfos.append(PlayerInfo(players[i], []))
            for j in range(numCardsPerPlayer):
                self.playerInfos[playerID].faceDownCards.append(deck.pop())
            self.playerInfos[playerID].player.initialize(playerID, self.numPlayers,
                                                         self.faceUpCards, self.playerInfos[playerID].faceDownCards)

        print("The players are:")

        for i in range(self.numPlayers):
            print("   " + str(i) + ": " +
                  self.playerInfos[i].player.name() + " (" + ', '.join([card.name for card in self.playerInfos[i].faceDownCards]) + ")")
        print()
        if(len(self.faceUpCards) == 0):
            print("There are no face up cards.\n")
        else:
            print("The face up cards are:")
            for card in self.faceUpCards:
                print("   " + card.name)
            print()

    def execute(self) -> None:
        minNumTurnsToBruteForceSolve: int = 324
        for turnNum in range(minNumTurnsToBruteForceSolve):
            for currPlayerID in range(self.numPlayers):
                playerInfo: PlayerInfo = self.playerInfos[currPlayerID]
                if(playerInfo.canTakeTurns):
                    player = playerInfo.player
                    turn: Turn = player.takeTurn()
                    if (isinstance(turn, Suggestion)):
                        print(str(currPlayerID) + ": " + player.name() + " is making a suggestion: \"" + turn.who.name +
                              " in the " + turn.where.name + " with the " + turn.what.name + ".\"")
                        blockerID: bool = None
                        for i in range(self.numPlayers-1):
                            if blockerID is not None:
                                break
                            index: int = (currPlayerID+i+1) % self.numPlayers
                            faceDownCards = self.playerInfos[index].faceDownCards
                            if(turn.who in faceDownCards or turn.where in faceDownCards or turn.what in faceDownCards):
                                print("   " + str(
                                    index) + ": " + self.playerInfos[index].player.name() + " has at least one of those cards")
                                # player has at least one card, ask them which one they'd like to show.
                                card = self.playerInfos[index].player.respondToSuggestion(
                                    currPlayerID, turn)
                                assert(card is not None)
                                self.playerInfos[currPlayerID].player.receiveSuggestionResult(
                                    turn, [index, card])
                                blockerID = index
                        if blockerID is None:
                            print("No other player had any of those cards.")
                            self.playerInfos[currPlayerID].player.receiveSuggestionResult(
                                turn, None)

                        for playerInfo in self.playerInfos:
                            playerInfo.player.observeSuggestion(
                                currPlayerID, turn, blockerID)
                    else:
                        assert(isinstance(turn, Accusation))
                        print(str(currPlayerID) + ": " + player.name() + "is making an accusation: \"" + turn.who.name +
                              " in the " + turn.where.name + " with the " + turn.what.name + ".\"")
                        if (turn.who is self.envelope.who and
                            turn.where is self.envelope.where and
                                turn.what is self.envelope.what):
                            print(str(currPlayerID) + ": " +
                                  player.name() + " has won!")
                            exit()
                        else:
                            print(str(currPlayerID) + ": " +
                                  player.name() + " was wrong.")
                            playerInfo.canTakeTurns = False
                            for playerInfo in self.playerInfos:
                                playerInfo.player.observeAccusation(
                                    currPlayerID, turn)
        print("Time's up. No one wins.")
