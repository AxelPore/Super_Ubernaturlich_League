from .Player import *

class Battle :
    def __init__(self, player1, player2):
        self.player1 = player1
        self.pokemon1 = player1.get_equipe()[0]
        self.player2 = player2
        self.pokemon2 = player2.get_equipe()[0]
    
    def pokemon_moves(self, number): #Renvoi les moves du pokemon sur le terrain (1 ou 2)
        if (number == 1):
            self.pokemon1.get_moves()
        elif (number == 2):
            self.pokemon2.get_moves()
        else :
            return "Nombre invalide"
