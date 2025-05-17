from random import *
from .Player import Player
from .Pokemon import Pokemon
from .Battle import Battle
from sqlite3 import connect
from random import randint


class Game :
    def __init__(self):
        conn = connect('database.db')
        cursor = conn.cursor()
        self.max_pokemon = cursor.execute("SELECT Pokedexid FROM Pokedex").fetchall()[-1]
        self.Player = Player
        self.Pokemon = Pokemon
        self.Battle = Battle
        self.players = {}


    def add_player(self, ip_player, new_player):
        for i in self.players:
            if (i == new_player):
                return "Joueur déjà connecté"
        self.players[ip_player] = new_player

    def get_players(self):
        return self.players
    
    def zone_check(self): #Renvoi un dictionnaire avec le nom du player en clé, et l'id de sa zone en valeur
        result_dict = {}
        for i in range(len(self.players)):
            result_dict[self.players[i].get_username()] = self.players[i].get_zone()
        return result_dict
    
    def player_move(self, ip_player, input): #input: -1 = gauche, 1 = droite, -10 haut, 10 bas
        if self.players[ip_player].set_zone(self.players[ip_player].get_zone() + input) == False:
            return False
    
    def pokemon_captured(self, ip_player, new_pokemon):
        self.players[ip_player].add_pokemon(new_pokemon)

    def check_team(self, ip_player):
        return self.players[ip_player].get_equipe()
    
    def check_bag(self, ip_player):
        temp = self.players[ip_player].get_item()
        result = ''
        for i in range(len(temp)-1):
            result += temp[i][0] + temp[i][i]
        print(result)
        return result
    
    def check_pc(self, ip_player):
        return self.players[ip_player].get_pokemon()
    
    def remove_player(self, ip_player):
        self.players.pop(ip_player)
    
    def buy_item(self, ip_player, choose_item, quantity):
        self.players[ip_player].add_item(choose_item,quantity)

    def encounter_pokemon(self, ip_player):
        conn = connect('database.db')
        cursor = conn.cursor()
        spawnable_pokemons = cursor.execute("SELECT Pokedexid FROM Pokedex WHERE Zoneid = ?", (self.players[ip_player].get_zoneid(),)).fetchall()
        place_holder = self.Player()
        place_holder.add_pokemon_to_team(self.Pokemon(spawnable_pokemons[randint(range(spawnable_pokemons))]))
        wild_battle = self.Battle(self.players[ip_player], place_holder)
        wild_battle.start_battle()
    
    def generate_trainer(self, number_of_trainers, player_zone):
        for i in number_of_trainers:
            self.add_player(0, self.Player().create_pnj_trainer("Billy", player_zone, [self.Pokemon(randint(1, self.max_pokemon +1)), self.Pokemon(randint(1, self.max_pokemon +1)), self.Pokemon(randint(1, self.max_pokemon +1)), self.Pokemon(randint(1, self.max_pokemon +1))]))
