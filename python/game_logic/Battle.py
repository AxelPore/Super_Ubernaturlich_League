from .Player import *

class Battle :
    def __init__(self):
        self.player1 = None
        self.pokemon1 = None
        self.equipe1 = []
        self.player2 = None
        self.pokemon2 = None
        self.equipe2 = []
        
    async def set_attribute(self, player1, player2):
        self.player1 = player1
        self.pokemon1 = await player1.get_equipe()[0]
        self.equipe1 = await player1.get_equipe()
        self.player2 = player2
        self.pokemon2 = await player2.get_equipe()[0]
        self.equipe2 = await player2.get_equipe()
    
    async def changes_pokemon(self, number, pokemon):
        if number == 1:
            for i in range(len(self.equipe1)):
                if await self.equipe1[i].get_name() == pokemon:
                    self.pokemon1 = self.equipe1[i]
        elif number == 2:
            for i in range(len(self.equipe2)):
                if await self.equipe2[i].get_name() == pokemon:
                    self.pokemon2 = self.equipe2[i]
        
    async def catch_pokemon(self):
        if await self.pokemon2.get_catch_rate() > 65:
            await self.player1.add_pokemon(self.pokemon2)
            return "You successfully catched the pokemon !"
        else :
            return "You didn't catch the pokemon !"
            
    
    async def pokemon_moves(self, number): #Renvoi les moves du pokemon sur le terrain (1 ou 2)
        if (number == 1):
            return await self.pokemon1.get_moves()
        elif (number == 2):
            return await self.pokemon2.get_moves()
        else :
            return "Nombre invalide"
        
    async def use_skill(self, number, skill_name): 
        if (number == 1):
            return await self.pokemon1.use_move(skill_name, self.pokemon2)
        elif (number == 2):
            return await self.pokemon2.use_move(skill_name, self.pokemon1)
        else :
            return "Nombre invalide"
        
    async def end_turn(self, move_data1, move_data2):
        if move_data1[3] > move_data2[3]:
            self.pokemon2.set_hp(move_data1[0] * -1)
            self.pokemon1.set_hp(move_data1[1] * move_data1[0] + move_data1[2] * self.pokemon1.hp_max)
            if self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            elif self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            await self.pokemon1.set_hp(move_data2[0] * -1)
            await self.pokemon2.set_hp(move_data2[1] * move_data2[0] + move_data2[2] * self.pokemon2.hp_max)
            if self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            elif self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            else :
                return "End Turn"
        elif move_data2[3] > move_data1[3]:
            await self.pokemon1.set_hp(move_data2[0] * -1)
            await self.pokemon2.set_hp(move_data2[1] * move_data2[0] + move_data2[2] * self.pokemon2.hp_max)
            if self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            elif self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            await self.pokemon2.set_hp(move_data1[0] * -1)
            await self.pokemon1.set_hp(move_data1[1] * move_data1[0] + move_data1[2] * self.pokemon1.hp_max)
            if self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            elif self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            else :
                return "End Turn"
        elif move_data1[3] == move_data2[3] and self.pokemon1.speed > self.pokemon2.speed :
            await self.pokemon2.set_hp(move_data1[0] * -1)
            await self.pokemon1.set_hp(move_data1[1] * move_data1[0] + move_data1[2] * self.pokemon1.hp_max)
            if self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            elif self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            await self.pokemon1.set_hp(move_data2[0] * -1)
            await self.pokemon2.set_hp(move_data2[1] * move_data2[0] + move_data2[2] * self.pokemon2.hp_max)
            if self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            elif self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            else :
                return "End Turn"
        elif move_data1[3] == move_data2[3] and self.pokemon1.speed < self.pokemon2.speed :
            await self.pokemon1.set_hp(move_data2[0] * -1)
            await self.pokemon2.set_hp(move_data2[1] * move_data2[0] + move_data2[2] * self.pokemon2.hp_max)
            if self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            elif self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            await self.pokemon2.set_hp(move_data1[0] * -1)
            await self.pokemon1.set_hp(move_data1[1] * move_data1[0] + move_data1[2] * self.pokemon1.hp_max)
            if self.pokemon2.hp <= 0 :
                for i in range(len(self.equipe2)):
                    if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                        self.equipe2.pop(i)
                        break
                if len(self.equipe2) == 0 :
                    return "Le joueur 2 a perdu"
                return "Pokemon 2 est KO"
            elif self.pokemon1.hp <= 0 :
                for i in range(len(self.equipe1)):
                    if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                        self.equipe1.pop(i)
                        break
                if len(self.equipe1) == 0 :
                    return "Le joueur 1 a perdu"
                return "Pokemon 1 est KO"
            else :
                return "End Turn"
        else :
            choice = random.randint(1, 3)
            if choice == 1 :
                await self.pokemon2.set_hp(move_data1[0] * -1)
                await self.pokemon1.set_hp(move_data1[1] * move_data1[0] + move_data1[2] * self.pokemon1.hp_max)
                if self.pokemon2.hp <= 0 :
                    for i in range(len(self.equipe2)):
                        if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                            self.equipe2.pop(i)
                            break
                    if len(self.equipe2) == 0 :
                        return "Le joueur 2 a perdu"
                    return "Pokemon 2 est KO"
                elif self.pokemon1.hp <= 0 :
                    for i in range(len(self.equipe1)):
                        if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                            self.equipe1.pop(i)
                            break
                    if len(self.equipe1) == 0 :
                        return "Le joueur 1 a perdu"
                    return "Pokemon 1 est KO"
                await self.pokemon1.set_hp(move_data2[0] * -1)
                await self.pokemon2.set_hp(move_data2[1] * move_data2[0] + move_data2[2] * self.pokemon2.hp_max)
                if self.pokemon1.hp <= 0 :
                    for i in range(len(self.equipe1)):
                        if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                            self.equipe1.pop(i)
                            break
                    if len(self.equipe1) == 0 :
                        return "Le joueur 1 a perdu"
                    return "Pokemon 1 est KO"
                elif self.pokemon2.hp <= 0 :
                    for i in range(len(self.equipe2)):
                        if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                            self.equipe2.pop(i)
                            break
                    if len(self.equipe2) == 0 :
                        return "Le joueur 2 a perdu"
                    return "Pokemon 2 est KO"
                else :
                    return "End Turn"
            else :
                await self.pokemon1.set_hp(move_data2[0] * -1)
                await self.pokemon2.set_hp(move_data2[1] * move_data2[0] + move_data2[2] * self.pokemon2.hp_max)
                if self.pokemon1.hp <= 0 :
                    for i in range(len(self.equipe1)):
                        if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                            self.equipe1.pop(i)
                            break
                    if len(self.equipe1) == 0 :
                        return "Le joueur 1 a perdu"
                    return "Pokemon 1 est KO"
                elif self.pokemon2.hp <= 0 :
                    for i in range(len(self.equipe2)):
                        if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                            self.equipe2.pop(i)
                            break
                    if len(self.equipe2) == 0 :
                        return "Le joueur 2 a perdu"
                    return "Pokemon 2 est KO"
                await self.pokemon2.set_hp(move_data1[0] * -1)
                await self.pokemon1.set_hp(move_data1[1] * move_data1[0] + move_data1[2] * self.pokemon1.hp_max)
                if self.pokemon2.hp <= 0 :
                    for i in range(len(self.equipe2)):
                        if await self.equipe2[i].get_name() == await self.pokemon2.get_name():
                            self.equipe2.pop(i)
                            break
                    if len(self.equipe2) == 0 :
                        return "Le joueur 2 a perdu"
                    return "Pokemon 2 est KO"
                elif self.pokemon1.hp <= 0 :
                    for i in range(len(self.equipe1)):
                        if await self.equipe1[i].get_name() == await self.pokemon1.get_name():
                            self.equipe1.pop(i)
                            break
                    if len(self.equipe1) == 0 :
                        return "Le joueur 1 a perdu"
                    return "Pokemon 1 est KO"
                else :
                    return "End Turn"