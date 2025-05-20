import asyncio
import random
import aiosqlite
from game_logic.Player import Player
from game_logic.Pokemon import Pokemon
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..Common import DISPLAY_BYTE_ID, INPUT_BYTE_ID, game, CLIENTS
from .handle_battle import handle_wild_fight, handle_duel
from .handle_change_player_zone import handle_change_player_zone

async def handle_wild_menu(reader, writer, player):
    while True:
        writer.write(f"{DISPLAY_BYTE_ID}|Welcome to the wild! You are in the {await player.zone_name()} Here are your options:\n 1. Find and fight a wild Pokemon \n 2. Fight another trainer nearby \n 3. Check your Pokemon \n 4. Check your items \n 5. Explore somewhere else \n 6. Go back to the main menu \n".encode())
        await writer.drain()
        await asyncio.sleep(0.5)
        writer.write(f"{INPUT_BYTE_ID}|Enter the number of your choice: ".encode())
        await writer.drain()
        choice = await reader.read(1024)
        choice = choice.decode().strip()
        if choice == "1":
            async with aiosqlite.connect('database.db') as conn:
                cursor = await conn.execute("SELECT Pokedexid FROM Pokedex WHERE Zoneid = ?", (await player.get_zoneid(),))
                spawnable_pokemons = await cursor.fetchall()
                place_holder = Player()
                place_holder.equipe.append(Pokemon(spawnable_pokemons[random.randint(0, len(spawnable_pokemons) - 1)][0]))
            writer.write(f"{DISPLAY_BYTE_ID}|You encountered a wild Pokemon!".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            await handle_wild_fight(reader, writer, player, place_holder)
            await player.reset_equipe()
            continue
        elif choice == "2":
            writer.write(f"{DISPLAY_BYTE_ID}|Here are the trainers nearby:\n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            # Find all players in the same zone
            current_zone = await player.get_zone()
            nearby_players = []
            for client_id, client_info in CLIENTS.items():
                if 'pseudo' in client_info and client_info['pseudo'] != await player.get_username():
                    # We need to get the player's zone for this client
                    # Since we don't have player object here, we check game.players or similar
                    # Assuming game.players is a dict of player objects keyed by pseudo or client_id
                    # We will try to find the player object by pseudo
                    for p, v in game.players.items():
                        print (p, v)
                        if v.username == client_info['pseudo']:
                            if await v.get_zone() == current_zone:
                                nearby_players.append(client_info['pseudo'])
            if not nearby_players:
                writer.write(f"{DISPLAY_BYTE_ID}|No trainers nearby.".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
                continue
            # List nearby players
            for idx, pseudo in enumerate(nearby_players):
                writer.write(f"{DISPLAY_BYTE_ID}|{idx + 1}. {pseudo}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            writer.write(f"{INPUT_BYTE_ID}|Enter the number of the trainer you want to fight: ".encode())
            await writer.drain()
            choice = await reader.read(1024)
            choice = choice.decode().strip()
            try:
                choice_idx = int(choice) - 1
                if choice_idx < 0 or choice_idx >= len(nearby_players):
                    writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    continue
                opponent_pseudo = nearby_players[choice_idx]
                # Find opponent's reader and writer
                opponent_reader = None
                opponent_writer = None
                for client_id, client_info in CLIENTS.items():
                    if client_info.get('pseudo') == opponent_pseudo:
                        opponent_reader = client_info['r']
                        opponent_writer = client_info['w']
                        break
                if opponent_reader is None or opponent_writer is None:
                    writer.write(f"{DISPLAY_BYTE_ID}|Opponent not found.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
                    continue
                # Send challenge request to opponent
                opponent_writer.write(f"{DISPLAY_BYTE_ID}|You have been challenged to a battle by {await player.get_username()}. Accept? (yes/no)".encode())
                await opponent_writer.drain()
                response = await opponent_reader.read(1024)
                response = response.decode().strip().lower()
                player2 = None
                for p , v in game.players.items():
                        if v.username == opponent_pseudo:
                            player2 = v
                            break
                if response == "yes":
                    await handle_duel(reader, writer, player, opponent_reader, opponent_writer, player2)
                else:
                    writer.write(f"{DISPLAY_BYTE_ID}|Challenge declined.".encode())
                    await writer.drain()
                    await asyncio.sleep(0.5)
            except Exception as e:
                writer.write(f"{DISPLAY_BYTE_ID}|Error: {str(e)}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "3":
            equipe = await player.get_equipe()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Pokemons: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(equipe)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {equipe[i].pokemon_name} : {equipe[i].hp}/{equipe[i].hp_max}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "4":
            items = await player.get_item()
            writer.write(f"{DISPLAY_BYTE_ID}|Here are your Items: \n".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            for i in range(len(items)):
                writer.write(f"{DISPLAY_BYTE_ID}|{i+1}. {items[i][0]} : {items[i][1]}".encode())
                await writer.drain()
                await asyncio.sleep(0.5)
            continue
        elif choice == "5":
            await handle_change_player_zone(reader, writer, player)
            continue
        elif choice == "6":
            addr = writer.get_extra_info('peername')
            game.remove_player(addr)
            break
        else:
            writer.write(f"{DISPLAY_BYTE_ID}|Invalid choice. Please try again.".encode())
            await writer.drain()
            await asyncio.sleep(0.5)
            continue
