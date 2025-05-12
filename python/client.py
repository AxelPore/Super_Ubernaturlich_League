import sys
import aioconsole
import asyncio
from pathlib import Path

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

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

async def asRecieve(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        if message.startswith(INPUT_BYTE_ID):
            # Handle input request
            prompt = message.split('|', 1)[1]
            response = await aioconsole.ainput(prompt + " ")
            writer.write(response.encode())
            await writer.drain()
        elif message.startswith(DISPLAY_BYTE_ID):
            # Handle display-only message
            display_message = message.split('|', 1)[1]
            print(f"{bcolors.OKGREEN}{display_message}{bcolors.ENDC}")
        elif "ID|" in message:
            with open('/tmp/idServ', 'w+') as f:
                f.write(message.split('|')[1])
        else:
            print(f"Unknown message: {message}")

async def main():
    reader, writer = await asyncio.open_connection(host="10.1.2.69", port=8888)
    try:
        id = ''
        idFile = Path('/tmp/idServ')
        if idFile.exists():
            # Reconnecting client
            with open('/tmp/idServ', 'r') as f:
                id = f.read()
            writer.write(f"Hello|reconnect|{id}".encode())
        else:
            # New client
            writer.write("Hello|new".encode())

        await writer.drain()
        await asRecieve(reader, writer)
    except KeyboardInterrupt:
        print(bcolors.FAIL + "Application interrupted" + bcolors.ENDC)
        writer.write('&<END>'.encode())
        return
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
    print("Connection closed")
sys.exit(0)