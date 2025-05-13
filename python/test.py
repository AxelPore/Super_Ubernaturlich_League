import sqlite3
import Player
    
if __name__ == "__main__":
    player = Player()
    username = input("[01]Enter your username: ")
    mdp = input("Enter your password: ")
    starter = 1
    player.register(username, mdp, starter)
    player.login(username, mdp)

