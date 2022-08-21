from clue_game import ClueGame
from sample_bot import SampleBot


def main():
    game = ClueGame([SampleBot(),
                     SampleBot(),
                     SampleBot(),
                     SampleBot()])
    game.execute()


main()
