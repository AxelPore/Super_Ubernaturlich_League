import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .common import INPUT_BYTE_ID, DISPLAY_BYTE_ID, bcolors
from game_logic.Player import Player
from .common import game
from pprint import pprint
import asyncio

async def handle_login(reader, writer):
    while True:
        writer.write(f"{INPUT_BYTE_ID}|{bcolors.OKCYAN}Welcome! Do you want to (1) Login, (2) Register or (3) Quit? {bcolors.ENDC}".encode())
        await writer.drain()
        choice = await reader.read(1024)
        print(f"Raw data received: {choice}")  # Debugging log
        choice = choice.decode().strip()
        print(f"Client chose: {choice}")  # Debugging log

        if choice == "1":
            # Handle login
            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter your username: {bcolors.ENDC}".encode())
            await writer.drain()
            username = await reader.read(1024)
            username = username.decode().strip()
            print(f"Received username for login: {username}")  # Debugging log

            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter your password: {bcolors.ENDC}".encode())
            await writer.drain()
            password = await reader.read(1024)
            password = password.decode().strip()
            print(f"Received password for login: {password}")  # Debugging log

            player = Player()
            if player.login(username, password):
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.OKGREEN}Login successful! Welcome, {username}.{bcolors.ENDC}\n".encode())
                await writer.drain()
                writer.write(f"{DISPLAY_BYTE_ID}|Welcome Trainer ! It's time to start your journey ".encode())
                await writer.drain()
                await asyncio.sleep(0.5) 
                pprint(f"Player object after registration: {player}")  # Debugging log
                game.add_player(player)
                return player
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.WARNING}Login failed or account not found. Please try again or Register.{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                continue

        elif choice == "2":
            # Handle registration
            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter a username to register: {bcolors.ENDC}".encode())
            await writer.drain()
            username = await reader.read(1024)
            username = username.decode().strip()
            print(f"Received username for registration: {username}")  # Debugging log

            writer.write(f"{INPUT_BYTE_ID}|{bcolors.HEADER}Enter a password to register: {bcolors.ENDC}".encode())
            await writer.drain()
            password = await reader.read(1024)
            password = password.decode().strip()
            print(f"Received password for registration: {password}")  # Debugging log

            STARTER_POKEMONS = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee", "Chikorita", "Cyndaquil", "Totodile", "Treecko", "Torchic", "Mudkip", "Turtwig", "Chimchar", "Piplup", "Snivy", "Tepig", "Oshawott", "Chespin", "Fennekin", "Froakie", "Rowlet", "Litten", "Popplio", "Grookey", "Scorbunny", "Sobble", "Sprigatito", "Fuecoco", "Quaxly"]
            writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.BOLD}Here is a list of Pokemon starters : {bcolors.ENDC}\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)

            for i in range (len(STARTER_POKEMONS)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {STARTER_POKEMONS[i]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)  # Optional delay for better readability

            writer.write(f"{INPUT_BYTE_ID}|\n{bcolors.HEADER}Choose a pokemon starter: {bcolors.ENDC}".encode())
            await writer.drain()
            starter = await reader.read(1024)
            starter = starter.decode().strip()
            starter = {
                1: 1,
                2: 4,
                3: 7,
                4: 25,
                5: 133,
                6: 152,
                7: 155,
                8: 158,
                9: 252,
                10: 255,
                11: 258,
                12: 387,
                13: 390,
                14: 393,
                15: 495,
                16: 498,
                17: 501,
                18: 650,
                19: 653,
                20: 656,
                21: 722,
                22: 725,
                23: 728,
                24: 810,
                25: 813,
                26: 816,
                27: 906,
                28: 909,
                29: 912,
            }.get(int(starter), 1)  # Default to Bulbasaur if invalid choice
            print(f"Received starter choice: {starter}")  # Debugging log

            player = Player()
            try:
                print(f"Attempting to register user: {username} with password: {password} and starter: {starter}")  # Debugging log
                player.register(username, password, starter)
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.OKGREEN}Registration successful! Welcome, {username}.{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5) 
                writer.write(f"{DISPLAY_BYTE_ID}|Welcome Trainer ! It's time to start your journey ".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                pprint(f"Player object after registration: {player}")  # Debugging log
                game.add_player(player)
                return player
            except Exception as e:
                writer.write(f"{DISPLAY_BYTE_ID}|{bcolors.WARNING}Registration failed: {str(e)}{bcolors.ENDC}\n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)  # Optional delay for better readability
                continue

        elif choice == "3":
            writer.close()
            await writer.wait_closed()
        else:
            # Invalid input, send the user back to the menu
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please enter 1 to Login or 2 to Register.\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5) 
            continue
    # This point should not be reached
