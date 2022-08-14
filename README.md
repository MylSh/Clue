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

**Suggestions** are used to gather information (and maybe to bluff).  A scenario is proposed (suspect, location, and weapon) by the active player.  The details of the suggestion (who, where, what) and who made the suggestion are public knowledge.  The next player will then check their facedown cards.  If one or more of their facedown cards match a card in the suggestion, they must secretly show the active player a single card, and may choose which one to reveal.  If the first checker doesn't have any cards that match, the following player will check.  Until a card is found that matches, each player (in order) will check.  If the active player becomes the checker, then the turn ends.  It is public knowledge whether or not a suggestion has been disproven (by someone providing a card that is counterevidence to the theory), and by whom.  The card used to disprove a theory is not public knowledge, and is only known by the suggestor, and the player who provided the counterevidence.

*Note: `ClueGame` will monitor the players to ensure that no-one is cheating and claiming they don't have a card when they really do.*

**Accusations** are how the game is won.  The active player proposes a scenario (suspect, location, and weapon), and then checks against the final solution in the envelope.  If the accusation is correct, the active player has won and the game is over.  If the accusation is wrong, the active player may no longer take turns.  They must still stick around to help disprove suggestions.

The game ends immediately when a player makes a correct accusation, or when all players have made incorrect accusations (because no one is left to take turns)

*Note: `ClueGame` will also end after 324 rounds of active players taking turns.  324 is the number of possible scenarios (6 suspects x 9 locations x 6 weapons = 324), and is a lower bound for a brute-force approach.  Hopefully A.I.s will be strictly better than this.*

## Getting Started

**Approaching the Problem**

Implementing a Clue A.I. is literally a textbook example of a well studied problem called the "Boolean Satisfiability Problem," or SAT.  I recommend reading something like this pdf: http://modelai.gettysburg.edu/2011/clue/clue.pdf (which heavily inspired this project).  It gives a good path from knowing essentially nothing, to having a strong background in making a Clue A.I.

**Getting your python code off the ground**

This project has a sample A.I. class named `SampleBot` found in sample_bot.py.  If you run main.py, you should see a game of clue played with `SampleBot` instances.  I would recommend copy/pasting sample_bot.py, renaming it, renaming the `SampleBot` class in the copied/renamed file and then giving it a better implementation.  To test out your new A.I., update main.py to import and create instances of your new class.

**Making your life easier**

**Source Control**
This repository is hosted on github.  Using some form of source control is strongly recommended:
eg. forking this repository so that there's a modifiable copy on your github account, cloning that modifiably branch locally to whatever machine(s) you are working on (and have git installed), and pushing changes whenever you make edits is a decent approach.  Downloading the current repository as a zip file is also an option, but then you might lose progress if the computer dies, and you won't have access to previous versions if you ever want to revert undesired changes.

**Documentation** has been provided through python docstrings.  You can open up clue_game.py and read the doc in the `PlayerInterface` class to get all of the method and parameter descriptions and pre/post conditions, but it should also nicely integrate with IDEs when implementing the subclasses.

**Unit Testing** examples for sample_bot.py have been included in sample_bot_tests.py.  I strongly recommend duplicating that file and using it ASAP to test your code(probably easiest through an IDE), and whenever possible writing tests for a method BEFORE you write the method. Test driven development is your friend.

**IDEs** (**I**ntegrated **D**evelopment **E**nvironments) make life better.  You should use one for this.  The learning curve can be high initially, but the effort will easily pay off before the end of this project.  It'll make reading, writing, running, and testing your code so much easier.  This project might even by an excuse to get farmiliar with IDE development if you aren't already.  I used Visual Studio Code as my IDE for this.

**Myles** is a friendly person.  If you have questions or run into any issues, please check in with him.
