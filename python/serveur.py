import asyncio
import logging
import socket
import sys

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

file_handler = logging.FileHandler("bs_server.log", mode="a", encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(logging.Formatter(fmt2))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Global dictionaries to manage clients and active battles
CLIENTS = {}
ACTIVE_BATTLES = {}

async def handle_battle_request(reader, writer, challenger, opponent):
    logger.info(f"Battle request from {challenger} to {opponent}")
    # Check if both players are connected
    challenger_addr = None
    opponent_addr = None
    for addr, info in CLIENTS.items():
        if info.get('pseudo') == challenger:
            challenger_addr = addr
        if info.get('pseudo') == opponent:
            opponent_addr = addr
    if not challenger_addr or not opponent_addr:
        logger.warning("One or both players not connected")
        return False
    # Check if either player is already in a battle
    for (p1, p2) in ACTIVE_BATTLES.keys():
        if challenger in (p1, p2) or opponent in (p1, p2):
            logger.warning("One or both players already in a battle")
            return False
    # Register the battle
    ACTIVE_BATTLES[(challenger, opponent)] = {
        'turn': challenger,
        'state': 'initialized',
        'log': []
    }
    # Notify opponent of battle request
    opponent_writer = CLIENTS[opponent_addr]['w']
    opponent_writer.write(f"BATTLE_REQUEST|{challenger}|{opponent}".encode())
    await opponent_writer.drain()
    logger.info(f"Battle request sent to {opponent}")
    return True

async def start_battle(challenger, opponent):
    logger.info(f"Starting battle between {challenger} and {opponent}")
    battle_key = (challenger, opponent)
    if battle_key not in ACTIVE_BATTLES:
        logger.error("Battle not found in active battles")
        return
    ACTIVE_BATTLES[battle_key]['state'] = 'started'
    # Notify both players that battle has started
    for addr, info in CLIENTS.items():
        if info and 'pseudo' in info and info['pseudo'] in battle_key:
            info['w'].write(f"BATTLE_START|{challenger}|{opponent}".encode())
            await info['w'].drain()
    logger.info("Battle started notifications sent")

async def handle_battle_action(reader, writer, player, action, *args):
    logger.info(f"Battle action from {player}: {action} {args}")
    # Find the battle the player is in
    battle_key = None
    for (p1, p2) in ACTIVE_BATTLES.keys():
        if player in (p1, p2):
            battle_key = (p1, p2)
            break
    if not battle_key:
        logger.warning(f"Player {player} not in any active battle")
        return
    # Process action (stub)
    ACTIVE_BATTLES[battle_key]['log'].append((player, action, args))
    # Notify the other player of the action
    other_player = battle_key[1] if battle_key[0] == player else battle_key[0]
    other_addr = None
    for addr, info in CLIENTS.items():
        if info and 'pseudo' in info and info['pseudo'] == other_player:
            other_addr = addr
            break
    if other_addr:
        CLIENTS[other_addr]['w'].write(f"BATTLE_ACTION|{player}|{action}|{'|'.join(args)}".encode())
        await CLIENTS[other_addr]['w'].drain()
    logger.info(f"Battle action forwarded to {other_player}")

async def cleanup_battle(battle_key):
    logger.info(f"Cleaning up battle {battle_key}")
    if battle_key in ACTIVE_BATTLES:
        del ACTIVE_BATTLES[battle_key]
    # Notify players battle ended
    for addr, info in CLIENTS.items():
        if info and 'pseudo' in info and info['pseudo'] in battle_key:
            try:
                info['w'].write(f"BATTLE_END|{battle_key[0]}|{battle_key[1]}".encode())
                await info['w'].drain()
            except Exception as e:
                logger.error(f"Error notifying player {info.get('pseudo')} about battle end: {e}")

async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    try:
        while True:
            data = await reader.read(1024)
            if data == b'':
                break

            message = data.decode()
            if 'Hello|' in message:
                pseudo = message.split('|')[1]
                logger.info(f"{pseudo} ({addr[0]}) s'est connecté.")
                CLIENTS[addr] = {}
                CLIENTS[addr]['w'] = writer
                CLIENTS[addr]['r'] = reader
                CLIENTS[addr]['pseudo'] = pseudo
                
                for addrs in CLIENTS.keys():
                    if addrs[0] != addr[0]:
                        CLIENTS[addrs]["w"].write(f"Annonce : {pseudo} a rejoint la chatroom".encode())
                        await CLIENTS[addrs]["w"].drain()
            else:
                # Handle battle-related messages
                parts = message.split('|')
                if parts[0] == "BATTLE_REQUEST":
                    challenger = parts[1]
                    opponent = parts[2]
                    if await handle_battle_request(reader, writer, challenger, opponent):
                        await start_battle(challenger, opponent)
                elif parts[0] == "BATTLE_ACTION":
                    player = parts[1]
                    action = parts[2]
                    args = parts[3:]
                    await handle_battle_action(reader, writer, player, action, *args)
                else:
                    # Handle regular chat messages
                    for addrs in CLIENTS.keys():
                        if addrs[0] != addr[0]:
                            List = message.split("\n")
                            IP = addr[0].replace("'", "")
                            CLIENTS[addrs]["w"].write(f"{CLIENTS[addr]['pseudo']} a dit : {List[0]}".encode())
                            await CLIENTS[addrs]["w"].drain()
                            logger.info(f"Le client {CLIENTS[addr]['pseudo']} a envoyé \"{message}\".")
                            logger.info(f"Message envoyé aux autre utilisateur.")
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        # Clean up any battles this client was involved in
        if addr in CLIENTS:
            pseudo = CLIENTS[addr]['pseudo']
            battles_to_cleanup = []
            for (p1, p2) in ACTIVE_BATTLES.keys():
                if pseudo in [p1, p2]:
                    battles_to_cleanup.append((p1, p2))
            
            for battle_key in battles_to_cleanup:
                await cleanup_battle(battle_key)
            
            del CLIENTS[addr]
        writer.close()
        await writer.wait_closed()

async def main():
    # Get server configuration from user
    host = input("Enter host address (default: 0.0.0.0): ").strip() or "0.0.0.0"
    port = input("Enter port (default: 13337): ").strip() or "13337"
    
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Using default port 13337.")
        port = 13337

    try:
        server = await asyncio.start_server(handle_client_msg, host, port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        logger.info(f'Serving on {addrs}')
        
        async with server:
            await server.serve_forever()
    except Exception as e:
        logger.error(f"Server error: {e}")
        # Clean up all active battles on server shutdown
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)

async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    try:
        while True:
            data = await reader.read(1024)
            if data == b'':
                break

            message = data.decode()
            if 'Hello|' in message:
                pseudo = message.split('|')[1]
                logger.info(f"{pseudo} ({addr[0]}) s'est connecté.")
                CLIENTS[addr] = {}
                CLIENTS[addr]['w'] = writer
                CLIENTS[addr]['r'] = reader
                CLIENTS[addr]['pseudo'] = pseudo
                
                for addrs in CLIENTS.keys():
                    if addrs[0] != addr[0]:
                        CLIENTS[addrs]["w"].write(f"Annonce : {pseudo} a rejoint la chatroom".encode())
                        await CLIENTS[addrs]["w"].drain()
            else:
                # Handle battle-related messages
                parts = message.split('|')
                if parts[0] == "BATTLE_REQUEST":
                    challenger = parts[1]
                    opponent = parts[2]
                    if await handle_battle_request(reader, writer, challenger, opponent):
                        await start_battle(challenger, opponent)
                elif parts[0] == "BATTLE_ACTION":
                    player = parts[1]
                    action = parts[2]
                    args = parts[3:]
                    await handle_battle_action(reader, writer, player, action, *args)
                else:
                    # Handle regular chat messages
                    for addrs in CLIENTS.keys():
                        if addrs[0] != addr[0]:
                            List = message.split("\n")
                            IP = addr[0].replace("'", "")
                            CLIENTS[addrs]["w"].write(f"{CLIENTS[addr]['pseudo']} a dit : {List[0]}".encode())
                            await CLIENTS[addrs]["w"].drain()
                            logger.info(f"Le client {CLIENTS[addr]['pseudo']} a envoyé \"{message}\".")
                            logger.info(f"Message envoyé aux autre utilisateur.")
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        # Clean up any battles this client was involved in
        if addr in CLIENTS:
            pseudo = CLIENTS[addr]['pseudo']
            battles_to_cleanup = []
            for (p1, p2) in ACTIVE_BATTLES.keys():
                if pseudo in [p1, p2]:
                    battles_to_cleanup.append((p1, p2))
            
            for battle_key in battles_to_cleanup:
                await cleanup_battle(battle_key)
            
            del CLIENTS[addr]
        writer.close()
        await writer.wait_closed()

async def main():
    # Get server configuration from user
    host = input("Enter host address (default: 0.0.0.0): ").strip() or "0.0.0.0"
    port = input("Enter port (default: 13337): ").strip() or "13337"
    
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Using default port 13337.")
        port = 13337

    try:
        server = await asyncio.start_server(handle_client_msg, host, port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        logger.info(f'Serving on {addrs}')
        
        async with server:
            await server.serve_forever()
    except Exception as e:
        logger.error(f"Server error: {e}")
        # Clean up all active battles on server shutdown
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0) 