import sqlite3
import random
import math

class Pokemon :
    def __init__(self, random_pokemon):
        self.pokedex_id = random_pokemon
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        self.pokemon_name, self.type1, self.type2, self.base_hp, self.base_atk, self.base_defense, self.base_spatk, self.base_spdef, self.base_speed, self.base_exp, self.exp_curve, self.min_spawn_level, self.max_spawn_level, self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed, self.evolving_level = cursor.execute("SELECT name, type_1, type_2, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed, base_experience, exp_curve, min_spawn_level, max_spawn_level, ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_speed, Evolving_level FROM Pokedex WHERE Pokedexid = ?", (random_pokemon,)).fetchall()[0]
        self.pokedex_id, ability_1, ability_2, ability_3 = cursor.execute("""SELECT Pokedexid, ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()
        abilities = [ability_1, ability_2, ability_3]
        abilities = [x for x in abilities if x is not None]
        abilities = [x for x in abilities if x]
        result = cursor.execute("""SELECT Move.MoveName, Move.pp FROM Learning JOIN Move ON Learning.Moveid = Move.Moveid WHERE Learning.Pokedexid = ?""", (self.pokedex_id,)).fetchall()
        self.all_moves = {}
        for move_name, pp in result:
            self.all_moves[move_name] = [[pp], [pp]]
        self.moves = {}
        sample_size = min(4, len(result))
        x = random.sample(sorted(result), sample_size)
        for move_name, pp in x:
            self.moves[move_name] = [[pp], [pp]]
        conn.close()
        self.ability = random.sample(abilities, 1)
        self.Level = random.randint(self.min_spawn_level, self.max_spawn_level+1)
        self.surname = ""
        self.pokemonid = 0
        self.exp = 0
        self.total_ev = 0
        self.max_exp = 0
        self.hp_ev = 0
        self.hp_iv = random.randint(1, 31)
        self.stats_ev = [0, 0, 0, 0, 0]
        self.stats_iv = [random.randint(1, 31), random.randint(1, 31), random.randint(1, 31), random.randint(1, 31), random.randint(1, 31)]
        self.hp = int(((2 * self.base_hp + self.hp_iv) * self.Level) / 100 + self.Level + 10)
        self.hp_max = int(((2 * self.base_hp + self.hp_iv) * self.Level) / 100 + self.Level + 10)
        self.atk = int(((2 * self.base_atk + self.stats_iv[0]) * self.Level) / 100 + 5)
        self.defense = int(((2 * self.base_defense + self.stats_iv[1]) * self.Level) / 100 + 5)
        self.spatk = int(((2 * self.base_spatk + self.stats_iv[2]) * self.Level) / 100 + 5)
        self.spdef = int(((2 * self.base_spdef + self.stats_iv[3]) * self.Level) / 100 + 5)
        self.speed = int(((2 * self.base_speed + self.stats_iv[4]) * self.Level) / 100 + 5)
        self.ev_defeated = [self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed]
        self.accuracy = 100
        self.dodge = 100
        self.buff_atk = 0
        self.buff_def = 0
        self.buff_spatk = 0
        self.buff_spdef = 0
        self.buff_speed = 0
        self.buff_accuracy = 0
        self.buff_dodge = 0
        
        
    def get_needed_exp(self, level, curve):
        if curve == "Fast":
            return int(0.8 * (level ** 3))
        elif curve == "Medium Fast":
            return int(level ** 3)
        elif curve == "Medium Slow":
            if int(1.2 * (level ** 3) - 15 * (level ** 2) + 100 * level - 140) < 0:
                return -1 * int(1.2 * (level ** 3) - 15 * (level ** 2) + 100 * level - 140)
            else:
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
    
    def get_hp(self):
        return self.hp
    
    def get_hp_max(self):
        return self.hp_max
    
    def get_atk(self):
        return self.atk
    
    def get_def(self):
        return self.defense
    
    def get_spatk(self):
        return self.spatk
    
    def get_spdef(self):
        return self.spdef
    
    def get_speed(self):
        return self.speed
    
    def get_accuracy(self):
        return self.accuracy
    
    def get_dodge(self):
        return self.dodge
    
    def set_hp(self, hp):
        self.hp += hp
        if self.hp < 0:
            self.hp = 0
        
    def set_atk(self, buff_atk):
        self.buff_atk = buff_atk
        if -6 > buff_atk < 6:
            self.atk = int((((2 * self.base_atk + self.stats_iv[0]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_atk))
        elif -6 < buff_atk :
            self.buff_atk = -6
            self.atk = int((((2 * self.base_atk + self.stats_iv[0]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_atk))
        else :
            self.buff_atk = 6
            self.atk = int((((2 * self.base_atk + self.stats_iv[0]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_atk))
            
    def set_def(self, buff_def):
        self.buff_def = buff_def
        if -6 > buff_def < 6:
            self.defense = int((((2 * self.base_defense + self.stats_iv[1]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_def))
        elif -6 < buff_def :
            self.buff_def = -6
            self.defense = int((((2 * self.base_defense + self.stats_iv[1]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_def))
        else :
            self.buff_def = 6
            self.defense = int((((2 * self.base_defense + self.stats_iv[1]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_def))
            
    def set_spatk(self, buff_spatk):
        self.buff_spatk = buff_spatk
        if -6 > buff_spatk < 6:
            self.spatk = int((((2 * self.base_spatk + self.stats_iv[2]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_spatk))
        elif -6 < buff_spatk :
            self.buff_spatk = -6
            self.spatk = int((((2 * self.base_spatk + self.stats_iv[2]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_spatk))
        else :
            self.buff_spatk = 6
            self.spatk = int((((2 * self.base_spatk + self.stats_iv[2]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_spatk))
            
    def set_spdef(self, buff_spdef):
        self.buff_spdef = buff_spdef
        if -6 > buff_spdef < 6:
            self.spdef = int((((2 * self.base_spdef + self.stats_iv[3]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_spdef))
        elif -6 < buff_spdef :
            self.buff_spdef = -6
            self.spdef = int((((2 * self.base_spdef + self.stats_iv[3]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_spdef))
        else :
            self.buff_spdef = 6
            self.spdef = int((((2 * self.base_spdef + self.stats_iv[3]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_spdef))
            
    def set_speed(self, buff_speed):
        self.buff_speed = buff_speed
        if -6 > buff_speed < 6:
            self.speed = int((((2 * self.base_speed + self.stats_iv[4]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_speed))
        elif -6 < buff_speed :
            self.buff_speed = -6
            self.speed = int((((2 * self.base_speed + self.stats_iv[4]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_speed))
        else :
            self.buff_speed = 6
            self.speed = int((((2 * self.base_speed + self.stats_iv[4]) * self.Level) / 100 + 5) * self.buff_stats(self.buff_speed))      
        
    def set_accuracy(self, buff_acc):
        self.buff_accuracy = buff_acc
        if -6 > buff_acc < 6:
            self.accuracy = int(100 * self.buff_stats_acc_and_dodge(self.buff_accuracy))
        elif -6 < buff_acc :
            self.buff_accuracy = -6
            self.accuracy = int(100 * self.buff_stats_acc_and_dodge(self.buff_accuracy))
        else :
            self.buff_accuracy = 6
            self.accuracy = int(100 * self.buff_stats_acc_and_dodge(self.buff_accuracy))  
            
    def set_dodge(self, buff_dodge):
        self.buff_dodge = buff_dodge
        if -6 > buff_dodge < 6:
            self.dodge = int(100 * self.buff_stats_acc_and_dodge(self.buff_dodge))
        elif -6 < buff_dodge :
            self.buff_dodge = -6
            self.dodge = int(100 * self.buff_stats_acc_and_dodge(self.buff_dodge))
        else :
            self.buff_dodge = 6
            self.dodge = int(100 * self.buff_stats_acc_and_dodge(self.buff_dodge)) 
    
    def buff_stats_acc_and_dodge(self, buff):
        if buff == -6 :
            return 0.33
        elif buff == -5 :
            return 0.38
        elif buff == -4 :
            return 0.43
        elif buff == -3 :
            return 0.5
        elif buff == -2 :
            return 0.6
        elif buff == -1 :
            return 0.75
        elif buff == 0 :
            return 1
        elif buff == 1 :
            return 1.33
        elif buff == 2 :
            return 1.67
        elif buff == 3 :
            return 2
        elif buff == 4 :
            return 2.33
        elif buff == 5 :
            return 2.67
        else :
            return 3
    
    def buff_stats(self, buff):
        if buff == -6 :
            return 0.25
        elif buff == -5 :
            return 0.29
        elif buff == -4 :
            return 0.33
        elif buff == -3 :
            return 0.4
        elif buff == -2 :
            return 0.5
        elif buff == -1 :
            return 0.67
        elif buff == 0 :
            return 1
        elif buff == 1 :
            return 1.5
        elif buff == 2 :
            return 2
        elif buff == 3 :
            return 2.5
        elif buff == 4 :
            return 3
        elif buff == 5 :
            return 3.5
        else :
            return 4
    
    def get_level(self):
        return self.Level
    
    def get_min_level(self):
        return self.min_spawn_level
    
    def get_max_level(self):
        return self.max_spawn_level
    
    def set_level(self, level):
        self.Level = level
               
    def level_up(self, level):
        self.Level += level
        
    def gain_exp(self, gain_exp, trained_multiplier, lucky_egg_multiplier, nb_pokemon, exp_charm_multiplier):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.Level < 100:
            self.exp += ((gain_exp *trained_multiplier *lucky_egg_multiplier *self.Level) / (nb_pokemon * 7)) * exp_charm_multiplier
            while self.exp >= self.max_exp:
                self.exp -= self.max_exp
                self.level_up(1)
                if self.Level == self.evolving_level :
                    self.evolve()
                if self.Level < 100:
                    self.max_exp = self.get_needed_exp(self.Level, self.exp_curve)
                else:
                    break
        cursor.execute("UPDATE Pokemon SET Level = ?, Exp = ?, Needed_exp = ?, Stat_hp = ?, Stat_attack = ?, Stat_defense = ?, Stat_spattack = ?, Stat_spdefense = ?, Stat_speed = ? WHERE Pokemonid = ?", (self.Level, int(self.exp), int(self.get_needed_exp(self.Level, self.exp_curve)), self.get_stat_hp(self.Level, self.base_hp, self.hp_ev, self.hp_iv), self.get_stat(self.Level, self.base_atk, self.stats_ev[0], self.stats_iv[0]), self.get_stat(self.Level, self.base_defense, self.stats_ev[1], self.stats_iv[1]), self.get_stat(self.Level, self.base_spatk, self.stats_ev[2], self.stats_iv[2]), self.get_stat(self.Level, self.base_spdef, self.stats_ev[3], self.stats_iv[3]), self.get_stat(self.Level, self.base_speed, self.stats_ev[4], self.stats_iv[4]), self.pokemonid))
        conn.commit()
        conn.close()
      
    def get_max_ev(self, stats_ev):
        max_ev = 510
        total = sum(stats_ev) + self.hp_ev
        if total > max_ev:
            return False
        return True

    def gain_ev(self, ev):
        max_ev = 510
        # Calculate potential new EVs
        new_hp_ev = min(self.hp_ev + ev[0], 252)
        new_stats_ev = []
        for i in range(len(self.stats_ev)):
            new_val = min(self.stats_ev[i] + ev[i+1], 252)
            new_stats_ev.append(new_val)
        # Check if total EVs exceed max
        if new_hp_ev + sum(new_stats_ev) > max_ev:
            print("EV gain exceeds maximum allowed total EVs.")
            return
        # Update EVs
        self.hp_ev = new_hp_ev
        self.stats_ev = new_stats_ev
        self.total_ev = self.hp_ev + sum(self.stats_ev)
        # Update database once
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Pokemon SET Stat_hp_ev = ?, Stat_attack_ev = ?, Stat_defense_ev = ?, Stat_spattack_ev = ?, Stat_spdefense_ev = ?, Stat_speed_ev = ?, Max_ev = ?, Stat_hp = ?, Stat_attack = ?, Stat_defense = ?, Stat_spattack = ?, Stat_spdefense = ?, Stat_speed = ? WHERE Pokemonid = ?", (self.hp_ev, self.stats_ev[0], self.stats_ev[1], self.stats_ev[2], self.stats_ev[3], self.stats_ev[4], self.total_ev, self.get_stat_hp(self.Level, self.base_hp, self.hp_ev, self.hp_iv), self.get_stat(self.Level, self.base_atk, self.stats_ev[0], self.stats_iv[0]), self.get_stat(self.Level, self.base_defense, self.stats_ev[1], self.stats_iv[1]), self.get_stat(self.Level, self.base_spatk, self.stats_ev[2], self.stats_iv[2]), self.get_stat(self.Level, self.base_spdef, self.stats_ev[3], self.stats_iv[3]), self.get_stat(self.Level, self.base_speed, self.stats_ev[4], self.stats_iv[4]), self.pokemonid))
        conn.commit()
        conn.close()
        
    def evolve(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Evolving_to FROM Pokedex WHERE Pokedexid = ?", (self.pokedex_id,))
        result = cursor.fetchone()[0]
        cursor.execute("SELECT name, Pokedexid, exp_curve, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed FROM Pokedex WHERE name = ?", (result,))
        self.pokemon_name, self.pokedex_id, self.exp_curve, self.base_hp, self.base_atk, self.base_defense, self.base_spatk, self.base_spdef, self.base_speed = cursor.fetchone()
        print(self.pokemon_name, self.pokedex_id)
        ability_1, ability_2, ability_3 = cursor.execute("""SELECT ability_1, ability_2, ability_3 FROM Pokedex WHERE name = ?""", (self.pokemon_name,)).fetchone()
        abilities = [ability_1, ability_2, ability_3]
        abilities = [x for x in abilities if x is not None]
        abilities = [x for x in abilities if x]
        self.ability = random.sample(abilities, 1)
        result = cursor.execute("""SELECT Move.MoveName, Move.pp FROM Learning JOIN Move ON Learning.Moveid = Move.Moveid WHERE Learning.Pokedexid = ?""", (self.pokedex_id,)).fetchall()
        self.all_moves = {}
        for move_name, pp in result:
            self.all_moves[move_name] = [[pp], [pp]]
        self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed = cursor.execute("SELECT ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_speed FROM Pokedex WHERE name = ?", (self.pokemon_name,)).fetchone()
        cursor.execute("UPDATE Pokemon SET Ability = ?, Needed_exp = ?, Stat_hp = ?, Stat_attack = ?, Stat_defense = ?, Stat_spattack = ?, Stat_spdefense = ?, Stat_speed = ?, Pokedexid = ?, PokemonName = ? WHERE Pokemonid = ?", (self.ability[0], self.get_needed_exp(self.Level, self.exp_curve), self.get_stat_hp(self.Level, self.base_hp, self.hp_ev, self.hp_iv), self.get_stat(self.Level, self.base_atk, self.stats_ev[0], self.stats_iv[0]), self.get_stat(self.Level, self.base_defense, self.stats_ev[1], self.stats_iv[1]), self.get_stat(self.Level, self.base_spatk, self.stats_ev[2], self.stats_iv[2]), self.get_stat(self.Level, self.base_spdef, self.stats_ev[3], self.stats_iv[3]), self.get_stat(self.Level, self.base_speed, self.stats_ev[4], self.stats_iv[4]), self.pokedex_id, self.pokemon_name, self.pokemonid))
        conn.commit()
        conn.close()
        
            
    def use_move(self, selected_move, target):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        move_type, move_power, move_accuracy, move_crit, move_effect, move_class, move_effect_chance, move_drain, move_heal, move_priority, move_max_hits, move_min_hits, move_min_turns, move_max_turns, move_buff_debuff, move_flinch = cursor.execute("SELECT type, power, accuracy, crit_rate, effect, class, effect_chance, drain, healing, priority, max_hits, min_hits, min_turns, max_turns, buff_debuff, flinch_chance FROM Move WHERE MoveName = ?", (selected_move,)).fetchone()
        if 0 > move_accuracy * self.accuracy < random.randint(1, 101):
            return
        dmg = 0
        if move_class == 'physical' and move_power > 0:
            dmg = self.get_dmg(move_power, target, move_type, move_crit, move_class)
            # if move_effect not in [None, 'None', 'None.']: # If move has an effect
            #     effect = self.get_effect(move_effect_chance, move_effect, move_buff_debuff)
        elif move_class == 'special' and move_power > 0:
            dmg = self.get_dmg(move_power, target, move_type, move_crit, move_class)
        #     if move_effect not in [None, 'None', 'None.']: # If move has an effect
        #         effect = self.get_effect(move_effect_chance, move_effect, move_buff_debuff)
        # else:
        #     effect = self.get_effect(move_effect_chance, move_effect, move_buff_debuff)
        conn.close()
        return [dmg, move_drain, move_heal, move_priority]

    def get_dmg(self, move_power, target, move_type, move_crit, move_class):
        atk = 0
        defense = 0
        if move_class == 'physical':
            atk = self.atk
            defense = target.defense
        elif move_class == 'special':
            atk = self.spatk
            defense = target.spdef
        stab = self.get_stab(move_type)
        efficacity = self.get_move_efficacity(move_type, target)
        rand = random.uniform(0.85, 1.0)
        crit = self.get_crit(move_crit)
        Mod = stab * efficacity * crit * 1 * rand
        base = math.floor((2 * self.Level) / 5) + 2
        dmg = math.floor((base * move_power * atk) / defense) / 50 + 2
        final_dmg = math.floor(dmg * Mod)
        return final_dmg
    
    # def get_effect(self, move_effect_chance, move_effect, move_buff_debuff):
    #     return
    
    def get_crit(self, move_crit):
        if move_crit == 0:
            if random.randint(1, 101) > 96:
                return (2 * self.Level + 5) / (self.Level + 5) + 0.1
        if move_crit == 1:
            if random.randint(1, 101) > 87:
                return (2 * self.Level + 5) / (self.Level + 5) + 0.5
        if move_crit == 2:
            if random.randint(1, 101) > 50 :
                return (2 * self.Level + 5) / (self.Level + 5) + 1.5
        else :
            return (2 * self.Level + 5) / (self.Level + 5) + 2
        
    def get_stab(self, move_type):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT type_1, type_2 FROM Pokedex WHERE Pokedexid = ?", (self.pokedex_id,))
        result = cursor.fetchone()
        if result[0] == move_type:
            return 1.5
        elif result[1] == move_type:
            return 1.5
        else:
            return 1
        
    def get_move_efficacity(self, move_type, target):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT type_1, type_2 FROM Pokedex WHERE Pokedexid = ?", (target.pokedex_id,))
        result = cursor.fetchone()
        move_type = move_type.capitalize()
        if result[1] is None:
            type1 = result[0].capitalize()
            cursor.execute(f" SELECT {type1} FROM Type WHERE Attacking = ? ", (move_type,))
            result = cursor.fetchone()
            return result[0]
        else :
            type1 = result[0].capitalize()
            type2 = result[1].capitalize()
            cursor.execute(f" SELECT {type1}, {type2} FROM Type WHERE Attacking = ? ", (move_type,))
            result = cursor.fetchone()
            return result[0] * result[1]
    
    def get_catch_rate(self):
        value = [0.9, 1.1]
        return int(1 * (1 + ((100 * self.Level) / 100) / 4) * ((2 - self.hp / self.hp_max) * 4) * random.choice(value) * random.randint(1, 5) * 30)
    
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
        
    def change_moves(self, userid, selected_move, new_move):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Get current moves for this Pokemon
        cursor.execute("SELECT Move1, Move2, Move3, Move4 FROM Pokemon WHERE Userid = ? AND Pokemonid = ?", (userid, self.pokemonid))
        moves = cursor.fetchone()
        if not moves:
            conn.close()
            return
        # Find which move column matches selected_move
        move_columns = ['Move1', 'Move2', 'Move3', 'Move4']
        move_to_update = None
        for i, move in enumerate(moves):
            if move == selected_move:
                move_to_update = move_columns[i]
                break
        if not move_to_update:
            conn.close()
            return
        # Update the move column to new_move
        cursor.execute(f"UPDATE Pokemon SET {move_to_update} = ? WHERE Userid = ? AND Pokemonid = ?", (new_move, userid, self.pokemonid))
        conn.commit()
        conn.close()
        # Reload moves
        self.set_attribute(userid, self.pokemonid)
