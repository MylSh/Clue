from Game import Game
from RandomBot import RandomBot

def main():
    game:Game = Game([RandomBot(),RandomBot(),RandomBot(),RandomBot()])
    game.execute()

main()