import asyncio
import random
from pprint import pprint

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
    pseudo = ''
    id = ''
    addr = writer.get_extra_info('peername')

    while True:
        data = await reader.read(1024)
        if data == b'':
            break

        message = data.decode()
        newUsr = True

        if 'Hello|' in message and len(message.split("|")) == 2:
            print('New user received')
            pseudo = message.split('|')[1]
            id = generateId(100)
            writer.write(("ID|" + id).encode())
            newUsr = True
        elif 'Hello|' in message and len(message.split("|")) == 3:
            print('Already existing user trying to reconnect')
            pseudo = message.split('|')[1]
            id = message.split('|')[2]

        if data.decode() == "&<CLEAR_CLIENTS>":
            CLIENTS.clear()
            print("All clients have been cleared.")
            writer.write("CLIENTS cleared.".encode())
            await writer.drain()
            continue

        CLIENTS[id] = {
            'w': writer,
            'r': reader,
            'LastAdress': addr,
            'pseudo': pseudo
        }

        if newUsr:
            # Example registration process
            username = await handle_input(id, "Enter your username: ")
            password = await handle_input(id, "Enter your password: ")
            print(f"Registered username: {username}, password: {password}")

        for client_id in CLIENTS.keys():
            pprint(CLIENTS)
            if newUsr:
                CLIENTS[client_id]['w'].write(
                    f"{bcolors.OKBLUE}{CLIENTS[id]['pseudo']} {bcolors.HEADER} has joined{bcolors.ENDC}".encode()
                )
                await CLIENTS[client_id]["w"].drain()
            elif client_id != id:
                CLIENTS[client_id]["w"].write(
                    f"{bcolors.OKBLUE}{CLIENTS[id]['pseudo']} {bcolors.HEADER}:> {message}{bcolors.ENDC}".encode()
                )
                await CLIENTS[client_id]["w"].drain()

async def main():
    server = await asyncio.start_server(handle_client_msg, '10.1.2.69', 8888)
    print(f'Serving on {", ".join(str(sock.getsockname()) for sock in server.sockets)}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())