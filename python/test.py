import sqlite3
from Player import *
    
if __name__ == "__main__":
    player = Player()
    username = input("[01]Enter your username: ")
    mdp = input("Enter your password: ")
    starter = random.randint(1, 1300)
    player.login(username, mdp)

