import asyncio
import random

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..Common import DISPLAY_BYTE_ID, INPUT_BYTE_ID, game
from .handle_battle import handle_battle
from .handle_change_player_zone import handle_change_player_zone

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
            await handle_change_player_zone(reader, writer, player)
            continue
        elif choice == "6":
            addr = writer.get_extra_info('peername')
            game.remove_player(addr)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
