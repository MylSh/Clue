# Clue
This is python framework to build and test Clue A.I.s by extending the `PlayerInterface` class in clue_game.py.  

A crime has been committed in the Clue Mansion.  Someone has been killed somewhere with something.  A.I.s race to determine the suspect, location, and weapon.

The `ClueGame` class (found in clue_game.py) takes a list of A.I. objects, and then runs a game of clue with them.  It will print all relevant information, so that humans can watch.  A sample A.I., `SampleBot`, has been provided in sample_bot.py.


## Game Rules

Each game is played by 3-6 players

The game has exactly 21 unique cards divided into 3 categories:
  - 6 Suspects:
     - Colonel Mustard
     - Miss Scarlet
     - Mrs Peacock
     - Mrs White
     - Professor Plum
     - Reverend Green
  - 9 Locations:
     - Ballroom
     - Billiard Room
     - Conservatory
     - Dining Room
     - Hall
     - Kitchen
     - Lounge
     - Library
     - Study
  - 6 Weapons:
     - Candlestick
     - Dagger
     - Lead Pipe
     - Revolver
     - Rope
     - Spanner

At the start of the game a single card from each of the categories will be randomly selected.  This set of 3 cards (1 suspect, 1 location, and 1 weapon) is the final solution that the players must deduce, and is placed in an envelope.  The remaining cards are shuffled together to form a single deck of 18 cards.  Each of those 18 cards is guaranteed to NOT be part of the final solution.  Those cards are dealt to the players facedown and are hidden information.  If the number of cards does not evenly divide amongst the players, then the remaining modulo is placed faceup, and is known to all players.

A player sequence is determined (eg. clockwise), and players then take turns sequentially.  On a turn, a player may make a suggestion, or an accusation.

A **suggestion** is used to gather information (and maybe to bluff).  A scenario is publicly proposed (suspect, location, and weapon) by the active player.  The next player sequentially will then check their facedown cards.  If one or more of their facedown cards match a card in the suggestion, they must secretly show the active player a single card, and may choose which one to reveal.  If the first checker doesn't have any cards that match, the following player will check.  Until a card is found that matches, each player sequentially will check.  If the active player becomes the checker, then the turn ends.  It is public knowledge whether or not a suggestion has been disproven (by someone providing a card that is counterevidence to the theory), and by whom.  The card used to disprove a theory is not public knowledge, and is only known by the suggestor, and the player who provided the counterevidence.
*Note: `ClueGame` will monitor the players to ensure that no-one is cheating and claiming they don't have a card when they really do.*

An **accusation** is how the game is won.  It consists of proposing a scenario (suspect, location, and weapon), and then checking against the final solution in the envelope.  If the accusation is correct, that player has won and the game is over.  If the accusation is wrong, that player may no longer take turns.  They must still stick around to help refute suggestions.

The game ends immediately when a player makes a correct accusation, all players have made incorrect accusations (because no one is left to take turns), or when the game has reached 324 rounds.  324 is the number of possible scenarios (6 suspects x 9 locations x 6 weapons = 324), and is a lower bound for a brute-force approach.  Hopefully players will do better than this.


