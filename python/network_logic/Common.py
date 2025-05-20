import asyncio
import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_logic.Player import Player
from game_logic.Game import Game
from game_logic.Battle import Battle

import asyncio

global CLIENTS
CLIENTS = {}

def create_client_entry(reader, writer, pseudo=None):
    return {
        'r': reader,
        'w': writer,
        'pseudo': pseudo,
        'lock': asyncio.Lock()
    }

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

game = Game()

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

# rename

def exception_handler_decorator(func):
    async def wrapper(reader, writer, *args, **kwargs):
        addr = writer.get_extra_info('peername')
        try:
            return await func(reader, writer, *args, **kwargs)
        except (KeyboardInterrupt, ConnectionResetError, BrokenPipeError):
            print(f"Connection lost with {addr}.")
            try:
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.FAIL}Connection closed.{bcolors.ENDC}\\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            except Exception:
                pass
            writer.close()
            await writer.wait_closed()
            game.remove_player(addr)
    return wrapper

def get_client_id_by_username(username: str):
    for client_id, client_info in CLIENTS.items():
        if client_info.get('pseudo') == username:
            return client_id
    return None
