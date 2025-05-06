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
        self.zone = 0
        if not self.login(username, mdp) :
            self.register(username, mdp)
        print("Welcome to the game!", username, "you are in zone", self.zone, "with your team", self.equipe, "and your pokemon", self.pokemon, "and your items", self.item)
    
    def login(self, username, mdp):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, mdp))
        result = cursor.fetchone()
        if result is None:
            print("Login failed")
            return False
        self.username = username
        self.userid = result[0]
        self.equipeid = result[3]
        self.equipe = cursor.execute("SELECT Pokemon1, Pokemon2, Pokemon3, Pokemon4 FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.equipe = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ? AND Pokemonid IN (?, ?, ?, ?)", (self.userid, self.equipe[0][0], self.equipe[0][1], self.equipe[0][2], self.equipe[0][3])).fetchall()
        self.pokemon = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Inventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        self.zone = result[4]
        conn.close()
        return True
            
    def register(self, username, mdp):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (username, password, Zoneid) VALUES (?, ?, ?)", (username, mdp, 1))
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