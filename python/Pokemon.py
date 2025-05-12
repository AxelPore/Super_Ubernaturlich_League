import sqlite3
import random

class Pokemon :
    def __init__(self, random_pokemon):
        self.pokedexid = random_pokemon
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        self.pokemon_name, self.type1, self.type2, self.hp, self.atk, self.defense, self.spatk, self.spdef, self.speed = cursor.execute("SELECT PokemonName, type_1, type_2, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdefense, stat_speed FROM Pokedex WHERE Pokedexid = ?", (random_pokemon,)).fetchone()[0]
        print("You have encountered a wild", self.pokemon_name)
        self.pokedex_id, self.ability_1, self.ability_2, self.ability_3 = cursor.execute("""SELECT Pokedexid, ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()[0]
        abilities = [a for a in [self.ability_1, self.ability_2, self.ability_3] if a and a.strip()]
        cursor.execute("""SELECT Move.MoveName FROM Learning JOIN Move ON Learning.Moveid = Move.Moveid WHERE Learning.Pokedexid = ?""", (self.pokedex_id,))
        moves = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.moves = random.sample(moves, min(4, len(moves)))
        self.ability = random.choice(abilities)
            
        