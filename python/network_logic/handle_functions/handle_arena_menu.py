import asyncio
import random

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..Common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID, game

@exception_handler_decorator
async def handle_arena_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the arena!".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{DISPLAY_BYTE_ID}|Here are your options:\n 1. Fight another trainer in the Arena \n 2. Check your Pokemon \n 3. Check your items \n 4. Exit".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        await writer.drain()
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            writer.write(f"{DISPLAY_BYTE_ID}|Here are the trainers nearby:\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            number_of_trainers = random.randint(1, 5)
            game.generate_trainer(number_of_trainers, player.get_zone())
            get_trainer = game.zone_check()
            for k, v in get_trainer.items():
                if v == player.get_zone():
                    writer.write(f"{DISPLAY_BYTE_ID}|{k} is nearby.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the trainer you want to fight: ".encode())
                    await writer.drain()
                    trainer = await reader.read(1024)
                    trainer = trainer.decode().strip()
                    from handle_battle import handle_battle
                    await handle_battle(reader, writer, player, trainer)
                else:
                    writer.write(f"{DISPLAY_BYTE_ID}|No trainers nearby.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
            continue
        elif choice == "2":
            equipe = player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].get_moves()}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "3":
            items = player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "4":
            writer.write(f"{DISPLAY_BYTE_ID}|You are now in the city.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            from handle_city_menu import handle_city_menu
            await handle_city_menu(reader, writer, player)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
