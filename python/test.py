import sqlite3
from Player import *
from Game import *
    
if __name__ == "__main__":
    player = Player()
    player.add_item(26,5)
    player.add_item(25,2)
    new_game = Game()
    new_game.add_player(player)
    print(new_game.check_bag(player))

