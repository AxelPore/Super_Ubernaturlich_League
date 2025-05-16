import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..Common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID, game

@exception_handler_decorator
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
            from .handle_pokemart_menu import handle_pokemart_menu
            await handle_pokemart_menu(reader, writer, player)
            break
