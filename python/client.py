import sys
import aioconsole
import asyncio
from pathlib import Path

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

async def asInput(r, w):
    while True:
        lines = []
        while True:
            ZaLine = await aioconsole.ainput()
            if not ZaLine:
                break
            lines.append(ZaLine)
        line = '\n'.join(lines)
        w.write(line.encode())
        await w.drain()

async def asRecieve(r, w):
    while True:
        data = await r.read(1024)
        if not data:
            break
        mess = data.decode()
        if mess.startswith('r=Ip|'):
            # Handle input byte
            prompt = mess.split('|', 1)[1]
            response = input(prompt + " ")
            w.write(response.encode())
            await w.drain()
        elif mess.startswith('r=Dp|'):
            # Handle display byte
            display_message = mess.split('|', 1)[1]
            print(f"{bcolors.OKGREEN}{display_message}{bcolors.ENDC}")
        elif "ID|" in mess:
            with open('/tmp/idServ', 'w+') as f:
                f.write(mess.split('|')[1])
        else:
            print(f"{mess}")

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
        tasks = [asInput(reader, writer), asRecieve(reader, writer)]
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print(bcolors.FAIL + "Application interrupted" + bcolors.ENDC)
        writer.write('&<END>'.encode())
        return

if __name__ == "__main__":
    asyncio.run(main())
    print("Connection closed")
sys.exit(0)