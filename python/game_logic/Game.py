from Player import *
from Pokemon import *
from Battle import *
from random import *


class Game :
    def __init__(self):
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

    def encounter_pokemon(self, ip_player):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        spawnable_pokemons = cursor.execute("SELECT Pokedexid FROM Pokedex WHERE Zoneid = ?", (self.players[ip_player].get_zoneid(),)).fetchall()
        place_holder = Player()
        place_holder.add_pokemon_to_team(Pokemon(spawnable_pokemons[randint(range(spawnable_pokemons))]))
        wild_battle = Battle(self.players[ip_player], place_holder)
        wild_battle.start_battle()