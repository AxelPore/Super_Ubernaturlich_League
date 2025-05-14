import asyncio

async def clear_clients():
    host = "10.1.2.69"  # Replace with the server's IP address
    port = 8888         # Replace with the server's port

    try:
        reader, writer = await asyncio.open_connection(host=host, port=port)

        # Send a special command to clear all data in CLIENTS
        clear_command = "&<CLEAR_CLIENTS>"
        writer.write(clear_command.encode())
        await writer.drain()

        print("Clear command sent to the server.")

        # Wait for response (optional)
        response = await reader.read(1024)
        print("Server response:", response.decode())

        writer.close()
        await writer.wait_closed()

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    asyncio.run(clear_clients())