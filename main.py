from Game import Game
from SampleBot import SampleBot

def main():
    game:Game = Game([SampleBot(),SampleBot(),SampleBot(),SampleBot()])
    game.execute()

main()