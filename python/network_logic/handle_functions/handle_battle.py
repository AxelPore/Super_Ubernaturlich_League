import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import random
from game_logic.Battle import Battle

from ..Common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID, game

@exception_handler_decorator
async def handle_duel(reader1, writer1, player1, reader2, writer2, player2):
    battle = Battle()
    await battle.set_attribute(player1, player2)

    # Send initial messages to players
    other_player_name = await player2.get_username()
    if writer1:
        writer1.write(f"{DISPLAY_BYTE_ID}|You are in battle with {other_player_name}!".encode())
        await writer1.drain()
    if writer2:
        player1_name = await player1.get_username()
        writer2.write(f"{DISPLAY_BYTE_ID}|You are in battle with {player1_name}!".encode())
        await writer2.drain()

    await asyncio.sleep(0.5)

    # Battle loop
    battle_over = False
    while not battle_over:
        action1 = False
        action2 = False
        # Send command options to players
        if writer1:
            writer1.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon".encode())
            await writer1.drain()
        if writer2:
            writer2.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon".encode())
            await writer2.drain()
        # Player 1 action
        if writer1:
            writer1.write(f"{INPUT_BYTE_ID}|Player 1, what do you want to do: ".encode())
            await writer1.drain()
        choice1 = None
        if reader1:
            choice1_raw = await reader1.read(1)
            if choice1_raw:
                try:
                    choice1 = int(choice1_raw.decode())
                except:
                    choice1 = None

        # Player 2 action
        if writer2:
            writer2.write(f"{INPUT_BYTE_ID}|Player 2, what do you want to do: ".encode())
            await writer2.drain()
        choice2 = None
        if reader2:
            choice2_raw = await reader2.read(1)
            if choice2_raw:
                try:
                    choice2 = int(choice2_raw.decode())
                except:
                    choice2 = None

        # Process player 1 action
        if choice1 == 1:
            moves = battle.pokemon_moves(1)
            move_name = list(moves.keys())
            writer1.write(f"{INPUT_BYTE_ID}|Choose a skill to use: 1. {move_name[0]} 2. {move_name[1]} 3. {move_name[2]} 4. {move_name[3]}".encode())
            await writer1.drain()
            move_choice1 = await reader1.read(1)
            move_choice1 = int(move_choice1.decode())    
            skill_name1 = move_name[move_choice1 - 1]
            move_data1 = await battle.use_skill(1, skill_name1)
            action1 = True
        elif choice1 == 2:
            for i in range(len(battle.equipe1)):
                writer1.write(f"{DISPLAY_BYTE_ID}|Choose a pokemon to switch to: {i+1}. {battle.equipe1[i].pokemon_name}".encode())
                await writer1.drain()
                await asyncio.sleep(0.5)
            writer1.write(f"{INPUT_BYTE_ID}|Choose a number:")
            await writer1.drain()
            pokemon_name1 = await reader1.read(1024)
            pokemon_name1 = pokemon_name1.decode().strip()
            await battle.changes_pokemon(1, battle.equipe1[pokemon_name1 - 1].pokemon_name)
            action1 = True

        # Process player 2 action
        if choice2 == 1:
            moves = battle.pokemon_moves(2)
            move_name = list(moves.keys())
            writer2.write(f"{INPUT_BYTE_ID}|Choose a skill to use: 1. {move_name[0]} 2. {move_name[1]} 3. {move_name[2]} 4. {move_name[3]}".encode())
            await writer2.drain()
            move_choice2 = await reader2.read(1)
            move_choice2 = int(move_choice2.decode())    
            skill_name2 = move_name[move_choice2 - 1]
            move_data2 = await battle.use_skill(2, skill_name2)
            action2 = True
        elif choice2 == 2:
            for i in range(len(battle.equipe1)):
                writer2.write(f"{DISPLAY_BYTE_ID}|Choose a pokemon to switch to: {i+1}. {battle.equipe2[i].pokemon_name}".encode())
                await writer2.drain()
                await asyncio.sleep(0.5)
            writer2.write(f"{INPUT_BYTE_ID}|Choose a number:")
            await writer2.drain()
            pokemon_name2 = await reader2.read(1024)
            pokemon_name2 = pokemon_name2.decode().strip()
            await battle.changes_pokemon(2, battle.equipe2[pokemon_name2 - 1].pokemon_name)
            action2 = True
        if action1 and action2:
            result = await battle.end_turn(move_data1, move_data2)
        writer1.write(f"{DISPLAY_BYTE_ID}|{result}".encode())
        await writer1.drain()
        writer2.write(f"{DISPLAY_BYTE_ID}|{result}".encode())
        await writer2.drain()

        # Check if battle is over
        if "a perdu" in result or battle_over:
            battle_over = True
            break

    # Battle ended message
    if writer1:
        writer1.write(f"{DISPLAY_BYTE_ID}|Battle ended.".encode())
        await writer1.drain()
    if writer2:
        writer2.write(f"{DISPLAY_BYTE_ID}|Battle ended.".encode())
        await writer2.drain()


