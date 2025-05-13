import sqlite3
import random

class Pokemon :
    def __init__(self, random_pokemon):
        self.pokedexid = random_pokemon
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        print("Pokedexid: ", self.pokedexid)
        self.pokemon_name, self.type1, self.type2, self.hp, self.atk, self.defense, self.spatk, self.spdef, self.speed = cursor.execute("SELECT name, type_1, type_2, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed FROM Pokedex WHERE Pokedexid = ?", (random_pokemon,)).fetchall()[0]
        self.pokedex_id, ability_1, ability_2, ability_3 = cursor.execute("""SELECT Pokedexid, ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()
        abilities = [ability_1, ability_2, ability_3]
        result = cursor.execute("""SELECT Move.MoveName, Move.pp FROM Learning JOIN Move ON Learning.Moveid = Move.Moveid WHERE Learning.Pokedexid = ?""", (self.pokedex_id,)).fetchall()
        self.moves = {}
        x = random.sample(range(len(result)), 4)
        for i in x:
            self.moves[result[i][0]] = [[result[i][1]], [result[i][1]]]
        conn.close()
        self.ability = random.sample(abilities, 1)
        self.surname = ""
        self.pokemonid = 0
        self.hpmax = self.hp
            
    def attack(self, selected_move):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        move = self.moves[selected_move]

    def get_moves(self):
        return self.moves
    
    def set_attribute(self, userid):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        self.pokemonid, self.surname, self.ability, move1, move2, move3, move4 = cursor.execute("SELECT Pokemonid, Surname, Ability, Move1, Move2, Move3, Move4 FROM Pokemon WHERE Userid = ?", (userid,)).fetchone()[0]
        tmp_moves = [move1, move2, move3, move4]
        for i in range(len(tmp_moves)):
            tmp_pp = cursor.execute("SELECT pp FROM Move WHERE MoveName = ?", (tmp_moves[i],)).fetchone()[0]
            self.moves[tmp_moves[i]] = [[tmp_pp], [tmp_pp]]
        