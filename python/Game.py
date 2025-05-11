from Player import *


class Game :
    def __init__(self):
        self.players = []

    def add_player(self, new_player):
        for i in self.players:
            if (i == new_player):
                return "Joueur déjà existant"
        self.players.append(new_player)
    
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