import asyncio
import logging

logger = logging.getLogger("logs")
logger.setLevel(10)
fmt = "%(levelname)8s"
fmt2 = "%(asctime)s %(levelname)8s %(message)s"

class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    white = '\x1b[38;5;255m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: "%(asctime)s" + self.grey + self.fmt + self.reset + " %(message)s",
            logging.INFO: "%(asctime)s" + self.white + self.fmt + self.reset + " %(message)s",
            logging.WARNING: "%(asctime)s" + self.yellow + self.fmt + self.reset + " %(message)s",
            logging.ERROR: "%(asctime)s" + self.red + self.fmt + self.reset + " %(message)s",
            logging.CRITICAL: "%(asctime)s" + self.bold_red + self.fmt + self.reset + " %(message)s",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

console_handler = logging.StreamHandler()
console_handler.setLevel(10)
console_handler.setFormatter(CustomFormatter(fmt))

file_handler = logging.FileHandler("bs_client.log", mode="a", encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(logging.Formatter(fmt2))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

async def listen_server(reader):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                logger.info("Server closed the connection.")
                break
            message = data.decode()
            print(f"\n[Server] {message}\n> ", end="", flush=True)
            logger.info(f"Received from server: {message}")
        except Exception as e:
            logger.error(f"Error reading from server: {e}")
            break

async def send_messages(writer, pseudo):
    print("You can start typing messages. Type 'quit' to exit.")
    while True:
        try:
            message = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            if message.lower() == "quit":
                logger.info("Quitting client.")
                writer.close()
                await writer.wait_closed()
                break
            full_message = message
            writer.write(full_message.encode())
            await writer.drain()
            logger.info(f"Sent to server: {full_message}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            break

async def main():
    host = input("Enter server host (default: 127.0.0.1): ").strip() or "127.0.0.1"
    port_input = input("Enter server port (default: 13337): ").strip() or "13337"
    try:
        port = int(port_input)
    except ValueError:
        print("Invalid port number. Using default 13337.")
        port = 13337

    pseudo = input("Enter your pseudo: ").strip()
    if not pseudo:
        print("Pseudo cannot be empty.")
        return

    try:
        reader, writer = await asyncio.open_connection(host, port)
        logger.info(f"Connected to server at {host}:{port}")

        # Send Hello message
        hello_message = f"Hello|{pseudo}"
        writer.write(hello_message.encode())
        await writer.drain()
        logger.info(f"Sent to server: {hello_message}")

        # Start listening to server messages
        listen_task = asyncio.create_task(listen_server(reader))
        # Start sending messages
        await send_messages(writer, pseudo)
        # Wait for listen task to finish
        await listen_task

    except ConnectionRefusedError:
        print(f"Could not connect to server at {host}:{port}")
        logger.error(f"Connection refused to {host}:{port}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
