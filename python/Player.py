import sqlite3
import get_pokemon_moves_abilities as gpm

class Player :
    def __init__(self, username, mdp):
        self.username = ""
        self.userid = 0
        self.equipeid = 0
        self.equipe = []
        self.pokemon = [[]]
        self.item = [[]]
        self.zoneid = 0
        self.zone = 0
        if not self.login(username, mdp) :
            self.register(username, mdp)
        print("Welcome to the game!", self.username, "you are in zone", self.zone, "with your team", self.equipe, "and your pokemon", self.pokemon, "and your items", self.item)
    
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
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        self.pokemon = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        self.zoneid = result[4]
        self.zone = cursor.execute("SELECT ZonePosition FROM Zone WHERE Zoneid = ?", (self.zoneid,)).fetchone()[0]
        conn.close()
        return True
            
    def register(self, username, mdp):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (username, password, Zoneid) VALUES (?, ?, ?)", (username, mdp, 10))
        self.userid = cursor.lastrowid
        print("Choose a Pokemon as your starter: \n 1. Pikachu \n 2. Bulbasaur \n 3. Charmander \n 4. Squirtle")
        choice = int(input("Enter the number of your choice: "))
        starter_pokemon = {
            1: "Pikachu",
            2: "Bulbasaur",
            3: "Charmander",
            4: "Squirtle"
        }.get(choice, "Pikachu")
        pokedexid, moves, ability = gpm.get_pokemon_moves_and_ability(starter_pokemon)
        cursor.execute("INSERT INTO Pokemon (PokemonName, Userid, Pokedexid, Ability, Move1, Move2, Move3, Move4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (starter_pokemon, self.userid, pokedexid, ability, moves[0], moves[1], moves[2], moves[3]))
        cursor.execute("INSERT INTO Equipe (Pokemon1) VALUES (?)", (cursor.lastrowid,))
        cursor.execute("UPDATE User SET Equipeid = ? WHERE Userid = ?", (cursor.lastrowid, self.userid))
        cursor.execute("INSERT INTO Inventory (Itemid, Userid, Quantity) VALUES (?, ?, ?)", (4, self.userid, 10))
        conn.commit()
        conn.close()
        print("Registration successful")
        self.login(username, mdp)
        
    def add_pokemon(self, pokemon_name):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        pokedexid, moves, ability = gpm.get_pokemon_moves_and_ability(pokemon_name)
        cursor.execute("INSERT INTO Pokemon (PokemonName, Userid, Pokedexid, Ability, Move1, Move2, Move3, Move4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (pokemon_name, self.userid, pokedexid, ability, moves[0], moves[1], moves[2], moves[3]))
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
        print(f"Pokémon {pokemon_name} added to your collection.")
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
        
    def getUsername(self):
        return self.username
    
    def getZone(self):
        return self.zone
    
    def getEquipe(self):
        return self.equipe
    
    def getPokemon(self):
        return self.pokemon
    
    def getItem(self):
        return self.item
    
    def getUserid(self):
        return self.userid
    
    def Equipeid(self):
        return self.equipeid
    
    def setZone(self, newZone):
        conn = sqlite3.connect('../database.db')
        cursor = conn.cursor()
        self.zone = newZone
        cursor.execute("UPDATE User SET Zoneid = ? WHERE Userid = ?", (self.zone, self.userid))
        
        