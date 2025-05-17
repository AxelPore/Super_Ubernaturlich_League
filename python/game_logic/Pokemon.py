import sqlite3
import random

class Pokemon :
    def __init__(self, random_pokemon):
        self.pokedex_id = random_pokemon
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        self.pokemon_name, self.type1, self.type2, self.base_hp, self.base_atk, self.base_defense, self.base_spatk, self.base_spdef, self.base_speed, self.base_exp, self.exp_curve, min_spawn_level, max_spawn_level, self.ev_hp, self.ev_atk, self.ev_def, self.ev_spatk, self.ev_spdef, self.ev_speed, self.evolving_level = cursor.execute("SELECT name, type_1, type_2, stat_hp, stat_attack, stat_defense, stat_spattack, stat_spdef, stat_speed, base_experience, exp_curve, min_spawn_level, max_spawn_level, ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_speed, Evolving_level FROM Pokedex WHERE Pokedexid = ?", (random_pokemon,)).fetchall()[0]
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
        self.Level = random.randint(min_spawn_level, max_spawn_level+1)
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
    
    def get_level(self):
        return self.Level
               
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
        
            
    def attack(self, selected_move):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        move = self.moves[selected_move]
        conn.close()

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
