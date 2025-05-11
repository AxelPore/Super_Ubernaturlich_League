import sqlite3
import random

def get_pokemon_moves_and_ability(pokemon_name):
    conn = sqlite3.connect('../database.db')
    cursor = conn.cursor()
    pokemon_name = pokemon_name.lower()
    # Get Pokedexid and abilities for the given Pokémon name
    cursor.execute("""
        SELECT Pokedexid, ability_1, ability_2, ability_3
        FROM Pokedex
        WHERE name = ?
    """, (pokemon_name,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return f"Pokémon '{pokemon_name}' not found in the database."

    pokedex_id, ability_1, ability_2, ability_3 = result

    # Collect available abilities (non-null and non-empty)
    abilities = [a for a in [ability_1, ability_2, ability_3] if a and a.strip()]

    # Get all moves learned by the Pokémon
    cursor.execute("""
        SELECT Move.MoveName
        FROM Learning
        JOIN Move ON Learning.Moveid = Move.Moveid
        WHERE Learning.Pokedexid = ?
    """, (pokedex_id,))
    moves = [row[0] for row in cursor.fetchall()]

    conn.close()

    if not moves:
        return f"No moves found for Pokémon '{pokemon_name}'."

    # Select up to 4 random moves
    selected_moves = random.sample(moves, min(4, len(moves)))

    # Select one random ability
    selected_ability = random.choice(abilities) if abilities else "No ability found"

    return pokedex_id, selected_moves, selected_ability
