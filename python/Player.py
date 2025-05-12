import sqlite3
import Pokemon

class Player :
    def __init__(self):
        self.username = ""
        self.userid = 0
        self.equipeid = 0
        self.equipe = []
        self.pokemon = [[]]
        self.item = [[]]
        self.zoneid = 0
        self.zone = 0
    
    def login(self, username, mdp):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, mdp))
        result = cursor.fetchone()
        if result is None:
            print("Login failed, you'll be registered")
            conn.close()
            return False
        self.username = username
        self.userid = result[0]
        self.equipeid = result[3]
        pc = cursor.execute("SELECT Pokedexid FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        for i in pc:
            self.pokemon.append(Pokemon.Pokemon(i))
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        self.pokemon = 
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        self.zoneid = result[4]
        self.zone = cursor.execute("SELECT ZonePosition FROM Zone WHERE Zoneid = ?", (self.zoneid,)).fetchone()[0]
        conn.close()
        print("Welcome to the game!", self.username, "you are in zone", self.zone, "with your team", self.equipe, "and your pokemon", self.pokemon, "and your items", self.item)
        return True
            
    def register(self, username, mdp, starter_pokemon):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (username, password, Zoneid) VALUES (?, ?, ?)", (username, mdp, 10))
        self.userid = cursor.lastrowid
        first_pokemon = Pokemon.Pokemon(starter_pokemon)
        cursor.execute("INSERT INTO Pokemon (PokemonName, Userid, Pokedexid, Ability, Move1, Move2, Move3, Move4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_pokemon.pokemon_name, self.userid, first_pokemon.pokedexid, first_pokemon.ability, first_pokemon.moves[0], first_pokemon.moves[1], first_pokemon.moves[2], first_pokemon.moves[3]))
        cursor.execute("INSERT INTO Equipe (Pokemon1) VALUES (?)", (cursor.lastrowid,))
        cursor.execute("UPDATE User SET Equipeid = ? WHERE Userid = ?", (cursor.lastrowid, self.userid))
        cursor.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (4, self.userid, 10))
        conn.commit()
        conn.close()
        print("Registration successful")
        self.login(username, mdp)
    
    def add_pokemon(self, pokemon):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Pokemon (PokemonName, Userid, Pokedexid, Ability, Move1, Move2, Move3, Move4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (pokemon.pokemon_name, self.userid, pokemon.pokedexid, pokemon.ability, pokemon.moves[0], pokemon.moves[1], pokemon.moves[2], pokemon.moves[3]))
        if len(self.equipe) == 1:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (cursor.lastrowid, self.equipeid))
        elif len(self.equipe) == 2:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (cursor.lastrowid, self.equipeid))
        elif len(self.equipe) == 3:
            cursor.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (cursor.lastrowid, self.equipeid))
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        self.pokemon = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        conn.commit()
        conn.close()
        print(f"Pokémon {pokemon.pokemon_name} added to your collection.")
        print(self.username, "this is now your team", self.equipe, "and your pokemons", self.pokemon)
        
    def change_equipe(self):
        if len(self.equipe) == 1:
            print("Here you can manage your team : \n 1. Add a Pokemon \n 2. Replace a Pokemon ")
            choice = int(input("Enter the number of your choice: "))
            if choice == 1:
                self.add_pokemon_to_team()
            elif choice == 2:
                self.replace_pokemon_in_team()
            else:
                print("Invalid choice.")
        if len(self.equipe) == 4:
            print("Here you can manage your team : \n 1. Replace a Pokemon \n 2. Remove a Pokemon")
            choice = int(input("Enter the number of your choice: "))
            if choice == 1:
                self.replace_pokemon_in_team()
            elif choice == 2:
                self.remove_pokemon_to_team()
            else:
                print("Invalid choice.")
        else:
            print("Here you can manage your team : \n 1. Add a Pokemon \n 2. Replace a Pokemon \n 3. Remove a Pokemon")
            choice = int(input("Enter the number of your choice: "))
            if choice == 1:
                self.add_pokemon_to_team()
            elif choice == 2:
                self.replace_pokemon_in_team()
            elif choice == 3:
                self.remove_pokemon_to_team()
            else:
                print("Invalid choice.")
        
    def add_pokemon_to_team(self):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        print(f"Choose a Pokemon to add : \n")
        for i, pokemon in enumerate(self.pokemon):
            print(f"{i + 1}. {pokemon}   ")
        choice2 = int(input("Enter the number of your choice: "))
        if choice2 < 1 or choice2 > len(self.pokemon):
            print("Invalid choice.")
            conn.close()
            return
        pokemonid = cursor.execute("SELECT Pokemonid FROM Pokemon WHERE Userid = ? AND PokemonName = ?", (self.userid, self.pokemon[choice2 - 1][0])).fetchone()[0]
        if len(self.equipe) == 1:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif len(self.equipe) == 2:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif len(self.equipe) == 3:
            cursor.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        conn.commit()
        conn.close()
        print(self.username, "this is now your team", self.equipe, "and your pokemons", self.pokemon)
        
    def replace_pokemon_in_team(self):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        if len(self.equipe) == 1:
            print(f"Choose a Pokemon to replace: \n 1. {self.equipe[0]}")
        elif len(self.equipe) == 2:
            print(f"Choose a Pokemon to replace: \n 1. {self.equipe[0]} \n 2. {self.equipe[1]}")
        elif len(self.equipe) == 3:
            print(f"Choose a Pokemon to replace: \n 1. {self.equipe[0]} \n 2. {self.equipe[1]} \n 3. {self.equipe[2]}")
        elif len(self.equipe) == 4:
            print(f"Choose a Pokemon to replace: \n 1. {self.equipe[0]} \n 2. {self.equipe[1]} \n 3. {self.equipe[2]} \n 4. {self.equipe[3]}")
        choice = int(input("Enter the number of your choice: "))
        if choice < 1 or choice > 4:
            print("Invalid choice.")
            conn.close()
            return
        print(f"Here is your pokemons :")
        for i, pokemon in enumerate(self.pokemon):
            print(f"{i + 1}. {pokemon}   ")
        choice2 = int(input("Enter the number of your choice: "))
        if choice2 < 1 or choice2 > len(self.pokemon):
            print("Invalid choice.")
            conn.close()
            return
        pokemonid = cursor.execute("SELECT Pokemonid FROM Pokemon WHERE Userid = ? AND PokemonName = ?", (self.userid, self.pokemon[choice2 - 1][0])).fetchone()[0]
        if choice == 1:
            cursor.execute("UPDATE Equipe SET Pokemon1 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif choice == 2:
            cursor.execute("UPDATE Equipe SET Pokemon2 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif choice == 3:
            cursor.execute("UPDATE Equipe SET Pokemon3 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        elif choice == 4:
            cursor.execute("UPDATE Equipe SET Pokemon4 = ? WHERE Equipeid = ?", (pokemonid, self.equipeid))
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        conn.commit()
        conn.close()
        print(self.username, "this is now your team", self.equipe, "and your pokemons", self.pokemon)
        
    def remove_pokemon_to_team(self):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        if len(self.equipe) == 2:
            print(f"Choose a Pokemon to remove from your team: \n 1. {self.equipe[0]} \n 2. {self.equipe[1]}")
        elif len(self.equipe) == 3:
            print(f"Choose a Pokemon to remove from your team: \n 1. {self.equipe[0]} \n 2. {self.equipe[1]} \n 3. {self.equipe[2]}")
        elif len(self.equipe) == 4:
            print(f"Choose a Pokemon to remove from your team: \n 1. {self.equipe[0]} \n 2. {self.equipe[1]} \n 3. {self.equipe[2]} \n 4. {self.equipe[3]}")
        choice = int(input("Enter the number of your choice: "))
        if choice < 1 or choice > 4:
            print("Invalid choice.")
            conn.close()
            return
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchone()
        print(self.equipe)
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
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        conn.commit()
        conn.close()
        print(self.username, "this is now your team", self.equipe, "and your pokemons", self.pokemon)
        
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
            print("Invalid zone.")
            conn.close()
            return
        cursor.execute("UPDATE User SET Zoneid = Zone.Zoneid FROM Zone WHERE Zone.ZonePosition = ? AND User.Userid = ?", (self.zone, self.userid))
        self.zoneid = cursor.execute("SELECT Zoneid FROM User WHERE Userid = ?", (self.userid,)).fetchone()[0]
        print("You are now in zone", result[0])
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
        for item in self.item:
            if item[0] == itemid:
                item_name = item[0]
                break
        print(f"You used {quantity}{item_name}.")
        
    def add_item(self, itemid, quantity):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM Item WHERE Itemid = ?", (itemid,)).fetchone()[0]
        if result is None:
            cursor.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (itemid, self.userid, quantity))
        else:
            cursor.execute("UPDATE Inventory SET Quantity = Quantity + ? WHERE Userid = ? AND Itemid = ?", (quantity, self.userid, itemid))
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        for item in self.item:
            if item[0] == itemid:
                item_name = item[0]
                break
        conn.commit()
        conn.close()
        print(f"You added {quantity} {item_name} to your inventory.")