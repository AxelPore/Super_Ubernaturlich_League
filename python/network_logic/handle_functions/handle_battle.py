import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from game_logic.Battle import Battle

from ..Common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID, game

@exception_handler_decorator
async def handle_battle(reader, writer, player, trainer):
    battle = Battle()
    battle.set_attribute(player, trainer)
    writer.write(f"{DISPLAY_BYTE_ID}|You are now in a battle with {trainer}!".encode())
    await writer.drain()
    await asyncio.sleep(0.5)
    writer.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon".encode())
    await writer.drain()
    await asyncio.sleep(0.5)
    writer.write(f"{INPUT_BYTE_ID}|What do you want to do :".encode())
    await writer.drain()
    choice = await reader.read(1)
    choice = int(choice.decode())
    if choice == 1:
        pass
    
