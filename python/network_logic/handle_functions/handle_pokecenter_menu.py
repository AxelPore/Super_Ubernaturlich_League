import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID
from handle_team_change import handle_team_change
from handle_city_menu import handle_city_menu

@exception_handler_decorator
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
