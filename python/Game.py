from Player import *


class Game :
    def __init__(self):
        self.players = []
    
    def zoneCheck(self): #Renvoi un dictionnaire avec le nom du player en clé, et l'id de sa zone en valeur
        resultDict = {}
        for i in range(len(self.players)):
            resultDict[self.players[i].username] = self.players[i].zone
        return resultDict
    
