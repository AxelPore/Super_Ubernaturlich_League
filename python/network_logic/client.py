import sys
import asyncio
import aioconsole

from network_logic.Common import bcolors

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

async def send_input_to_server(writer, prompt):
    """
    Handles input from the user and sends it to the server asynchronously.
    """
    #print(f"Prompting user: {prompt}")  # Debugging log
    response = await aioconsole.ainput(prompt + " ")  # Prompt the user for input asynchronously
    #print(f"Sending input to server: {response}")  # Debugging log
    writer.write(response.encode())  # Send the response to the server
    await writer.drain()
    #print("Input sent to server.")  # Debugging log

async def asRecieve(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            print("No data received. Closing connection.")  # Debugging log
            break
        message = data.decode(errors='replace')
        #print(f"Message received from server: {message}")  # Debugging log
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
        # Send initial connection message
        print("Sending initial connection message: Hello|new")  # Debugging log
        writer.write("Hello|new".encode())
        await writer.drain()
        print("Initial connection message sent.")  # Debugging log

        # Start receiving messages from the server
        await asRecieve(reader, writer)
    except Exception as e:
        pass
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nyou have been disconnected")
