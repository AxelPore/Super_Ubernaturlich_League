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

file_handler = logging.FileHandler("/var/log/bs_server/bs_server.log", mode="a", encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(logging.Formatter(fmt2))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

global CLIENTS
CLIENTS = {}


async def handle_client_msg(reader, writer):
    while True:
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')
        if data == b'':
            break

        message = data.decode()
        if 'Hello|' in message :
            pseudo = message.split('|')[1]  
        logger.info(f"{pseudo} ({addr[0]}) s'est connecté.")
        CLIENTS[addr] = {}
        CLIENTS[addr]['w'] = writer
        CLIENTS[addr]['r'] = reader
        CLIENTS[addr]['pseudo'] = pseudo
        
        
        for addrs in CLIENTS.keys():
            if addrs[0] != addr[0] :
                CLIENTS[addrs]["w"].write(f"Annonce : {pseudo} a rejoint la chatroom".encode())
                await CLIENTS[addrs]["w"].drain()


        for addrs in CLIENTS.keys():
            if addrs[0] != addr[0] and 'Hello|' not in message :
                List = message.split("\n")
                IP = addr[0].replace("'", "")
                CLIENTS[addrs]["w"].write(f"{pseudo} a dit : {List[0]}".encode())
                await CLIENTS[addrs]["w"].drain()
                logger.info(f"Le client {pseudo} a envoyé \"{message}\".")
                logger.info(f"Message envoyé aux autre utilisateur.")


async def main():
    server = await asyncio.start_server(handle_client_msg, '10.1.2.17', 13337)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logger.info(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())