import sqlite3

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
        self.equipe = cursor.execute("SELECT * FROM Equipe WHERE Equipeid = ?", (self.equipeid,)).fetchall()
        self.pokemon = cursor.execute("SELECT PokemonName, Surname FROM Pokemon WHERE Userid = ?", (self.userid,)).fetchall()
        self.item = cursor.execute("SELECT ItemName, Quantity FROM Iventory INNER JOIN Item ON Inventory.Itemid = Item.Itemid WHERE Userid = ?", (self.userid,)).fetchall()
        self.zone = result[4]
        conn.close()
        return True
            
    def register(self, username, mdp):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        print("Choose a Pokemon as your starter: \n 1. Pikachu \n 2. Bulbasaur \n 3. Charmander \n 4. Squirtle")
        choice = int(input("Enter the number of your choice: "))
        starter_pokemon = {
            1: "Pikachu",
            2: "Bulbasaur",
            3: "Charmander",
            4: "Squirtle"
        }.get(choice, "Pikachu")
        
        cursor.execute("INSERT INTO User (username, password, Zoneid) VALUES (?, ?, ?)", (username, mdp, 1))
        conn.commit()
        conn.close()
        print("Registration successful")
        self.login(username, mdp)