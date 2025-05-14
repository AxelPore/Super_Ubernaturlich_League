import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID

@exception_handler_decorator
async def handle_pokemart_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the Pokemart! Here are your options:\n 1. Buy items \n 2. Sell items \n 3. Check your Pokemon \n 4. Check your items \n 5. Exit Pokemart".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            from python.network_logic.handle_functions.handle_buy_items import handle_buy_items
            await handle_buy_items(reader, writer, player)
            continue
        elif choice == "2":
            from python.network_logic.handle_functions.handle_sell_items import handle_sell_items
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
            from python.network_logic.handle_functions.handle_city_menu import handle_city_menu
            await handle_city_menu(reader, writer, player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
