import sqlite3

class Player :
    def __init__(self):
        self.username = None
        self.equipe = []
        self.pokemon = []
        self.zone = None
    
    def login(self, username, mdp):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, mdp))
        if cursor.fetchone() is None:
            print("Login failed")
            return False
        else:
            self.username = username
            print("Login successful")
            return True
