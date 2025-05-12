import asyncio
import random
from pprint import pprint
from Player import Player

global CLIENTS
CLIENTS = {}

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

def generateId(lenght):
    id = ''
    while lenght > 8:
        comp = 9
        if lenght <= 9:
            comp = lenght
        id += str(hex(random.randrange(1, 10**(comp))))[2:]
        lenght -= 9
    return id

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

async def handle_input(client_id, message):
    writer = CLIENTS[client_id]['w']
    reader = CLIENTS[client_id]['r']
    writer.write(f"{INPUT_BYTE_ID}|{message}".encode())
    await writer.drain()
    data = await reader.read(1024)
    return data.decode()

async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    try:
        # Handle initial connection message
        initial_message = await reader.read(1024)
        initial_message = initial_message.decode().strip()
        print(f"Client chose: {initial_message}")  # Debugging log

        if initial_message == "Hello|new":
            # Proceed to login/register menu
            while True:
                writer.write(f"{DISPLAY_BYTE_ID}|Welcome! Do you want to (1) Login or (2) Register? ".encode())
                await writer.drain()
                choice = await reader.read(1024)
                choice = choice.decode().strip()
                print(f"Client chose: {choice}")  # Debugging log

                if choice == "1":
                    # Handle login
                    writer.write(f"{INPUT_BYTE_ID}|Enter your username: ".encode())
                    await writer.drain()
                    username = await reader.read(1024)
                    username = username.decode().strip()
                    print(f"Received username for login: {username}")  # Debugging log

                    writer.write(f"{INPUT_BYTE_ID}|Enter your password: ".encode())
                    await writer.drain()
                    password = await reader.read(1024)
                    password = password.decode().strip()
                    print(f"Received password for login: {password}")  # Debugging log

                    player = Player(username, password)
                    if player.login(username, password):
                        writer.write(f"{DISPLAY_BYTE_ID}|Login successful! Welcome, {username}.\n".encode())
                        await writer.drain()
                        break  # Exit the loop after successful login
                    else:
                        writer.write(f"{DISPLAY_BYTE_ID}|Login failed. Please try again.\n".encode())
                        await writer.drain()

                elif choice == "2":
                    # Handle registration
                    writer.write(f"{INPUT_BYTE_ID}|Enter a username to register: ".encode())
                    await writer.drain()
                    username = await reader.read(1024)
                    username = username.decode().strip()
                    print(f"Received username for registration: {username}")  # Debugging log

                    writer.write(f"{INPUT_BYTE_ID}|Enter a password to register: ".encode())
                    await writer.drain()
                    password = await reader.read(1024)
                    password = password.decode().strip()
                    print(f"Received password for registration: {password}")  # Debugging log

                    player = Player(username, password)
                    try:
                        player.register(username, password)
                        writer.write(f"{DISPLAY_BYTE_ID}|Registration successful! Welcome, {username}.\n".encode())
                        await writer.drain()
                        break  # Exit the loop after successful registration
                    except Exception as e:
                        writer.write(f"{DISPLAY_BYTE_ID}|Registration failed: {str(e)}\n".encode())
                        await writer.drain()

                else:
                    # Invalid input, send the user back to the menu
                    writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please enter 1 to Login or 2 to Register.\n".encode())
                    await writer.drain()

    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection lost with {addr}.")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client_msg, '10.1.2.69', 8888)
    print(f'Serving on {", ".join(str(sock.getsockname()) for sock in server.sockets)}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())