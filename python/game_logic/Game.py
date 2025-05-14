from .Player import *
from .Pokemon import *
from .Battle import *
from random import *


class Game :
    def __init__(self):
        self.players = []

    def add_player(self, new_player):
        for i in self.players:
            if (i == new_player):
                return "Joueur déjà connecté"
        self.players.append(new_player)

    def get_players(self):
        return self.players
    
    def zone_check(self): #Renvoi un dictionnaire avec le nom du player en clé, et l'id de sa zone en valeur
        result_dict = {}
        for i in range(len(self.players)):
            result_dict[self.players[i].get_username()] = self.players[i].get_zone()
        return result_dict
    
    def player_move(self, player, input): #input: -1 = gauche, 1 = droite, -10 haut, 10 bas
        self.players[player].set_zone(self.players[player].get_zone() + input)
    
    def pokemon_captured(self, player, new_pokemon):
        self.players[player].add_pokemon(new_pokemon)

    def change_team(self, player):
        self.players[player].change_equipe()

    def check_team(self, player):
        return self.players[player].get_equipe()
    
    def check_bag(self, player):
        return self.players[player].get_item()
    
    def check_pc(self, player):
        return self.players[player].get_pokemon()
    
    def remove_player(self, player):
        self.players.pop(player)

    def encounter_pokemon(self, player):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        spawnable_pokemons = cursor.execute("SELECT Pokedexid FROM Pokedex WHERE Zoneid = ?", (self.players[player].get_zoneid(),)).fetchall()
        place_holder = Player()
        place_holder.add_pokemon_to_team(Pokemon(spawnable_pokemons[randint(range(spawnable_pokemons))]))
        wild_battle = Battle(self.players[player], place_holder)
        wild_battle.start_battle()