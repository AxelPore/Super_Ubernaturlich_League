import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..Common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID, game

@exception_handler_decorator
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
            from python.network_logic.handle_functions.handle_pokemart_menu import handle_pokemart_menu
            await handle_pokemart_menu(reader, writer, player)
            break
