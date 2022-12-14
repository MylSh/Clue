# Clue
This is a python 3.10 framework to build and test Clue A.I.s by extending the `PlayerInterface` class in clue_game.py.

A crime has been committed in the Clue Mansion.  Someone has been killed somewhere with something.  A.I.s race to determine the suspect, location, and weapon.

The `ClueGame` class (found in clue_game.py) takes a list of A.I. objects, and then runs a game of clue with them.  It will print all relevant information, so that humans can watch.  A sample A.I., `SampleBot`, has been provided in sample_bot.py.

## Sample Output
When run, the ClueGame class will log the progress of the game.  Eg.
```
Starting a game of Clue with 4 players.

The final solution is: COLONEL_MUSTARD in the DINING_ROOM with the CANDLESTICK

The players are:
   0: sample_bot(SPANNER, LIBRARY, MISS_SCARLETT, BALLROOM)
   1: sample_bot(LOUNGE, HALL, KITCHEN, LEAD_PIPE)
   2: sample_bot(MRS_WHITE, ROPE, REVEREND_GREEN, MRS_PEACOCK)
   3: full_bot(REVOLVER, STUDY, DAGGER, CONSERVATORY)

The face up cards are:
   BILLIARD_ROOM
   PROFESSOR_PLUM

==============================================================================================
Round #0
==============================================================================================
0: sample_bot is making a suggestion: "MRS_PEACOCK in the BALLROOM with the LEAD_PIPE."
    1: sample_bot disproved this by secretly showing LEAD_PIPE.
1: sample_bot is making a suggestion: "MRS_PEACOCK in the KITCHEN with the ROPE."
    2: sample_bot disproved this by secretly showing MRS_PEACOCK.
2: sample_bot is making a suggestion: "MRS_WHITE in the HALL with the LEAD_PIPE."
    1: sample_bot disproved this by secretly showing HALL.
3: full_bot is making a suggestion: "COLONEL_MUSTARD in the BALLROOM with the CANDLESTICK."
    0: sample_bot disproved this by secretly showing BALLROOM.
==============================================================================================
Round #1
==============================================================================================
0: sample_bot is making a suggestion: "PROFESSOR_PLUM in the LOUNGE with the CANDLESTICK."
    1: sample_bot disproved this by secretly showing LOUNGE.
1: sample_bot is making a suggestion: "MRS_WHITE in the BALLROOM with the DAGGER."
    2: sample_bot disproved this by secretly showing MRS_WHITE.
2: sample_bot is making a suggestion: "MRS_WHITE in the DINING_ROOM with the SPANNER."
    0: sample_bot disproved this by secretly showing SPANNER.
3: full_bot is making a suggestion: "COLONEL_MUSTARD in the DINING_ROOM with the CANDLESTICK."
    No other player had any of those cards.
==============================================================================================
Round #2
==============================================================================================
0: sample_bot is making a suggestion: "MISS_SCARLETT in the CONSERVATORY with the ROPE."
    2: sample_bot disproved this by secretly showing ROPE.
1: sample_bot is making a suggestion: "MISS_SCARLETT in the HALL with the REVOLVER."
    3: full_bot disproved this by secretly showing REVOLVER.
2: sample_bot is making a suggestion: "REVEREND_GREEN in the LOUNGE with the ROPE."
    1: sample_bot disproved this by secretly showing LOUNGE.
3: full_bot is making an accusation: "COLONEL_MUSTARD in the DINING_ROOM with the CANDLESTICK."
    3: full_bot has won!
```

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

*Note: Each category of card is represented as an enum in clue_game.py: `Suspect`, `Location` and `Weapon`. `Card` is a union of the three enums.  The category of a card can be checked by using `in` eg. `if card in Suspect... elif card in Location ... else assert card in Weapon ...`
`Card.name` returns the human readible title of the card.  `Card.value` returns a strictly positive integer that is unique for each card.*

At the start of the game a single card from each of the categories will be randomly selected.  This set of 3 cards (1 suspect, 1 location, and 1 weapon) is the final solution that the players must deduce, and is placed in an envelope.  The remaining cards are shuffled together to form a single deck of 18 cards.  Each of those 18 cards is guaranteed to NOT be part of the final solution.  Those cards are dealt to the players facedown and are hidden information.  If the number of cards does not evenly divide amongst the players, then the remaining modulo is placed faceup, and is known to all players.

