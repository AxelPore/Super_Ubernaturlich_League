import asyncio
import logging
from battle_system import Battle, Pokemon, Move, Type, Status, Weather

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

async def handle_client_msg(reader, writer):
    while True:
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')
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