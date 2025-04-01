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
    elif parts[0] == "BATTLE_CANCELLED":
        reason = parts[1]
        print(f"\nBattle was cancelled: {reason}")
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

async def connect_to_server(host: str, port: int, max_retries: int = 3) -> tuple:
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to server at {host}:{port}...")
            reader, writer = await asyncio.open_connection(host=host, port=port)
            print("Successfully connected to server!")
            return reader, writer
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                print("Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                print(f"Failed to connect to server after {max_retries} attempts.")
                raise

async def main():
    # Get server address from user
    host = input("Enter server IP address (default: localhost): ").strip() or "localhost"
    port = input("Enter server port (default: 13337): ").strip() or "13337"
    
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Using default port 13337.")
        port = 13337

    try:
        reader, writer = await connect_to_server(host, port)
        pseudo = input("Pseudo : ")
        writer.write(("Hello|" + pseudo).encode())
        await writer.drain()
        
        # Create tasks for input, receive, and battle loop
        tasks = [
            Input(reader, writer),
            Recieve(reader, writer),
            battle_loop(writer)
        ]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to connect to server. Please check if the server is running and the address is correct.")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)