A player sequence is determined (eg. clockwise), and players then take turns sequentially.  On a turn, a player may make a suggestion, or an accusation.

**Suggestions** are used to gather information (and maybe to bluff).  A scenario is publicly proposed (suspect, location, and weapon) by the active player.  The next player will then check their facedown cards.  If one or more of their facedown cards match a card in the suggestion, they must secretly show the active player one of the matching cards.  If they have more than one matching cards, they may choose which one to reveal.  If the first checker doesn't have any cards that match, the following player will check.  Until a card is found that matches, each player (in order) will check.  The active player never publicly checks their own suggestion. If every other player has checked without finding a matching card, then the turn ends.  It is public knowledge who makes each suggestion, the contents of the suggestion, whether or not the suggestion has been disproven (by someone providing a card that is counterevidence to the theory), and by whom.  The card used to disprove a theory is not public knowledge, and is only known by the suggestor, and the player who provided the counterevidence.

*Note: `ClueGame` will monitor the A.I.s to ensure that none of them cheats and claims they don't have a card when they really do.*

**Accusations** are how the game is won.  The active player proposes a scenario (suspect, location, and weapon), and then checks against the final solution in the envelope.  If the accusation is correct, the active player has won and the game is over.  If the accusation is wrong, the active player may no longer take turns.  They must still stick around to help disprove suggestions.

The game ends immediately when a player makes a correct accusation, or when all players have made incorrect accusations (because no one is left to take turns)

*Note: `ClueGame` will also end after 324 rounds of active players taking turns.  324 is the number of possible scenarios (6 suspects x 9 locations x 6 weapons = 324), and is a lower bound for a brute-force approach.  Hopefully A.I.s will be strictly better than this.*

## Getting Started

**Approaching the problem**

There is no right answer here, but I'll give one possible path.  Keeping track of where each card definitely isn't, and then looking at where it must therefore be will get you pretty far.  If you then want to take the next step and keep track of what each card might be based on who blocked which suggestion, the "Boolean Satisfiability Problem" also called "SAT" might be helpful to learn about.  This pdf gives a good path from knowing essentially nothing, to understanding the SAT problem in the context of Clue A.I.s: http://modelai.gettysburg.edu/2011/clue/clue.pdf (and heavily inspired this project).  

**Getting your python code off the ground**

This project has a sample A.I. class named `SampleBot` found in sample_bot.py.  If you run main.py, you should see a game of clue played with `SampleBot` instances.  I would recommend copy/pasting sample_bot.py, renaming it, renaming the `SampleBot` class in the copied/renamed file and then giving it a better implementation.  To test out your new A.I., update main.py to import and create instances of your new class.

**Making your life easier**

**Source Control** is useful.  This repository is hosted on github.  Using some form of source control is strongly recommended:
eg. forking this repository so that there's a modifiable copy on your github account, cloning that modifiably branch locally to whatever machine(s) you are working on (and have git installed), and pushing changes whenever you make edits is a decent approach.  Downloading the current repository as a zip file is also an option, but then you might lose progress if the computer dies, and you won't have access to previous versions if you ever want to revert undesired changes.

**Documentation** has been provided through python docstrings.  You can open up clue_game.py and read the doc in the `PlayerInterface` class to get all of the method and parameter descriptions and pre/post conditions, but it should also nicely integrate with IDEs when implementing the subclasses.

**Unit Testing** examples for sample_bot.py have been included in sample_bot_tests.py.  I strongly recommend duplicating that file and using it ASAP to test your code(probably easiest through an IDE), and whenever possible writing tests for a method BEFORE you write the method. Test driven development is your friend.

**IDEs** (**I**ntegrated **D**evelopment **E**nvironments) make life better.  You should use one for this.  The learning curve can be high initially, but the effort will easily pay off before the end of this project.  It'll make reading, writing, running, and testing your code so much easier.  This project might even by an excuse to get farmiliar with IDE development if you aren't already.  I used Visual Studio Code as my IDE for this.

**Myles** is a friendly person.  If you have questions or run into any issues, please check in with him.
