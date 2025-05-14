import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .common import exception_handler_decorator, DISPLAY_BYTE_ID, INPUT_BYTE_ID

@exception_handler_decorator
async def handle_team_change(reader, writer, player):
    while True:
        equipe = player.get_equipe()
        pokemon = player.get_pokemon()        
        if len(equipe) == 1:
            writer.write(f"{DISPLAY_BYTE_ID}|Here you can manage your team : \n 1. Add a Pokemon \n 2. Replace a Pokemon \n 3. Exit".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            if choice == "1":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to add: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.add_pokemon_to_team(int(choice))
            elif choice == "2":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to put instead of {equipe[0].get_name()}: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.replace_pokemon_in_team(1, int(choice))
            elif choice == "3":
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif len(equipe) == 4:
            writer.write(f"{DISPLAY_BYTE_ID}|Here you can manage your team : \n 1. Replace a Pokemon \n 2. Remove a Pokemon \n 3. Exit".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            if choice == "1":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to replace: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                choice2 = 0
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to put instead of {equipe[int(choice)-1].get_name()}: ".encode())
                    await writer.drain()
                    choice2 = await reader.read(1024)
                    choice2 = choice2.decode().strip()
                player.replace_pokemon_in_team(int(choice), int(choice2))
            elif choice == "2":
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to remove: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.remove_pokemon_to_team(int(choice))
            elif choice == "3":
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Here you can manage your team : \n 1. Add a Pokemon \n 2. Replace a Pokemon \n 3. Remove a Pokemon \n 4. Exit".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            if choice == "1":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to add: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.add_pokemon_to_team(int(choice))
            elif choice == "2":
                if len(pokemon) == 0:
                    writer.write(f"{DISPLAY_BYTE_ID}|You don't have any Pokemon in your PC.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    break
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to replace: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                writer.write(f"{DISPLAY_BYTE_ID}|Here are the available Pokemon: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                choice2 = 0
                for i in range(len(pokemon)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {pokemon[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to put instead of {equipe[int(choice)-1].get_name()}: ".encode())
                    await writer.drain()
                    choice2 = await reader.read(1024)
                    choice2 = choice2.decode().strip()
                player.replace_pokemon_in_team(int(choice), int(choice2))
            elif choice == "3":
                writer.write(f"{DISPLAY_BYTE_ID}|Here is your team: \n".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                for i in range(len(equipe)):
                    writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].get_name()}".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    writer.write(f"{INPUT_BYTE_ID}|Enter the number of the Pokemon you want to remove: ".encode())
                    await writer.drain()
                    choice = await reader.read(1024)
                    choice = choice.decode().strip()
                player.remove_pokemon_to_team(int(choice))
            elif choice == "4":
                break
            else:
                writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
