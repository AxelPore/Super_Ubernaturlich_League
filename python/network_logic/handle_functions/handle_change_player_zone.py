import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..Common import DISPLAY_BYTE_ID, INPUT_BYTE_ID, game

async def handle_change_player_zone(reader, writer, player):
    from .handle_wild_menu import handle_wild_menu
    from .handle_city_menu import handle_city_menu
    while True:
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
        wrong = False
        addr = writer.get_extra_info('peername')
        if move in MOVES:
            if await game.player_move(addr, MOVES[move]) == False:
                writer.write(f"{DISPLAY_BYTE_ID}|You can't move in this direction.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                wrong = True
            if wrong == False:
                if await player.get_zone() == 10 :
                    writer.write(f"{DISPLAY_BYTE_ID}|You are now in the wity.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    await handle_city_menu(reader, writer, player)
                else:
                    await handle_wild_menu(reader, writer, player)
                break
            else:
                continue
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid move. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
