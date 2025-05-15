import sqlite3
import random

class Pokemon :
    def __init__(self, random_pokemon):
        self.pokedexid = random_pokemon
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        self.pokemon_name, self.type1, self.type2, self.hp, self.atk, self.defense, self.spatk, self.spdef, self.speed = cursor.execute("SELECT name, type_1, type_2, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed FROM Pokedex WHERE Pokedexid = ?", (random_pokemon,)).fetchall()[0]
        self.pokedex_id, ability_1, ability_2, ability_3 = cursor.execute("""SELECT Pokedexid, ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()
        abilities = [ability_1, ability_2, ability_3]
        result = cursor.execute("""SELECT Move.MoveName, Move.pp FROM Learning JOIN Move ON Learning.Moveid = Move.Moveid WHERE Learning.Pokedexid = ?""", (self.pokedex_id,)).fetchall()
        self.moves = {}
        sample_size = min(4, len(result))
        x = random.sample(sorted(result), sample_size)
        for move_name, pp in x:
            self.moves[move_name] = [[pp], [pp]]
        conn.close()
        self.ability = random.sample(abilities, 1)
        self.surname = ""
        self.pokemonid = 0
        self.hpmax = self.hp
        self.base_exp = 0
        self.ev_defeated = [0, 0, 0, 0, 0, 0]
        self.exp_curve = "medium"
        self.Level = random.randint(min_spawn_level, max_spawn_level)
        self.hp_ev = 0
        self.hp_iv = random.randint(1, 31)
        self.stats_ev = [0, 0, 0, 0, 0]
        self.stats_iv = [random.randint(1, 31), random.randint(1, 31), random.randint(1, 31), random.randint(1, 31), random.randint(1, 31)]
        
    def get_needed_exp(self, level, curve):
        
    def get_stat_hp(self, level, hp, ev_hp, iv_hp):
        
    def get_stat(self, level, base_stat, ev_stat, iv_stat):
        
    def get_max_ev(self,stats_ev):
               
    def level_up(self, level):
        
    def gain_exp(self, exp, max_exp):
        
    def gain_ev(self, ev):
        
    def evolve(self, pokemon_name):
            
    def attack(self, selected_move):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        move = self.moves[selected_move]

    def get_moves(self):
        return self.moves
    
    def get_name(self):
        return self.pokemon_name
    
    def set_attribute(self, userid, pokemonid):
        self.moves = {}
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        self.pokemonid = pokemonid
        self.surname, self.ability, move1, move2, move3, move4 = cursor.execute("SELECT Surname, Ability, Move1, Move2, Move3, Move4 FROM Pokemon WHERE Userid = ? AND Pokemonid = ?", (userid, pokemonid)).fetchone()
        tmp_moves = [move1, move2, move3, move4]
        for i in range(len(tmp_moves)):
            tmp_pp = cursor.execute("SELECT pp FROM Move WHERE MoveName = ?", (tmp_moves[i],)).fetchone()[0]
            self.moves[tmp_moves[i]] = [[tmp_pp], [tmp_pp]]
        