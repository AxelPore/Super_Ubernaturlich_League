import csv
import sqlite3

def str_to_bool(s):
    return 1 if s.lower() == 'true' else 0

def add_pokedex():
    conn = sqlite3.connect('../database.db')
    cursor = conn.cursor()

    with open('../csv/pokemon.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insert with Zoneid=0 temporarily
            cursor.execute("""
                INSERT INTO Pokedex (
                    Zoneid, name, type_1, type_2,
                    ability_1, ability_1_is_hidden,
                    ability_2, ability_2_is_hidden,
                    ability_3, ability_3_is_hidden,
                    height, weight,
                    stat_hp, stat_attack, stat_defense,
                    stat_spattack, stat_spdef, stat_speed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                0,
                row['name'],
                row['type_1'],
                row['type_2'] if row['type_2'] else None,
                row['ability_1'],
                str_to_bool(row['ability_1_is_hidden']),
                row['ability_2'] if row['ability_2'] else None,
                str_to_bool(row['ability_2_is_hidden']) if row['ability_2_is_hidden'] else 0,
                row['ability_3'] if row['ability_3'] else None,
                str_to_bool(row['ability_3_is_hidden']) if row['ability_3_is_hidden'] else 0,
                int(float(row['height'])),
                int(float(row['weight'])),
                int(row['stat_hp']),
                int(row['stat_attack']),
                int(row['stat_defense']),
                int(row['stat_spattack']),
                int(row['stat_spdef']),
                int(row['stat_speed'])
            ))
            pokedex_id = cursor.lastrowid
            if pokedex_id < 100:
                zone_id = 1
            else:
                zone_id = pokedex_id // 100 + 1
            if zone_id > 13:
                zone_id = 13
            # Update Zoneid
            cursor.execute("UPDATE Pokedex SET Zoneid = ? WHERE Pokedexid = ?", (zone_id, pokedex_id))

    conn.commit()
    conn.close()
    print("Pokédex data inserted successfully.")

if __name__ == "__main__":
    add_pokedex()
