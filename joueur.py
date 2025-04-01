import socket
import sys
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
        self.pseudo = None
        self.battle_queue = asyncio.Queue()
        self.input_queue = asyncio.Queue()
        self.loop = None
        self.writer = None

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

async def handle_battle_request(challenger: str):
    print(f"\n{challenger} wants to battle!")
    print("Accept battle? (y/n): ", end='', flush=True)
    response = await battle_state.input_queue.get()
    if response.lower() == 'y':
        return f"BATTLE_ACCEPT|{challenger}"
    return None

async def process_battle_messages(writer):
    while True:
        try:
            message = await battle_state.battle_queue.get()
            if message.startswith("BATTLE_REQUEST"):
                challenger = message.split('|')[1]
                response = await handle_battle_request(challenger)
                if response:
                    try:
                        writer.write(response.encode())
                        await writer.drain()
                    except Exception as e:
                        print(f"Error sending battle response: {e}")
            elif message.startswith("BATTLE_START"):
                player1, player2 = message.split('|')[1], message.split('|')[2]
                battle_state.in_battle = True
                print(f"\nBattle started between {player1} and {player2}!")
            elif message.startswith("BATTLE_UPDATE"):
                attacker, move, damage, current_hp = message.split('|')[1:]
                print(f"\n{attacker} used {move}!")
                print(f"It dealt {damage} damage!")
                print(f"Opponent's Pokemon has {current_hp} HP remaining!")
            elif message.startswith("POKEMON_SWITCH"):
                player, pokemon = message.split('|')[1:]
                print(f"\n{player} switched to {pokemon}!")
            elif message.startswith("BATTLE_END"):
                winner = message.split('|')[1]
                print(f"\nBattle ended! {winner} is the winner!")
                battle_state.in_battle = False
                battle_state.battle = None
            elif message.startswith("BATTLE_CANCELLED"):
                reason = message.split('|')[1]
                print(f"\nBattle was cancelled: {reason}")
                battle_state.in_battle = False
                battle_state.battle = None
            elif message.startswith("ERROR"):
                error_msg = message.split('|')[1]
                print(f"\nError: {error_msg}")
        except Exception as e:
            print(f"Error processing battle message: {e}")
            await asyncio.sleep(0.1)

async def battle_loop(writer):
    while battle_state.in_battle:
        try:
            display_battle_menu()
            print("Choose an action: ", end='', flush=True)
            choice = await battle_state.input_queue.get()
            
            if choice == "1":
                display_pokemon_status(battle_state.active_pokemon)
                print("Choose a move (1-4): ", end='', flush=True)
                move_choice = await battle_state.input_queue.get()
                try:
                    move_index = int(move_choice) - 1
                    if 0 <= move_index < len(battle_state.active_pokemon.moves):
                        writer.write(f"BATTLE_ACTION|{battle_state.active_pokemon.name}|MOVE|{move_index}".encode())
                        await writer.drain()
                except ValueError:
                    print("Invalid move choice!")
            elif choice == "2":
                display_team_status(battle_state.team)
                print("Choose a Pokemon to switch to (1-3): ", end='', flush=True)
                switch_choice = await battle_state.input_queue.get()
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
        except Exception as e:
            print(f"Error in battle loop: {e}")
            await asyncio.sleep(0.1)

async def handle_input():
    while True:
        try:
            message = input()
            if message.lower() == 'quit':
                sys.exit(0)
            elif message.lower().startswith('battle '):
                opponent = message[7:].strip()  # Remove 'battle ' prefix
                if opponent:
                    battle_state.writer.write(f"BATTLE_REQUEST|{battle_state.pseudo}|{opponent}".encode())
                    await battle_state.writer.drain()
                    print(f"Challenging {opponent} to a battle...")
            else:
                battle_state.writer.write(message.encode())
                await battle_state.writer.drain()
        except Exception as e:
            print(f"Error handling input: {e}")
            break

async def Recieve(reader, writer):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break
            
            message = data.decode()
            if message.startswith("BATTLE_"):
                await battle_state.battle_queue.put(message)
            else:
                print('\n' + f"Message du serveur : {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

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
    battle_state.loop = asyncio.get_event_loop()
    
    host = input("Enter server IP address (default: localhost): ").strip() or "localhost"
    port = input("Enter server port (default: 13337): ").strip() or "13337"
    
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Using default port 13337.")
        port = 13337

    try:
        reader, writer = await connect_to_server(host, port)
        battle_state.writer = writer  # Store writer in battle_state for handle_input
        battle_state.pseudo = input("Pseudo : ")
        writer.write(("Hello|" + battle_state.pseudo).encode())
        await writer.drain()
        
        print("\n=== Available Commands ===")
        print("battle <username> - Challenge a player to a battle")
        print("quit - Exit the game")
        print("========================")
        
        tasks = [
            handle_input(),
            Recieve(reader, writer),
            process_battle_messages(writer),
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