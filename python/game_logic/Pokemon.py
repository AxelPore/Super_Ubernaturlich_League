import sqlite3
import random

class Pokemon :
    def __init__(self, random_pokemon):
        self.pokedexid = random_pokemon
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        self.pokemon_name, self.type1, self.type2, self.base_hp, self.base_atk, self.base_defense, self.base_spatk, self.base_spdef, self.base_speed, self.base_exp, self.exp_curve, min_spawn_level, max_spawn_level, self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed, self.evolving_level = cursor.execute("SELECT name, type_1, type_2, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed, base_experience, exp_curve, min_spawn_level, max_spawn_level, ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_speed, Evolving_level FROM Pokedex WHERE Pokedexid = ?", (random_pokemon,)).fetchall()[0]
        self.pokedex_id, ability_1, ability_2, ability_3 = cursor.execute("""SELECT Pokedexid, ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()
        abilities = [ability_1, ability_2, ability_3]
        abilities = [x for x in abilities if x is not None]
        abilities = [x for x in abilities if x]
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
        self.exp = 0
        self.total_ev = 0
        self.max_exp = 0
        self.hp = self.base_hp
        self.hp_max = self.base_hp
        self.atk = self.base_atk
        self.defense = self.base_defense
        self.spatk = self.base_spatk
        self.spdef = self.base_spdef
        self.speed = self.base_speed
        self.ev_defeated = [self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed]
        self.Level = random.randint(min_spawn_level, max_spawn_level)
        self.hp_ev = 0
        self.hp_iv = random.randint(1, 31)
        self.stats_ev = [0, 0, 0, 0, 0]
        self.stats_iv = [random.randint(1, 31), random.randint(1, 31), random.randint(1, 31), random.randint(1, 31), random.randint(1, 31)]
        
    def get_needed_exp(self, level, curve):
        if curve == "Fast":
            return int(0.8 * (level ** 3))
        elif curve == "Medium Fast":
            return int(level ** 3)
        elif curve == "Medium Slow":
            return int(1.2 * (level ** 3) - 15 * (level ** 2) + 100 * level - 140)
        elif curve == "Slow":
            return int(1.25 * (level ** 3))
        elif curve == "Erratic":
            if level <= 50:
                return int((level ** 3) * ((100 - level) / 50))
            elif level <= 68:
                return int((level ** 3) * ((150 - level) / 100))
            elif level <= 98:
                return int((level ** 3) * ((1,274 - (1/50)) * (level / 3)))
            else:
                return int((level ** 3) * ((160 - level) / 100))
        else :
            if level <= 15:
                return int((level ** 3) * (24 * ((level + 1) / 3) / 50))
            elif level <= 35:
                return int((level ** 3) * ((14 + level) / 50))
            else :
                return int((level ** 3) * ((32 + (level / 2)) / 50))
        
    def get_stat_hp(self, level, hp, ev_hp, iv_hp):
        return int(((2 * hp + ev_hp/4 + iv_hp) * level) / 100 + level + 10)
    
    def get_stat(self, level, base_stat, ev_stat, iv_stat):
        return int(((2 * base_stat + ev_stat/4 + iv_stat) * level) / 100 + 5)
        
    def get_max_ev(self,stats_ev):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        max_ev = 510
        for i in range(len(stats_ev)):
            if self.total_ev + stats_ev[i] <= max_ev:
                self.total_ev += stats_ev[i]
            else :
                return False
        cursor.execute("UPDATE Pokemon SET Max_ev = ? WHERE Pokemonid = ?", (self.total_ev, self.pokemonid))
        conn.commit()
        conn.close()
               
    def level_up(self, level):
        self.Level += level
        
    def gain_exp(self, exp, max_exp, gain_exp, trained_multiplier, lucky_egg_multiplier, nb_pokemon, exp_charm_multiplier):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.Level < 100:
            exp += ((gain_exp *trained_multiplier *lucky_egg_multiplier *self.Level) / (nb_pokemon * 7)) * exp_charm_multiplier
            while exp >= max_exp:
                exp -= max_exp
                self.level_up(1)
                if self.Level == self.evolving_level :
                    self.evolve()
                if self.Level < 100:
                    max_exp = self.get_needed_exp(self.Level, self.exp_curve)
                else:
                    break
            cursor.execute("UPDATE Pokemon SET Level = ?, Exp = ?, Needed_exp = ?, Stat_hp = ?, Stat_attack = ?, Stat_defense = ?, Stat_spattack = ?, Stat_spdefense = ?, Stat_speed = ? WHERE Pokemonid = ?", (self.Level, self.get_needed_exp(self.Level, self.exp_curve), exp, self.get_stat_hp(self.Level, self.base_hp, self.hp_ev, self.hp_iv), self.get_stat(self.Level, self.base_atk, self.stats_ev[0], self.stats_iv[0]), self.get_stat(self.Level, self.base_defense, self.stats_ev[1], self.stats_iv[1]), self.get_stat(self.Level, self.base_spatk, self.stats_ev[2], self.stats_iv[2]), self.get_stat(self.Level, self.base_spdef, self.stats_ev[3], self.stats_iv[3]), self.get_stat(self.Level, self.base_speed, self.stats_ev[4], self.stats_iv[4]), self.pokemonid))
        conn.commit()
            
        
    def gain_ev(self, ev):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.total_ev <= 510:
            if self.hp_ev <= 252:
                self.hp_ev += ev[0]
            else :
                self.hp_ev = 252
            if self.get_max_ev(self.stats_ev) == False:
                self.hp_ev -= ev[0]
            for i in range(len(self.stats_ev)):
                if self.stats_ev[i] + ev[i+1] <= 252 :
                    self.stats_ev[i] += ev[i+1]
                else :
                    self.stats_ev[i] = 252
                if self.get_max_ev(self.stats_ev):
                    continue
                else :
                    self.stats_ev[i] -= ev[i+1]
            cursor.execute("UPDATE Pokemon SET Stat_hp_ev = ?, Stat_attack_ev = ?, Stat_defense_ev = ?, Stat_spattack_ev = ?, Stat_spdefense_ev = ?, Stat_speed_ev = ?", (self.hp_ev, self.stats_ev[0], self.stats_ev[1], self.stats_ev[2], self.stats_ev[3], self.stats_ev[4]))
                
        conn.commit()
        conn.close()
        
        
        
    def evolve(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Evolving_to FROM Pokedex WHERE Pokedexid = ?", (self.pokedex_id,))
        result = cursor.fetchone()[0]
        cursor.execute("SELECT name, Pokedexid, exp_curve, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed FROM Pokedex WHERE name = ?", (result,))
        self.pokemon_name, self.pokedex_id, self.exp_curve, self.base_hp, self.base_atk, self.base_defense, self.base_spatk, self.base_spdef, self.base_speed = cursor.fetchone()
        ability_1, ability_2, ability_3 = cursor.execute("""SELECT ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()
        abilities = [ability_1, ability_2, ability_3]
        self.ability = random.sample(abilities, 1)
        self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed = cursor.execute("SELECT ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_speed FROM Pokedex WHERE name = ?", (self.pokemon_name,)).fetchone()
        cursor.execute("UPDATE Pokemon SET Ability = ?, Needed_exp = ?, Stat_hp = ?, Stat_attack = ?, Stat_defense = ?, Stat_spattack = ?, Stat_spdefense = ?, Stat_speed = ?, Pokedexid = ? WHERE Pokemonid = ?", (self.ability, self.get_needed_exp(self.Level, self.exp_curve), self.get_stat_hp(self.Level, self.base_hp, self.hp_ev, self.hp_iv), self.get_stat(self.Level, self.base_atk, self.stats_ev[0], self.stats_iv[0]), self.get_stat(self.Level, self.base_defense, self.stats_ev[1], self.stats_iv[1]), self.get_stat(self.Level, self.base_spatk, self.stats_ev[2], self.stats_iv[2]), self.get_stat(self.Level, self.base_spdef, self.stats_ev[3], self.stats_iv[3]), self.get_stat(self.Level, self.base_speed, self.stats_ev[4], self.stats_iv[4]), self.pokedex_id, self.pokemonid))
        conn.close()
        self.hp_max = self.get_stat_hp(self.Level, self.hp, self.ev_hp, self.hp_iv)
        
            
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
        self.Level, self.exp, self.max_exp, self.hp, self.atk, self.defense, self.spatk, self.spdef, self.speed, self.hp_ev, self.stats_ev[0], self.stats_ev[1], self.stats_ev[2], self.stats_ev[3], self.stats_ev[4], self.hp_iv, self.stats_iv[0], self.stats_iv[1], self.stats_iv[2], self.stats_iv[3], self.stats_iv[4] = cursor.execute("SELECT Level, Exp, Needed_exp, Stat_hp, Stat_attack, Stat_defense, Stat_spattack, Stat_spdefense, Stat_speed, Stat_hp_ev, Stat_attack_ev, Stat_defense_ev, Stat_spattack_ev, Stat_spdefense_ev, Stat_speed_ev, Stat_hp_iv, Stat_attack_iv, Stat_defense_iv, Stat_spattack_iv, Stat_spdefense_iv, Stat_speed_iv FROM Pokemon WHERE Userid = ? AND Pokemonid = ?", (userid, self.pokemonid)).fetchone()
        self.hp_max = self.hp
        conn.close()