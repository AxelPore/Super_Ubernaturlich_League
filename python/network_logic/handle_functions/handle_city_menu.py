import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..common import DISPLAY_BYTE_ID, INPUT_BYTE_ID, game
from .handle_pokecenter_menu import handle_pokecenter_menu
from .handle_pokemart_menu import handle_pokemart_menu
from .handle_arena_menu import handle_arena_menu
from .handle_change_player_zone import handle_change_player_zone

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
            await handle_change_player_zone(reader, writer, player)
            continue
        elif choice == "7":
            game.remove_player(player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
