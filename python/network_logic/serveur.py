import sys
import os

# Add the `python` directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import random
from pprint import pprint

from game_logic.Player import Player
from network_logic.Common import CLIENTS, INPUT_BYTE_ID, DISPLAY_BYTE_ID, game, bcolors, exception_handler_decorator
from network_logic.handle_functions.handle_battle import handle_battle
from network_logic.handle_functions.handle_arena_menu import handle_arena_menu
from network_logic.handle_functions.handle_buy_items import handle_buy_items
from network_logic.handle_functions.handle_sell_items import handle_sell_items
from network_logic.handle_functions.handle_pokemart_menu import handle_pokemart_menu
from network_logic.handle_functions.handle_pokecenter_menu import handle_pokecenter_menu
from network_logic.handle_functions.handle_change_player_zone import handle_change_player_zone
from network_logic.handle_functions.handle_wild_menu import handle_wild_menu
from network_logic.handle_functions.handle_city_menu import handle_city_menu
from network_logic.handle_functions.handle_team_change import handle_team_change
from network_logic.handle_functions.handle_login import handle_login

def generateId(lenght):
    id = ''
    while lenght > 8:
        comp = 9
        if lenght <= 9:
            comp = lenght
        id += str(hex(random.randrange(1, 10**(comp))))[2:]
        lenght -= 9
    return id

async def handle_input(client_id, message):
    writer = CLIENTS[client_id]['w']
    reader = CLIENTS[client_id]['r']
    writer.write(f"{INPUT_BYTE_ID}|{message}".encode())
    await writer.drain()
    data = await reader.read(1024)
    return data.decode()

@exception_handler_decorator
async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    try:
        # Handle initial connection message
        initial_message = await reader.read(1024)
        initial_message = initial_message.decode().strip()
        print(f"Client chose: {initial_message}")  # Debugging log
        player = Player()
        if initial_message == "Hello|new":
            # Call the login_or_register function
            player = await handle_login(reader, writer)
        if player is None:
            writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.FAIL}{bcolors.ENDC}\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.close()
            await writer.wait_closed()
        print (f"Zone : {player.get_zone()}")

        while True:
            if player.get_zone() == 10:
                await handle_city_menu(reader, writer, player)
            else:
                await handle_wild_menu(reader, writer, player)
            player = await handle_login(reader, writer)

    except (KeyboardInterrupt, ConnectionResetError, BrokenPipeError) as e:
        # Suppress error messages for broken pipe and connection reset
        if isinstance(e, BrokenPipeError) or isinstance(e, ConnectionResetError) or isinstance(e, KeyboardInterrupt):
            print(f"Connection lost with {addr}.")
        else:
            raise
    finally:
        try:
            writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.FAIL}Connection closed.{bcolors.ENDC}\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
        except Exception:
            pass
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

async def main():
    server = await asyncio.start_server(handle_client_msg, '10.1.2.69', 8888)
    print(f'Serving on {", ".join(str(sock.getsockname()) for sock in server.sockets)}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())