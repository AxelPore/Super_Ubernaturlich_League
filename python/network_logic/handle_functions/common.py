import asyncio
import random

global CLIENTS
CLIENTS = {}

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

from game_logic.Player import Player
from game_logic.Game import *
from game_logic.Battle import *

game = Game()

class bcolors:
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'

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
    return wrapper
