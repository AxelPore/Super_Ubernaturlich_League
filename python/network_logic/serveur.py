import asyncio
import random
from pprint import pprint
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_logic.Player import Player
from game_logic.Game import *
from game_logic.Battle import *

global CLIENTS
CLIENTS = {}

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

game = Game()

def generateId(lenght):
    id = ''
    while lenght > 8:
        comp = 9
        if lenght <= 9:
            comp = lenght
        id += str(hex(random.randrange(1, 10**(comp))))[2:]
        lenght -= 9
    return id

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
async def handle_battle(reader, writer, player, trainer):
    battle = Battle(player, trainer)
    battle.start_battle()
    writer.write(f"{DISPLAY_BYTE_ID}|You are now in a battle with {trainer}!".encode())
    await writer.drain()
    await asyncio.sleep(0.5)
    
    
async def handle_arena_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the arena!".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{DISPLAY_BYTE_ID}|Here are your options:\n 1. Fight another trainer in the Arena \n 2. Check your Pokemon \n 3. Check your items \n 4. Exit".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        await writer.drain()
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            writer.write(f"{DISPLAY_BYTE_ID}|Here are the trainers nearby:\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            number_of_trainers = random.randint(1, 5)
            game.generate_trainer(number_of_trainers, player.get_zone())
            get_trainer = game.zone_check()
            for k, v in get_trainer.items():
                if v == player.get_zone():
                    writer.write(f"{DISPLAY_BYTE_ID}|{k} is nearby.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the trainer you want to fight: ".encode())
                    await writer.drain()
                    trainer = await reader.read(1024)
                    trainer = trainer.decode().strip()
                    await handle_battle(reader, writer, player, trainer)
                else:
                    writer.write(f"{DISPLAY_BYTE_ID}|No trainers nearby.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
            continue
        elif choice == "2":
            equipe = player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].get_moves()}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "3":
            items = player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "4":
            writer.write(f"{DISPLAY_BYTE_ID}|You are now in the city.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            await handle_city_menu(reader, writer, player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
        
async def handle_buy_items(reader, writer, player):
    while True:        
        writer.write(f"{DISPLAY_BYTE_ID}|Here are the items available for purchase:\n 1. Potion \n 2. Super Potion \n 3. Revive \n 4. PokeBall \n 5. Elixir \n 6. Antidote \n 7. Burn-Heal \n 8. Ice-Heal \n 9. awakening \n 10. Paralyze-Heal \n 11. Exit".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of the item you want to buy: ".encode())
        await writer.drain()
        item_choice = await reader.read(1024)
        item_choice = item_choice.decode().strip()
        if item_choice != None and item_choice != "11":
            writer.write(f"{INPUT_BYTE_ID}|Enter how many you want to buy: ".encode())
            await writer.drain()
            quantity = await reader.read(1024)
            quantity = quantity.decode().strip()
            item = ["Potion", "Super Potion", "Revive", "PokeBall", "Elixir", "Antidote", "Burn-Heal", "Ice-Heal", "awakening", "Paralyze-Heal"]
            writer.write(f"{INPUT_BYTE_ID}|You will bought {quantity} {item[int(item_choice)-1]} for the price of {quantity * player.get_price(item[int(item_choice)-1])}, continue ? : y/n ".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            confirm = await reader.read(1024)
            confirm = confirm.decode().strip()
            if confirm.lower() == "n":
                writer.write(f"{DISPLAY_BYTE_ID}|Transaction cancelled".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                break
            for i in range(len(item)):
                if item_choice == item[i]:
                    writer.write(f"{DISPLAY_BYTE_ID}|You bought {quantity} {item[i]}!".encode()) 
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    game.buy_item(player, item[i], quantity)
                    break
            await asyncio.sleep(0.5)
            break
        else:
            await handle_pokemart_menu(reader, writer, player)
            break
    
async def handle_sell_items(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Here are the items you can sell:\n".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        items = player.get_item()
        for i in range(len(items)):
            writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of the item you want to sell: ".encode())
        await writer.drain()
        item_choice = await reader.read(1024)
        item_choice = item_choice.decode().strip()
        item_choice = int(item_choice) - 1
        if item_choice != None:
            writer.write(f"{INPUT_BYTE_ID}|Enter how many you want to sell: ".encode())
            await writer.drain()
            quantity = await reader.read(1024)
            quantity = quantity.decode().strip()
            item = items[item_choice][0]
            writer.write(f"{INPUT_BYTE_ID}|You will sell {quantity} {item} for the price of {quantity * player.get_price(item)}, continue ? : y/n ".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{DISPLAY_BYTE_ID}|You sold {quantity} {item}!".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            game.sell_item(player, item, quantity)
            await asyncio.sleep(0.5)
            break
        else:
            await handle_pokemart_menu(reader, writer, player)
            break
    
async def handle_pokemart_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the Pokemart! Here are your options:\n 1. Buy items \n 2. Sell items \n 3. Check your Pokemon \n 4. Check your items \n 5. Exit Pokemart".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            await handle_buy_items(reader, writer, player)
            continue
        elif choice == "2":
            await handle_sell_items(reader, writer, player)
            continue
        elif choice == "3":
            equipe = player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].get_moves()}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "4":
            items = player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "5":
            writer.write(f"{DISPLAY_BYTE_ID}|You exited the Pokemart".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            await handle_city_menu(reader, writer, player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
        
async def handle_pokecenter_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the Pokecenter! Here are your options:\n 1. Heal your Pokemon \n 2. Check your Pokemon \n 3. Check your items \n 4. Access PC \n 5. Exit Pokecenter".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        await writer.drain()
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            # game.heal_pokemon(player)
            writer.write(f"{DISPLAY_BYTE_ID}|Healing your Pokemon...".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
        elif choice == "2":
            equipe = player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].get_moves()}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "3":
            items = player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "4":
            writer.write(f"{DISPLAY_BYTE_ID}|You are now in the PC.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            await handle_team_change(reader, writer, player)
            continue
        elif choice == "5":
            writer.write(f"{DISPLAY_BYTE_ID}|You are now in the city.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            await handle_city_menu(reader, writer, player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue

async def change_player_zone(reader, writer, player):
    while True:
        #writer.write(f"{DISPLAY_BYTE_ID}|You are in zone {game.get_zone_name(player)}.\n".encode())
        #writer.write(f"{DISPLAY_BYTE_ID}| You can access these zones : \n".encode())
        #await writer.drain()
        #await asyncio.sleep(0.5)
        #for i in game.get_zones(player):
        writer.write(f"{INPUT_BYTE_ID}|You are going to change your zone. Are you sure ? : y/n \n".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        choice = await reader.read(1)
        choice = choice.decode().strip()
        if choice == "n":
            break
        MOVES = {
            "up": -10,
            "down": 10,
            "left": -1,
            "right": 1
        }
        writer.write(f"{INPUT_BYTE_ID}|Enter your move (up, down, left, right): ".encode())
        await writer.drain()
        move = await reader.read(1024)
        move = move.decode().strip()
        print(f"Player move: {move} and id : {MOVES[move]}")  # Debugging log
        if move in MOVES:
            for i in range(len(game.get_players())):
                print(i)
                if game.get_players()[i] == player:
                    game.player_move(i, MOVES[move])
                    break
            # writer.write(f"{DISPLAY_BYTE_ID}|You moved to zone {game.get_zone_name(player)}.\n".encode())
            # await writer.drain()
            # await asyncio.sleep(0.5)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid move. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue

async def handle_wild_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the wild! Here are your options:\n 1. Find and fight a wild Pokemon \n 2. Fight another trainer nearby \n 3. Check your Pokemon \n 4. Check your items \n 5. Explore somewhere else \n 6. Go back to the main menu \n".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        await writer.drain()
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            game.encounter_pokemon(player)
            writer.write(f"{DISPLAY_BYTE_ID}|You encountered a wild Pokemon!".encode())
            continue
        elif choice == "2":
            writer.write(f"{DISPLAY_BYTE_ID}|Here are the trainers nearby:\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            number_of_trainers = random.randint(1, 5)
            game.generate_trainer(number_of_trainers, player.get_zone())
            get_trainer = game.zone_check()
            for k, v in get_trainer.items():
                if v == player.get_zone():
                    writer.write(f"{DISPLAY_BYTE_ID}|{k} is nearby.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the trainer you want to fight: ".encode())
                    await writer.drain()
                    trainer = await reader.read(1024)
                    trainer = trainer.decode().strip()
                    await handle_battle(reader, writer, player, trainer)
                else:
                    writer.write(f"{DISPLAY_BYTE_ID}|No trainers nearby.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
            continue
        elif choice == "3":
            equipe = player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].get_moves()}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "4":
            items = player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "5":
            await change_player_zone(reader, writer, player)
            continue
        elif choice == "6":
            game.remove_player(player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue

async def handle_city_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the city! Here are your options:\n 1. Go to the Pokecenter \n 2. Go to the Pokemart \n 3. Go to the Arena \n 4. Check your Pokemon \n 5. Check your items\n 6. Exit City \n 7. Go back to the main menu".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        await writer.drain()
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            await handle_pokecenter_menu(reader, writer, player)
            continue
        elif choice == "2":
            await handle_pokemart_menu(reader, writer, player)
            continue
        elif choice == "3":
            await handle_arena_menu(reader, writer, player)
            continue
        elif choice == "4":
            equipe = player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].get_moves()}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "5":
            items = player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "6":
            await change_player_zone(reader, writer, player)
            continue
        elif choice == "7":
            game.remove_player(player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue

async def handle_input(client_id, message):
    writer = CLIENTS[client_id]['w']
    reader = CLIENTS[client_id]['r']
    writer.write(f"{INPUT_BYTE_ID}|{message}".encode())
    await writer.drain()
    data = await reader.read(1024)
    return data.decode()

async def handle_team_change(reader, writer, player):
    while True:
        equipe = player.get_equipe()
        pokemon = player.get_pokemon()        
        if len(equipe) == 1:
            writer.write(f"{DISPLAY_BYTE_ID}|Here you can manage your team : \n 1. Add a Pokemon \n 2. Replace a Pokemon \n 3. Exit".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            if choice == "1":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to add: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.add_pokemon_to_team(int(choice))
            elif choice == "2":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to put instead of {equipe[0].get_name()}: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.replace_pokemon_in_team(1, int(choice))
            elif choice == "3":
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif len(equipe) == 4:
            writer.write(f"{DISPLAY_BYTE_ID}|Here you can manage your team : \n 1. Replace a Pokemon \n 2. Remove a Pokemon \n 3. Exit".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            if choice == "1":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to replace: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                choice2 = 0
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to put instead of {equipe[int(choice)-1].get_name()}: ".encode())
                    await writer.drain()
                    choice2 = await reader.read(1024)
                    choice2 = choice.decode().strip()
                player.replace_pokemon_in_team(int(choice), int(choice2))
            elif choice == "2":
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to remove: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.remove_pokemon_to_team(int(choice))
            elif choice == "3":
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Here you can manage your team : \n 1. Add a Pokemon \n 2. Replace a Pokemon \n 3. Remove a Pokemon \n 4. Exit".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            if choice == "1":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to add: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.add_pokemon_to_team(int(choice))
            elif choice == "2":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to replace: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                choice2 = 0
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to put instead of {equipe[int(choice)-1].get_name()}: ".encode())
                    await writer.drain()
                    choice2 = await reader.read(1024)
                    choice2 = choice.decode().strip()
                player.replace_pokemon_in_team(int(choice), int(choice2))
            elif choice == "3":
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to remove: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.remove_pokemon_to_team(int(choice))
            elif choice == "4":
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue

async def login_or_register(reader, writer):
    while True:
        writer.write(f"{INPUT_BYTE_ID}|{bcolors.OKCYAN}Welcome! Do you want to (1) Login, (2) Register or (3) Quit? {bcolors.ENDC}".encode())
        await writer.drain()
        choice = await reader.read(1024)
        print(f"Raw data received: {choice}")  # Debugging log
        choice = choice.decode().strip()
        print(f"Client chose: {choice}")  # Debugging log

        if choice == "1":
            # Handle login
            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter your username: {bcolors.ENDC}".encode())
            await writer.drain()
            username = await reader.read(1024)
            username = username.decode().strip()
            print(f"Received username for login: {username}")  # Debugging log

            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter your password: {bcolors.ENDC}".encode())
            await writer.drain()
            password = await reader.read(1024)
            password = password.decode().strip()
            print(f"Received password for login: {password}")  # Debugging log

            player = Player()
            if player.login(username, password):
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.OKGREEN}Login successful! Welcome, {username}.{bcolors.ENDC}\n".encode())
                await writer.drain()
                writer.write(f"{DISPLAY_BYTE_ID}|Welcome Trainer ! It's time to start your journey ".encode())
                await writer.drain()
                await asyncio.sleep(0.5) 
                pprint(f"Player object after registration: {player}")  # Debugging log
                game.add_player(player)
                return player
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.WARNING}Login failed or account not found. Please try again or Register.{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                continue
            
            

        elif choice == "2":
            # Handle registration
            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter a username to register: {bcolors.ENDC}".encode())
            await writer.drain()
            username = await reader.read(1024)
            username = username.decode().strip()
            print(f"Received username for registration: {username}")  # Debugging log

            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter a password to register: {bcolors.ENDC}".encode())
            await writer.drain()
            password = await reader.read(1024)
            password = password.decode().strip()
            print(f"Received password for registration: {password}")  # Debugging log

            STARTER_POKEMONS = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee", "Chikorita", "Cyndaquil", "Totodile", "Treecko", "Torchic", "Mudkip", "Turtwig", "Chimchar", "Piplup", "Snivy", "Tepig", "Oshawott", "Chespin", "Fennekin", "Froakie", "Rowlet", "Litten", "Popplio", "Grookey", "Scorbunny", "Sobble", "Sprigatito", "Fuecoco", "Quaxly"]
            writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.BOLD}Here is a list of Pokemon starters : {bcolors.ENDC}\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)

            for i in range (len(STARTER_POKEMONS)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {STARTER_POKEMONS[i]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)  # Optional delay for better readability

            writer.write(f"{INPUT_BYTE_ID}|\n{bcolors.HEADER}Choose a pokemon starter: {bcolors.ENDC}".encode())
            await writer.drain()
            starter = await reader.read(1024)
            starter = starter.decode().strip()
            starter = {
                1: 1,
                2: 4,
                3: 7,
                4: 25,
                5: 133,
                6: 152,
                7: 155,
                8: 158,
                9: 252,
                10: 255,
                11: 258,
                12: 387,
                13: 390,
                14: 393,
                15: 495,
                16: 498,
                17: 501,
                18: 650,
                19: 653,
                20: 656,
                21: 722,
                22: 725,
                23: 728,
                24: 810,
                25: 813,
                26: 816,
                27: 906,
                28: 909,
                29: 912,
            }.get(int(starter), 1)  # Default to Bulbasaur if invalid choice
            print(f"Received starter choice: {starter}")  # Debugging log

            player = Player()
            try:
                print(f"Attempting to register user: {username} with password: {password} and starter: {starter}")  # Debugging log
                player.register(username, password, starter)
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.OKGREEN}Registration successful! Welcome, {username}.{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5) 
                writer.write(f"{DISPLAY_BYTE_ID}|Welcome Trainer ! It's time to start your journey ".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                pprint(f"Player object after registration: {player}")  # Debugging log
                game.add_player(player)
                return player
            except Exception as e:
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.WARNING}Registration failed: {str(e)}{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)  # Optional delay for better readability
                continue
            
        elif choice == "3":
            writer.close()
            await writer.wait_closed()
        else:
            # Invalid input, send the user back to the menu
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please enter 1 to Login or 2 to Register.\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5) 
            continue
    # This point should not be reached

async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    try:
        # Handle initial connection message
        initial_message = await reader.read(1024)
        initial_message = initial_message.decode().strip()
        print(f"Client chose: {initial_message}")  # Debugging log
        player = Player()
        if initial_message == "Hello|new":
            # Call the login_or_register function
            player = await login_or_register(reader, writer)
        if player is None:
            writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.FAIL}{bcolors.ENDC}\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.close()
            await writer.wait_closed()
        print (f"Zone : {player.get_zone()}")
        try :
            while True:
                if player.get_zone() == 10:
                    await handle_city_menu(reader, writer, player)
                else:
                    await handle_wild_menu(reader, writer, player)
                player = await login_or_register(reader, writer)
        except Exception as e:
            if e is ConnectionResetError or BrokenPipeError:
                print(f"Connection lost with {addr}.")
            else:
                print(f"An error occurred: {e}")
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.FAIL}An error occurred: {e}{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
        finally:
            writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.FAIL}Connection closed.{bcolors.ENDC}\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.close()
            await writer.wait_closed()

    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection lost with {addr}.")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client_msg, '10.1.2.69', 8888)
    print(f'Serving on {", ".join(str(sock.getsockname()) for sock in server.sockets)}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())