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
