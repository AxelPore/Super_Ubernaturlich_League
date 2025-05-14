import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from game_logic.Battle import Battle

from common import exception_handler_decorator, DISPLAY_BYTE_ID, game

@exception_handler_decorator
async def handle_battle(reader, writer, player, trainer):
    battle = Battle(player, trainer)
    battle.start_battle()
    writer.write(f"{DISPLAY_BYTE_ID}|You are now in a battle with {trainer}!".encode())
    await writer.drain()
    await asyncio.sleep(0.5)
