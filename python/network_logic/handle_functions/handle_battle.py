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

    # Send command options to players
    if writer1:
        writer1.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon".encode())
        await writer1.drain()
    if writer2:
        writer2.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon".encode())
        await writer2.drain()

    # Battle loop
    battle_over = False
    while not battle_over:
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
            if writer1:
                writer1.write(f"{DISPLAY_BYTE_ID}|Choose a skill to use:".encode())
                await writer1.drain()
            skill_name1 = None
            if reader1:
                skill_name_bytes = await reader1.readline()
                skill_name1 = skill_name_bytes.decode().strip()
            if skill_name1:
                await battle.use_skill(1, skill_name1)
        elif choice1 == 2:
            if writer1:
                writer1.write(f"{DISPLAY_BYTE_ID}|Choose a pokemon to switch to:".encode())
                await writer1.drain()
            pokemon_name1 = None
            if reader1:
                pokemon_name_bytes = await reader1.readline()
                pokemon_name1 = pokemon_name_bytes.decode().strip()
            if pokemon_name1:
                await battle.changes_pokemon(1, pokemon_name1)

        # Process player 2 action
        if choice2 == 1:
            if writer2:
                writer2.write(f"{DISPLAY_BYTE_ID}|Choose a skill to use:".encode())
                await writer2.drain()
            skill_name2 = None
            if reader2:
                skill_name_bytes = await reader2.readline()
                skill_name2 = skill_name_bytes.decode().strip()
            if skill_name2:
                await battle.use_skill(2, skill_name2)
        elif choice2 == 2:
            if writer2:
                writer2.write(f"{DISPLAY_BYTE_ID}|Choose a pokemon to switch to:".encode())
                await writer2.drain()
            pokemon_name2 = None
            if reader2:
                pokemon_name_bytes = await reader2.readline()
                pokemon_name2 = pokemon_name_bytes.decode().strip()
            if pokemon_name2:
                await battle.changes_pokemon(2, pokemon_name2)

        # End turn and get result
        move_data1 = (10, 0, 0, 5)  # example dummy data
        move_data2 = (8, 0, 0, 4)   # example dummy data

        result = await battle.end_turn(move_data1, move_data2)

        # Send result messages to players
        if writer1:
            writer1.write(f"{DISPLAY_BYTE_ID}|{result}".encode())
            await writer1.drain()
        if writer2:
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

    if writer:
        writer.write(f"{DISPLAY_BYTE_ID}|You are now in a battle with {wild_pokemon}!".encode())
        await writer.drain()

    await asyncio.sleep(0.5)

    if writer:
        writer.write(f"{DISPLAY_BYTE_ID}|You can use the following commands:\n 1. Use Skill \n 2. Change Pokemon \n 3. Flee".encode())
        await writer.drain()

    battle_over = False
    while not battle_over:
        if writer:
            writer.write(f"{INPUT_BYTE_ID}|What do you want to do: ".encode())
            await writer.drain()
        choice = None
        if reader:
            choice_raw = await reader.read(1)
            if choice_raw:
                try:
                    choice = int(choice_raw.decode())
                except:
                    choice = None

        if choice == 3:
            flee_chance = random.random()
            if flee_chance <= 0.7:
                if writer:
                    writer.write(f"{DISPLAY_BYTE_ID}|You successfully fled the battle.".encode())
                    await writer.drain()
                battle_over = True
                break
            else:
                if writer:
                    writer.write(f"{DISPLAY_BYTE_ID}|Flee attempt failed!".encode())
                    await writer.drain()

        elif choice == 1:
            if writer:
                writer.write(f"{DISPLAY_BYTE_ID}|Choose a skill to use:".encode())
                await writer.drain()
            skill_name = None
            if reader:
                skill_name_bytes = await reader.readline()
                skill_name = skill_name_bytes.decode().strip()
            if skill_name:
                await battle.use_skill(1, skill_name)

        elif choice == 2:
            if writer:
                writer.write(f"{DISPLAY_BYTE_ID}|Choose a pokemon to switch to:".encode())
                await writer.drain()
            pokemon_name = None
            if reader:
                pokemon_name_bytes = await reader.readline()
                pokemon_name = pokemon_name_bytes.decode().strip()
            if pokemon_name:
                await battle.changes_pokemon(1, pokemon_name)

        # End turn and get result
        move_data1 = (10, 0, 0, 5)  # example dummy data
        move_data2 = (8, 0, 0, 4)   # example dummy data

        result = await battle.end_turn(move_data1, move_data2)

        if writer:
            writer.write(f"{DISPLAY_BYTE_ID}|{result}".encode())
            await writer.drain()

        if "a perdu" in result or battle_over:
            battle_over = True
            break

    if writer:
        writer.write(f"{DISPLAY_BYTE_ID}|Battle ended.".encode())
        await writer.drain()
