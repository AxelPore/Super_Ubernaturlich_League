import sqlite3
from Pokemon import *

class Player :
    def __init__(self):
        self.username = ""
        self.userid = 0
        self.equipeid = 0
        self.equipe = []
        self.pokemon = []
        self.item = [[]]
        self.zoneid = 0
        self.zone = 0
    
    def login(self, username, mdp):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, mdp))
        result = cursor.fetchone()
        if result is None:
            conn.close()
            return False
        self.username = username
        self.userid = result[0]
        self.equipeid = result[3]
        pc = cursor.execute("SELECT Pokedexid, Pokemonid FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        for i in pc:
            tmp_poke = Pokemon(i[0])
            tmp_poke.set_attribute(self.userid, i[1])
            self.pokemon.append(tmp_poke)
        tmp_equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchone()
        for j in tmp_equipe:
            for k in self.pokemon:
                if k.pokemonid == j:
                    self.equipe.append(k)  
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        self.zoneid = result[4]
        self.zone = cursor.execute("SELECT ZonePosition FROM Zone WHERE Zoneid = ?", (self.zoneid,)).fetchone()[0]
        conn.close()
        return True
            
    def register(self, username, mdp, starter_pokemon):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        print("Attempting to register user... with username: ", username, " and password: ", mdp, " and starter: ", starter_pokemon)
        cursor.execute("INSERT INTO User (username, password, Zoneid) VALUES (?, ?, ?)", (username, mdp, 10))
        self.userid = cursor.lastrowid
        print(self.userid)
        conn.commit()
        first_pokemon = Pokemon(starter_pokemon)
        moves = []
        for i in first_pokemon.moves.items():
            moves.append(i)
        pokedexid = int(first_pokemon.pokedexid)
        cursor.execute("INSERT INTO Pokemon (PokemonName, Userid, Ability, Move1, Move2, Move3, Move4, Pokedexid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_pokemon.pokemon_name, self.userid, first_pokemon.ability[0], moves[0][0], moves[1][0], moves[2][0], moves[3][0], pokedexid))
        cursor.execute("INSERT INTO Equipe (Pokemon1) VALUES (?)", (cursor.lastrowid,))
        cursor.execute("UPDATE User SET Equipeid = ? WHERE Userid = ?", (cursor.lastrowid, self.userid))
        cursor.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (4, self.userid, 10))
        conn.commit()
        conn.close()
        self.login(username, mdp)
    
    def add_pokemon(self, pokemon):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        moves = []
        for i in pokemon.moves.items():
            moves.append(i)
        cursor.execute("INSERT INTO Pokemon (PokemonName, Userid, Pokedexid, Ability, Move1, Move2, Move3, Move4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (pokemon.pokemon_name, self.userid, pokemon.pokedexid, pokemon.ability[0], moves[0][0], moves[1][0], moves[2][0], moves[3][0]))
        print(len(self.equipe))
        if len(self.equipe) == 1:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (cursor.lastrowid, self.equipeid))
        elif len(self.equipe) == 2:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (cursor.lastrowid, self.equipeid))
        elif len(self.equipe) == 3:
            cursor.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (cursor.lastrowid, self.equipeid))
        conn.commit()
        self.pokemon.clear()
        self.equipe.clear()
        pc = cursor.execute("SELECT Pokedexid, Pokemonid FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        for i in pc:
            tmp_poke = Pokemon(i[0])
            tmp_poke.set_attribute(self.userid, i[1])
            self.pokemon.append(tmp_poke)
        tmp_equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchone()
        for j in tmp_equipe:
            for k in self.pokemon:
                if k.pokemonid == j:
                    self.equipe.append(k)
        conn.commit()
        conn.close()
        
    def add_pokemon_to_team(self, choice):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        if choice < 1 or choice > len(self.pokemon):
            conn.close()
            return False
        pokemonid = cursor.execute("SELECT Pokemonid FROM Pokemon WHERE Userid = ? AND PokemonName = ?", (self.userid, self.pokemon[choice - 1][0])).fetchone()[0]
        if len(self.equipe) == 1:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif len(self.equipe) == 2:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif len(self.equipe) == 3:
            cursor.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        tmp_equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        for j in tmp_equipe:
            for k in self.pokemon:
                if k.pokemonid == j:
                    self.equipe.append(k)
        conn.commit()
        conn.close()
        
    def replace_pokemon_in_team(self, choice, choice2):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        if choice < 1 or choice > 4:
            conn.close()
            return False
        if choice2 < 1 or choice2 > len(self.pokemon):
            conn.close()
            return False
        pokemonid = cursor.execute("SELECT Pokemonid FROM Pokemon WHERE Userid = ? AND PokemonName = ?", (self.userid, self.pokemon[choice2 - 1][0])).fetchone()[0]
        if choice == 1:
            cursor.execute("UPDATE Equipe SET Pokemon1 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif choice == 2:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif choice == 3:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif choice == 4:
            cursor.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        tmp_equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        for j in tmp_equipe:
            for k in self.pokemon:
                if k.pokemonid == j:
                    self.equipe.append(k)
        conn.commit()
        conn.close()
        
    def remove_pokemon_to_team(self, choice):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        if choice < 1 or choice > 4:
            conn.close()
            return False
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchone()
        if choice == 1:
            cursor.execute("UPDATE Equipe SET Pokemon1 = ? WHERE Equipeid = ?", (self.equipe[1], self.equipeid))
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (self.equipe[2], self.equipeid))
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (self.equipe[3], self.equipeid))
        elif choice == 2:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (self.equipe[2], self.equipeid))
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (self.equipe[3], self.equipeid))
        elif choice == 3:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (self.equipe[3], self.equipeid))
        elif choice == 4:
            cursor.execute("UPDATE Equipe SET Pokemon4 = NULL WHERE Equipeid = ?", (self.equipeid,))
        tmp_equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        for j in tmp_equipe:
            for k in self.pokemon:
                if k.pokemonid == j:
                    self.equipe.append(k)
        conn.commit()
        conn.close()
        
    def get_username(self):
        return self.username
    
    def get_zone(self):
        return self.zone
    
    def get_equipe(self):
        return self.equipe
    
    def get_pokemon(self):
        return self.pokemon
    
    def get_item(self):
        return self.item
    
    def get_userid(self):
        return self.userid
    
    def get_equipeid(self):
        return self.equipeid
    
    def get_zoneid(self):
        return self.zoneid
    
    def set_zone(self, newZone):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        self.zone = newZone
        cursor.execute("SELECT ZoneName FROM Zone WHERE ZonePosition = ?", (self.zone,))
        result = cursor.fetchone()
        if result is None:
            conn.close()
            return False
        cursor.execute("UPDATE User SET Zoneid = Zone.Zoneid FROM Zone WHERE Zone.ZonePosition = ? AND User.Userid = ?", (self.zone, self.userid))
        self.zoneid = cursor.execute("SELECT Zoneid FROM User WHERE Userid = ?", (self.userid,)).fetchone()[0]
        conn.commit()
        conn.close()
        
    def use_item(self, itemid, quantity):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE Userid = ? AND Itemid = ?", (quantity, self.userid, itemid))
        cursor.execute("DELETE * FROM Item WHERE Quantity = 0")
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        conn.commit()
        conn.close()
        
    def add_item(self, itemid, quantity):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM Item WHERE Itemid = ?", (itemid,)).fetchone()[0]
        if result is None:
            cursor.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (itemid, self.userid, quantity))
        else:
            cursor.execute("UPDATE Inventory SET Quantity = Quantity + ? WHERE Userid = ? AND Itemid = ?", (quantity, self.userid, itemid))
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        conn.commit()
        conn.close()
        
    def use_money(self, money):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET Money = Money - ? WHERE Userid = ?", (money, self.userid))
        conn.commit()
        conn.close()
        
    def add_money(self, money):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET Money = Money + ? WHERE Userid = ?", (money, self.userid))
        conn.commit()
        conn.close()
    
    