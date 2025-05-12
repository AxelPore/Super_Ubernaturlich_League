import sys
import aioconsole
import asyncio

INPUT_BYTE_ID = 'r=Ip'
DISPLAY_BYTE_ID = 'r=Dp'

async def send_input_to_server(writer, prompt):
    """
    Handles input from the user and sends it to the server.
    """
    response = await aioconsole.ainput(prompt + " ")  # Prompt the user for input
    print(f"Sending input to server: {response}")  # Debugging log
    writer.write(response.encode())  # Send the response to the server
    await writer.drain()

async def asRecieve(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
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
        writer.write("Hello|new".encode())
        await writer.drain()

        # Start receiving messages from the server
        await asRecieve(reader, writer)
    except KeyboardInterrupt:
        print("Client interrupted.")
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())