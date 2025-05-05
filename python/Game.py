from Player import *


class Game :
    def __init__(self):
        self.players = []
    
    def zoneCheck(self):
        for i in range(len(self.players)):
