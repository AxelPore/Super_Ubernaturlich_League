import socket
import sys
import aioconsole
import asyncio
from battle_system import Battle, Pokemon, Move, Type, Status, Weather

class BattleState:
    def __init__(self):
        self.in_battle = False
        self.battle = None
        self.active_pokemon = None
        self.opponent_pokemon = None
        self.team = []
        self.opponent_team = []

battle_state = BattleState()

def display_battle_menu():
    print("\n=== Battle Menu ===")
    print("1. Fight")
    print("2. Switch Pokemon")
    print("3. Run")
    print("4. Show Status")
    print("==================")

def display_pokemon_status(pokemon: Pokemon):
    print(f"\n{pokemon.name} (Level {pokemon.level})")
    print(f"HP: {pokemon.current_hp}/{pokemon.max_hp}")
    print(f"Status: {pokemon.status.value}")
    print("\nMoves:")
    for i, move in enumerate(pokemon.moves):
        print(f"{i+1}. {move.name} (PP: {move.pp}/{move.max_pp})")

def display_team_status(team: list[Pokemon]):
    print("\nYour Team:")
    for i, pokemon in enumerate(team):
        print(f"{i+1}. {pokemon.name} - HP: {pokemon.current_hp}/{pokemon.max_hp}")

async def handle_battle_message(message: str):
    parts = message.split('|')
    if parts[0] == "BATTLE_REQUEST":
        challenger = parts[1]
        print(f"\n{challenger} wants to battle!")
        response = await aioconsole.ainput("Accept battle? (y/n): ")
        if response.lower() == 'y':
            return f"BATTLE_ACCEPT|{challenger}"
    elif parts[0] == "BATTLE_START":
        player1, player2 = parts[1], parts[2]
        battle_state.in_battle = True
        print(f"\nBattle started between {player1} and {player2}!")
    elif parts[0] == "BATTLE_UPDATE":
        attacker, move, damage, current_hp = parts[1], parts[2], parts[3], parts[4]
        print(f"\n{attacker} used {move}!")
        print(f"It dealt {damage} damage!")
        print(f"Opponent's Pokemon has {current_hp} HP remaining!")
    elif parts[0] == "POKEMON_SWITCH":
        player, pokemon = parts[1], parts[2]
        print(f"\n{player} switched to {pokemon}!")
    elif parts[0] == "BATTLE_END":
        winner = parts[1]
        print(f"\nBattle ended! {winner} is the winner!")
        battle_state.in_battle = False
        battle_state.battle = None
    return None

async def battle_loop(writer):
    while battle_state.in_battle:
        display_battle_menu()
        choice = await aioconsole.ainput("Choose an action: ")
        
        if choice == "1":
            display_pokemon_status(battle_state.active_pokemon)
            move_choice = await aioconsole.ainput("Choose a move (1-4): ")
            try:
                move_index = int(move_choice) - 1
                if 0 <= move_index < len(battle_state.active_pokemon.moves):
                    writer.write(f"BATTLE_ACTION|{battle_state.active_pokemon.name}|MOVE|{move_index}".encode())
                    await writer.drain()
            except ValueError:
                print("Invalid move choice!")
        elif choice == "2":
            display_team_status(battle_state.team)
            switch_choice = await aioconsole.ainput("Choose a Pokemon to switch to (1-3): ")
            try:
                switch_index = int(switch_choice) - 1
                if 0 <= switch_index < len(battle_state.team):
                    writer.write(f"BATTLE_ACTION|{battle_state.active_pokemon.name}|SWITCH|{switch_index}".encode())
                    await writer.drain()
            except ValueError:
                print("Invalid Pokemon choice!")
        elif choice == "3":
            writer.write("BATTLE_ACTION|RUN".encode())
            await writer.drain()
            battle_state.in_battle = False
            break
        elif choice == "4":
            print("\nYour Pokemon:")
            display_pokemon_status(battle_state.active_pokemon)
            print("\nOpponent's Pokemon:")
            display_pokemon_status(battle_state.opponent_pokemon)
        else:
            print("Invalid choice!")

async def Input(reader, writer):
    while True:
        messages = []
        while True:
            message = await aioconsole.ainput("Message : ")
            messages.append(message)
            break
        data = '\n'.join(messages)
        writer.write(data.encode())
        await writer.drain()

async def Recieve(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        
        message = data.decode()
        if message.startswith("BATTLE_"):
            response = await handle_battle_message(message)
            if response:
                writer.write(response.encode())
                await writer.drain()
        else:
            print('\n' + f"Message du serveur : {message}")

async def main():
    reader, writer = await asyncio.open_connection(host="10.1.2.17", port=13337)
    pseudo = input("Pseudo : ")
    writer.write(("Hello|" + pseudo).encode())
    tasks = [Input(reader, writer), Recieve(reader, writer)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)