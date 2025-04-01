import asyncio
import logging
import socket
import sys
from battle_system import Battle, Pokemon, Move, Type, Status, Weather

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

global CLIENTS
CLIENTS = {}
global ACTIVE_BATTLES
ACTIVE_BATTLES = {}

async def handle_battle_request(reader, writer, challenger: str, opponent: str):
    if opponent in CLIENTS:
        # Send battle request to opponent
        CLIENTS[opponent]["w"].write(f"BATTLE_REQUEST|{challenger}".encode())
        await CLIENTS[opponent]["w"].drain()
        return True
    return False

async def start_battle(player1: str, player2: str):
    battle = Battle(player1, player2)
    ACTIVE_BATTLES[(player1, player2)] = battle
    
    # Initialize teams with starter Pokemon
    # Charizard
    charizard_moves = [
        Move("Flamethrower", Type.FIRE, 90, 100, 15, True),
        Move("Dragon Claw", Type.DRAGON, 80, 100, 15, True),
        Move("Air Slash", Type.FLYING, 75, 95, 15, True),
        Move("Solar Beam", Type.GRASS, 120, 100, 10, False)
    ]
    charizard = Pokemon("Charizard", 50, [Type.FIRE, Type.FLYING], {
        "HP": 78, "Attack": 84, "Defense": 78, "SpAttack": 109, "SpDefense": 85, "Speed": 100
    }, charizard_moves)

    # Blastoise
    blastoise_moves = [
        Move("Hydro Pump", Type.WATER, 110, 80, 5, False),
        Move("Ice Beam", Type.ICE, 90, 100, 10, False),
        Move("Earthquake", Type.GROUND, 100, 100, 10, True),
        Move("Flash Cannon", Type.STEEL, 80, 100, 10, False)
    ]
    blastoise = Pokemon("Blastoise", 50, [Type.WATER], {
        "HP": 79, "Attack": 83, "Defense": 100, "SpAttack": 85, "SpDefense": 105, "Speed": 78
    }, blastoise_moves)

    # Venusaur
    venusaur_moves = [
        Move("Solar Beam", Type.GRASS, 120, 100, 10, False),
        Move("Sludge Bomb", Type.POISON, 90, 100, 10, False),
        Move("Earthquake", Type.GROUND, 100, 100, 10, True),
        Move("Sleep Powder", Type.GRASS, 0, 75, 15, False, Status.ASLEEP)
    ]
    venusaur = Pokemon("Venusaur", 50, [Type.GRASS, Type.POISON], {
        "HP": 80, "Attack": 82, "Defense": 83, "SpAttack": 100, "SpDefense": 100, "Speed": 80
    }, venusaur_moves)

    # Initialize teams
    battle.initialize_teams([charizard, blastoise, venusaur], [charizard, blastoise, venusaur])
    
    # Send battle start message to both players
    for player in [player1, player2]:
        CLIENTS[player]["w"].write(f"BATTLE_START|{player1}|{player2}".encode())
        await CLIENTS[player]["w"].drain()

async def handle_battle_action(reader, writer, player: str, action: str, *args):
    # Find the battle this player is in
    battle = None
    for (p1, p2), b in ACTIVE_BATTLES.items():
        if player in [p1, p2]:
            battle = b
            break
    
    if not battle:
        return

    if action == "MOVE":
        move_index = int(args[0])
        if 0 <= move_index < len(battle.active_pokemon[player].moves):
            move = battle.active_pokemon[player].moves[move_index]
            if move.pp > 0:
                # Calculate damage
                opponent = battle.player2 if player == battle.player1 else battle.player1
                damage = battle.calculate_damage(
                    battle.active_pokemon[player],
                    battle.active_pokemon[opponent],
                    move
                )
                
                # Apply damage
                battle.active_pokemon[opponent].current_hp -= damage
                move.pp -= 1

                # Send battle update to both players
                battle_state = f"BATTLE_UPDATE|{player}|{move.name}|{damage}|{battle.active_pokemon[opponent].current_hp}"
                for p in [battle.player1, battle.player2]:
                    CLIENTS[p]["w"].write(battle_state.encode())
                    await CLIENTS[p]["w"].drain()

                # Check if battle is over
                if battle.is_battle_over():
                    winner = battle.get_winner()
                    for p in [battle.player1, battle.player2]:
                        CLIENTS[p]["w"].write(f"BATTLE_END|{winner}".encode())
                        await CLIENTS[p]["w"].drain()
                    del ACTIVE_BATTLES[(battle.player1, battle.player2)]

    elif action == "SWITCH":
        new_pokemon_index = int(args[0])
        if battle.switch_pokemon(player, new_pokemon_index):
            # Send switch confirmation to both players
            switch_msg = f"POKEMON_SWITCH|{player}|{battle.active_pokemon[player].name}"
            for p in [battle.player1, battle.player2]:
                CLIENTS[p]["w"].write(switch_msg.encode())
                await CLIENTS[p]["w"].drain()

async def cleanup_battle(battle_key: tuple):
    """Clean up a battle and notify players"""
    if battle_key in ACTIVE_BATTLES:
        battle = ACTIVE_BATTLES[battle_key]
        for player in [battle.player1, battle.player2]:
            if player in CLIENTS:
                try:
                    CLIENTS[player]["w"].write("BATTLE_CANCELLED|Connection lost".encode())
                    await CLIENTS[player]["w"].drain()
                except Exception as e:
                    logger.error(f"Error notifying player {player} of battle cancellation: {e}")
        del ACTIVE_BATTLES[battle_key]

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
        for battle_key in list(ACTIVE_BATTLES.keys()):
            await cleanup_battle(battle_key)
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