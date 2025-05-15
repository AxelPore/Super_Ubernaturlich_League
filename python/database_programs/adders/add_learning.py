import csv
import sqlite3

def verify_no_duplicate_consecutive(current_entry, last_entry):
    return current_entry != last_entry

def add_learning():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    last_entry = None

    with open('csv/learning.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pokemon_name = row['pokemon']
            move_name = row['move']

            # Get Pokedexid for the pokemon
            cursor.execute("SELECT Pokedexid FROM Pokedex WHERE name = ?", (pokemon_name,))
            pokedex_result = cursor.fetchone()
            if not pokedex_result:
                continue
            pokedex_id = pokedex_result[0]

            # Get Moveid for the move
            cursor.execute("SELECT Moveid FROM Move WHERE MoveName = ?", (move_name,))
            move_result = cursor.fetchone()
            if not move_result:
                continue
            move_id = move_result[0]

            current_entry = (pokedex_id, move_id)
            if verify_no_duplicate_consecutive(current_entry, last_entry):
                # Insert into Learning table
                cursor.execute("""
                    INSERT INTO Learning (Pokedexid, Moveid)
                    VALUES (?, ?)
                """, current_entry)
                last_entry = current_entry
            else:
                pass

    conn.commit()
    conn.close()
    print("Learning data inserted successfully.")

if __name__ == "__main__":
    add_learning()