@exception_handler_decorator
async def handle_wild_fight(reader, writer, player, wild_pokemon):
    battle = Battle()
    await battle.set_attribute(player, wild_pokemon)

    writer.write(f"{DISPLAY_BYTE_ID}|You are now in a battle against {wild_pokemon}!".encode())
    await writer.drain()
    await asyncio.sleep(0.5)

    battle_over = False
    while not battle_over:
        writer.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon \n 3. Try to catch the pokemon \n 4. Flee".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|What do you want to do: ".encode())
        await writer.drain()
        choice = await reader.read(1)
        choice = int(choice.decode())

        if choice == 4:
            flee_chance = random.random()
            if flee_chance <= 0.7:
                writer.write(f"{DISPLAY_BYTE_ID}|You successfully fled the battle.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                battle_over = True
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Flee attempt failed!".encode())
                await writer.drain()
                await asyncio.sleep(0.5)

        elif choice == 1:
            moves = battle.pokemon_moves(1)
            move_name = list(moves.keys())
            writer.write(f"{INPUT_BYTE_ID}|Choose a skill to use: 1. {move_name[0]} 2. {move_name[1]} 3. {move_name[2]} 4. {move_name[3]}".encode())
            await writer.drain()
            move_choice = await reader.read(1)
            move_choice = int(move_choice.decode())    
            skill_name = move_name[move_choice - 1]
            move_data1 = await battle.use_skill(1, skill_name)

        elif choice == 2:
            for i in range(len(battle.equipe1)):
                writer.write(f"{DISPLAY_BYTE_ID}|Choose a pokemon to switch to: {i+1}. {battle.equipe1[i].pokemon_name}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Choose a number:")
            await writer.drain()
            pokemon_name = await reader.read(1024)
            pokemon_name = pokemon_name.decode().strip()
            await battle.changes_pokemon(1, battle.equipe1[pokemon_name - 1].pokemon_name)
        
        elif choice == 4:
            writer.write(f"{DISPLAY_BYTE_ID}|You throw a pokeball at the pokemon !".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            response, success = await battle.catch_pokemon()
            writer.write(f"{DISPLAY_BYTE_ID}|{response}".encode())
            if success:
                break
            else:
                continue
        wild_move = battle.pokemon_moves(2)
        wild_move_name = list(wild_move.keys())
        wild_skill_name = wild_move_name[random.randint(0, 4)]
        move_data2 = await battle.use_skill(2, wild_skill_name)

        result = await battle.end_turn(move_data1, move_data2)
        writer.write(f"{DISPLAY_BYTE_ID}|{result}".encode())
        await writer.drain()
        await asyncio.sleep(0.5)

        if "a perdu" in result or battle_over:
            battle_over = True
            break

    writer.write(f"{DISPLAY_BYTE_ID}|Battle ended.".encode())
    await writer.drain()
    await asyncio.sleep(0.5)
