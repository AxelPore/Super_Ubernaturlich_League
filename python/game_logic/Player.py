import aiosqlite
from .Pokemon import *

class Player:
    def __init__(self):
        self.username = ""
        self.userid = 0
        self.equipeid = 0
        self.equipe = []
        self.pokemon = []
        self.item = [[]]
        self.zoneid = 0
        self.zone = 0
        self.money = 0
        self.zonename = ""

    async def login(self, username, mdp):
        async with aiosqlite.connect('database.db') as conn:
            cursor = await conn.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, mdp))
            result = await cursor.fetchone()
            if result is None:
                return False
            self.username = username
            self.userid = result[0]
            self.equipeid = result[3]
            self.money = result[5]
            self.zoneid = result[4]
            pc_cursor = await conn.execute("SELECT Pokedexid, Pokemonid FROM Pokemon WHERE Userid = ?", (self.userid,))
            pc = await pc_cursor.fetchall()
            self.pokemon.clear()
            for i in pc:
                tmp_poke = Pokemon(i[0])
                tmp_poke.set_attribute(self.userid, i[1])
                self.pokemon.append(tmp_poke)
            tmp_equipe_cursor = await conn.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,))
            tmp_equipe = await tmp_equipe_cursor.fetchone()
            self.equipe.clear()
            for j in tmp_equipe:
                for k in self.pokemon:
                    if k.pokemonid == j:
                        self.equipe.append(k)
                        self.pokemon.remove(k)
            item_cursor = await conn.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,))
            self.item = await item_cursor.fetchall()
            zone_cursor = await conn.execute("SELECT ZonePosition, ZoneName FROM Zone WHERE Zoneid = ?", (result[4],))
            self.zone, self.zonename = await zone_cursor.fetchone()
            return True

    async def register(self, username, mdp, starter_pokemon):
        async with aiosqlite.connect('database.db') as conn:
            await conn.execute("INSERT INTO User (username, password, Zoneid) VALUES (?, ?, ?)", (username, mdp, 14))
            self.userid = conn.last_insert_rowid()
            await conn.commit()
            first_pokemon = Pokemon(starter_pokemon)
            moves = []
            for i in first_pokemon.moves.items():
                moves.append(i)
            pokedexid = int(first_pokemon.pokedex_id)
            await conn.execute("INSERT INTO Pokemon (PokemonName, Userid, Ability, Move1, Move2, Move3, Move4, Pokedexid, Level, Exp, Needed_exp, Stat_hp, Stat_attack, Stat_defense, Stat_spattack, Stat_spdefense, Stat_speed, Stat_hp_ev, Stat_attack_ev, Stat_defense_ev, Stat_spattack_ev, Stat_spdefense_ev, Stat_speed_ev, Max_ev, Stat_hp_iv , Stat_attack_iv, Stat_defense_iv, Stat_spattack_iv, Stat_spdefense_iv, Stat_speed_iv) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_pokemon.pokemon_name, self.userid, first_pokemon.ability[0], moves[0][0], moves[1][0], moves[2][0], moves[3][0], pokedexid, 5, 0, int(first_pokemon.get_needed_exp(5, first_pokemon.exp_curve)), first_pokemon.get_stat_hp(5,first_pokemon.base_hp, first_pokemon.hp_ev, first_pokemon.hp_iv), first_pokemon.get_stat(5,first_pokemon.base_atk, first_pokemon.stats_ev[0], first_pokemon.stats_iv[0]), first_pokemon.get_stat(5,first_pokemon.base_defense, first_pokemon.stats_ev[1], first_pokemon.stats_iv[1]), first_pokemon.get_stat(5,first_pokemon.base_spatk, first_pokemon.stats_ev[2], first_pokemon.stats_iv[2]), first_pokemon.get_stat(5,first_pokemon.base_spdef, first_pokemon.stats_ev[3], first_pokemon.stats_iv[3]), first_pokemon.get_stat(5,first_pokemon.base_speed, first_pokemon.stats_ev[4], first_pokemon.stats_iv[4]), first_pokemon.hp_ev, first_pokemon.stats_ev[0], first_pokemon.stats_ev[1], first_pokemon.stats_ev[2], first_pokemon.stats_ev[3], first_pokemon.stats_ev[4],first_pokemon.get_max_ev(first_pokemon.stats_ev), first_pokemon.hp_iv, first_pokemon.stats_iv[0], first_pokemon.stats_iv[1], first_pokemon.stats_iv[2], first_pokemon.stats_iv[3], first_pokemon.stats_iv[4]))
            await conn.execute("INSERT INTO Equipe (Pokemon1) VALUES (?)", (conn.last_insert_rowid(),))
            await conn.execute("UPDATE User SET Equipeid = ? WHERE Userid = ?", (conn.last_insert_rowid(), self.userid))
            await conn.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (4, self.userid, 10))
            await conn.commit()
            await self.login(username, mdp)
        
    # One line

    async def add_pokemon(self, pokemon):
        async with aiosqlite.connect('database.db') as conn:
            moves = []
            for i in pokemon.moves.items():
                moves.append(i)
            await conn.execute("INSERT INTO Pokemon (PokemonName, Userid, Ability, Move1, Move2, Move3, Move4, Pokedexid, Level, Exp, Needed_exp, Stat_hp, Stat_attack, Stat_defense, Stat_spattack, Stat_spdefense, Stat_speed, Stat_hp_ev, Stat_attack_ev, Stat_defense_ev, Stat_spattack_ev, Stat_spdefense_ev, Stat_speed_ev, Max_ev, Stat_hp_iv , Stat_attack_iv, Stat_defense_iv, Stat_spattack_iv, Stat_spdefense_iv, Stat_speed_iv) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (pokemon.pokemon_name, self.userid, pokemon.ability[0], moves[0][0], moves[1][0], moves[2][0], moves[3][0], pokemon.pokedex_id, pokemon.Level, 0, int(pokemon.get_needed_exp(pokemon.Level, pokemon.exp_curve)), pokemon.get_stat_hp(pokemon.Level,pokemon.base_hp, pokemon.hp_ev, pokemon.hp_iv), pokemon.get_stat(pokemon.Level,pokemon.base_atk, pokemon.stats_ev[0], pokemon.stats_iv[0]), pokemon.get_stat(pokemon.Level,pokemon.base_defense, pokemon.stats_ev[1], pokemon.stats_iv[1]), pokemon.get_stat(pokemon.Level,pokemon.base_spatk, pokemon.stats_ev[2], pokemon.stats_iv[2]), pokemon.get_stat(pokemon.Level,pokemon.base_spdef, pokemon.stats_ev[3], pokemon.stats_iv[3]), pokemon.get_stat(pokemon.Level,pokemon.base_speed, pokemon.stats_ev[4], pokemon.stats_iv[4]), pokemon.hp_ev, pokemon.stats_ev[0], pokemon.stats_ev[1], pokemon.stats_ev[2], pokemon.stats_ev[3], pokemon.stats_ev[4],pokemon.get_max_ev(pokemon.stats_ev), pokemon.hp_iv, pokemon.stats_iv[0], pokemon.stats_iv[1], pokemon.stats_iv[2], pokemon.stats_iv[3], pokemon.stats_iv[4]))
            if len(self.equipe) == 1:
                await conn.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (await conn.last_insert_rowid(), self.equipeid))
            elif len(self.equipe) == 2:
                await conn.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (await conn.last_insert_rowid(), self.equipeid))
            elif len(self.equipe) == 3:
                await conn.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (await conn.last_insert_rowid(), self.equipeid))
            await conn.commit()
            self.pokemon.clear()
            self.equipe.clear()
            pc_cursor = await conn.execute("SELECT Pokedexid, Pokemonid FROM Pokemon WHERE Userid = ?", (self.userid,))
            pc = await pc_cursor.fetchall()
            for i in pc:
                tmp_poke = Pokemon(i[0])
                tmp_poke.set_attribute(self.userid, i[1])
                self.pokemon.append(tmp_poke)
            tmp_equipe_cursor = await conn.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,))
            tmp_equipe = await tmp_equipe_cursor.fetchone()
            for j in tmp_equipe:
                for k in self.pokemon:
                    if k.pokemonid == j:
                        self.equipe.append(k)
                        self.pokemon.remove(k)

    async def add_pokemon_to_team(self, choice):
        async with aiosqlite.connect('database.db') as conn:
            if choice < 1 or choice > len(self.pokemon):
                return False
            pokemonid_cursor = await conn.execute("SELECT Pokemonid FROM Pokemon WHERE Userid = ? AND PokemonName = ?", (self.userid, self.pokemon[choice - 1][0]))
            pokemonid = (await pokemonid_cursor.fetchone())[0]
            if len(self.equipe) == 1:
                await conn.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            elif len(self.equipe) == 2:
                await conn.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            elif len(self.equipe) == 3:
                await conn.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            tmp_equipe_cursor = await conn.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,))
            tmp_equipe = await tmp_equipe_cursor.fetchall()
            for j in tmp_equipe:
                for k in self.pokemon:
                    if k.pokemonid == j:
                        self.equipe.append(k)
                        self.pokemon.remove(k)
            await conn.commit()
            return True

    async def replace_pokemon_in_team(self, choice, choice2):
        async with aiosqlite.connect('database.db') as conn:
            if choice < 1 or choice > 4:
                return False
            if choice2 < 1 or choice2 > len(self.pokemon):
                return False
            pokemonid_cursor = await conn.execute("SELECT Pokemonid FROM Pokemon WHERE Userid = ? AND PokemonName = ?", (self.userid, self.pokemon[choice2 - 1][0]))
            pokemonid = (await pokemonid_cursor.fetchone())[0]
            if choice == 1:
                await conn.execute("UPDATE Equipe SET Pokemon1 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            elif choice == 2:
                await conn.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            elif choice == 3:
                await conn.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            elif choice == 4:
                await conn.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
            tmp_equipe_cursor = await conn.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,))
            tmp_equipe = await tmp_equipe_cursor.fetchall()
            for j in tmp_equipe:
                for k in self.pokemon:
                    if k.pokemonid == j:
                        self.equipe.append(k)
                        self.pokemon.remove(k)
            self.pokemon.append(self.equipe[choice - 1])
            await conn.commit()
            return True

    async def remove_pokemon_to_team(self, choice):
        async with aiosqlite.connect('database.db') as conn:
            if choice < 1 or choice > 4:
                return False
            self.equipe = await conn.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,))
            if choice == 1:
                await conn.execute("UPDATE Equipe SET Pokemon1 = ? WHERE Equipeid = ?", (self.equipe[1], self.equipeid))
                await conn.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (self.equipe[2], self.equipeid))
                await conn.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (self.equipe[3], self.equipeid))
            elif choice == 2:
                await conn.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (self.equipe[2], self.equipeid))
                await conn.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (self.equipe[3], self.equipeid))
            elif choice == 3:
                await conn.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (self.equipe[3], self.equipeid))
            elif choice == 4:
                await conn.execute("UPDATE Equipe SET Pokemon4 = NULL WHERE Equipeid = ?", (self.equipeid,))
            tmp_equipe_cursor = await conn.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,))
            tmp_equipe = await tmp_equipe_cursor.fetchall()
            self.equipe.clear()
            for j in tmp_equipe:
                for k in self.pokemon:
                    if k.pokemonid == j:
                        self.equipe.append(k)
            self.pokemon.append(self.equipe[choice - 1])
            await conn.commit()
            return True

    async def get_username(self):

        return self.username

    async def get_zone(self):
        return self.zone

    async def get_equipe(self):
        return self.equipe

    async def get_pokemon(self):
        return self.pokemon

    async def get_item(self):
        return self.item

    async def get_userid(self):
        return self.userid

    async def get_equipeid(self):
        return self.equipeid

    async def get_zoneid(self):
        return self.zoneid

    async def get_money(self):
        return self.money

    async def zone_name(self):
        return self.zonename

    async def get_price(self, itemname):
        async with aiosqlite.connect('database.db') as conn:
            cursor = await conn.execute("SELECT ItemPrice FROM Item WHERE ItemName = ?", (itemname,))
            result = await cursor.fetchone()
            if result is None:
                return False
            else:
                price = result[0]
                return price

    async def set_zone(self, newZone):
        async with aiosqlite.connect('database.db') as conn:
            cursor = await conn.execute("SELECT ZoneName FROM Zone WHERE ZonePosition = ?", (newZone,))
            result = await cursor.fetchone()
            self.zonename = result[0]
            if result is None:
                return False
            self.zone = newZone
            await conn.execute("UPDATE User SET Zoneid = Zone.Zoneid FROM Zone WHERE Zone.ZonePosition = ? AND User.Userid = ?", (self.zone, self.userid))
            cursor = await conn.execute("SELECT Zoneid FROM User WHERE Userid = ?", (self.userid,))
            self.zoneid = (await cursor.fetchone())[0]
            await conn.commit()

    async def use_item(self, itemid, quantity):
        async with aiosqlite.connect('database.db') as conn:
            await conn.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE Userid = ? AND Itemid = ?", (quantity, self.userid, itemid))
            await conn.execute("DELETE FROM Inventory WHERE Quantity = 0")
            item_cursor = await conn.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,))
            self.item = await item_cursor.fetchall()
            await conn.commit()

    async def add_item(self, itemid, quantity):
        async with aiosqlite.connect('database.db') as conn:
            result_cursor = await conn.execute("SELECT * FROM Item WHERE Itemid = ?", (itemid,))
            result = await result_cursor.fetchone()
            if result is None:
                await conn.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (itemid, self.userid, quantity))
            else:
                await conn.execute("UPDATE Inventory SET Quantity = Quantity + ? WHERE Userid = ? AND Itemid = ?", (quantity, self.userid, itemid))
            item_cursor = await conn.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,))
            self.item = await item_cursor.fetchall()
            await conn.commit()

    async def use_money(self, money):
        async with aiosqlite.connect('database.db') as conn:
            await conn.execute("UPDATE User SET Money = Money - ? WHERE Userid = ?", (money, self.userid))
            await conn.commit()
            self.money -= money

    async def add_money(self, money):
        async with aiosqlite.connect('database.db') as conn:
            await conn.execute("UPDATE User SET Money = Money + ? WHERE Userid = ?", (money, self.userid))
            await conn.commit()
            self.money += money

    def create_pnj_trainer(self, name, zone, pokemon):
        self.username = name
        self.equipe = pokemon
        self.zone = zone
