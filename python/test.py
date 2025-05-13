import sqlite3
from Player import *
from Pokemon import *
    
if __name__ == "__main__":
    player = Player()
    username = input("[01]Enter your username: ")
    mdp = input("Enter your password: ")
    for i in range(3):
        starter = random.randint(1, 1300)
        tmp_poke = Pokemon(starter)
        player.add_pokemon(tmp_poke)
    player.login(username, mdp)

