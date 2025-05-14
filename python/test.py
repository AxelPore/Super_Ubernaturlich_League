import sqlite3
from Player import *
from Pokemon import *
    
if __name__ == "__main__":
    player = Player()
    choice = input("[00]Do you want to create a new account? (y/n): ")
    username = input("[01]Enter your username: ")
    mdp = input("Enter your password: ")
    if choice == "y":
        player.register(username, mdp, random.randint(1, 1300))
    else:
        player.login(username, mdp)
    equipe = player.get_equipe()
    for i in range(len(equipe)):
        print(f"[{i + 1}] {equipe[i].pokemon_name} ({equipe[i].get_moves()})")
    item = player.get_item()
    for i in range(len(item)):
        print(f"[{i + 1}] {item[i][0]} ({item[i][1]})")
