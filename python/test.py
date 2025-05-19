import sqlite3
from game_logic.Player import *
from game_logic.Pokemon import *
from game_logic.Battle import *
    
if __name__ == "__main__":
    player = Player()
    player2 = Player()
    username = "aze"
    mdp = "aze"
    player.login(username, mdp)
    username2 = "qsd"
    mdp2 = "qsd"
    player.add_pokemon(Pokemon(random.randint(1, 1319)))
    player2.login(username2, mdp2)
    player2.add_pokemon(Pokemon(random.randint(1, 1319)))
    battle = Battle(player, player2)
    print(battle.pokemon1.pokemon_name)
    print(battle.pokemon2.pokemon_name)
    moves1 = battle.pokemon_moves(1)
    moves2 = battle.pokemon_moves(2)
    mname1 = list(moves1.keys())
    mname2 = list(moves2.keys())
    data1 = battle.use_skill(1, mname1[2])
    data2 = battle.use_skill(2, mname2[2])
    print(battle.pokemon1.pokemon_name, battle.pokemon1.hp, data1)
    print(battle.pokemon2.pokemon_name, battle.pokemon2.hp, data2)
    battle.end_turn(data1, data2)
    print(battle.pokemon1.pokemon_name, battle.pokemon1.hp)
    print(battle.pokemon2.pokemon_name, battle.pokemon2.hp)
    
