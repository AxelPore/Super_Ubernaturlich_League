import sys
import os

# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import aioconsole
import colorama

from network_logic.Common import INPUT_BYTE_ID, DISPLAY_BYTE_ID

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

colorama.init()

async def send_input_to_server(writer, prompt):
    """
    Handles input from the user and sends it to the server asynchronously.
    """
    response = await aioconsole.ainput(prompt + " ")  # Prompt the user for input asynchronously
    writer.write(response.encode())  # Send the response to the server
    await writer.drain()

async def asRecieve(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            print("No data received. Closing connection.")  # Debugging log
            break
        message = data.decode(errors='replace')
        if message.startswith(INPUT_BYTE_ID):
            # Handle input request
            prompt = message.split('|', 1)[1]  # Extract the prompt
            await send_input_to_server(writer, prompt)  # Send user input to the server
        elif message.startswith(DISPLAY_BYTE_ID):
            # Handle display-only message
            display_message = message.split('|', 1)[1]  # Extract the display message
            print(display_message)
        else:
            print(f"Unknown message: {message}")

async def main():
    reader, writer = await asyncio.open_connection(host="10.1.2.69", port=8888)
    try:
        writer.write("Hello|new".encode())
        await writer.drain()
        await asRecieve(reader, writer)
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nYou have been disconnected")
