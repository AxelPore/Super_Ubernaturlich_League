import csv
import sqlite3

def str_to_bool(s):
    return 1 if s.lower() == 'true' else 0

def add_pokedex():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    with open('csv/pokemon.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insert with Zoneid=0 temporarily
            cursor.execute("""
                INSERT INTO Pokedex (
                    base_experience, min_spawn_level, max_spawn_level, exp_curve, Zoneid, name, type_1, type_2,
                    ability_1, ability_1_is_hidden,
                    ability_2, ability_2_is_hidden,
                    ability_3, ability_3_is_hidden,
                    height, weight,
                    stat_hp, stat_attack, stat_defense,
                    stat_spattack, stat_spdef, stat_speed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                0,
                0,
                0,
                "Fast",
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
            
    with open('csv/exp_curve.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("UPDATE Pokedex SET exp_curve = ? WHERE name = ?", (row['Experience type'], (row['Pokémon'])))
            
    with open('csv/base_xp_and_evs.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("UPDATE Pokedex SET base_experience = ?, ev_hp = ?, ev_atk = ?, ev_def = ?, ev_spatk = ?, ev_spdef = ?, ev_speed = ? WHERE name = ?", (int(row['Exp']), int(row['HP']), int(row['Attack']), int(row['Defense']), int(row['Sp.Attack']), int(row['Sp.Defense']), int(row['Speed']), (row['Pokémon'])))
            
    with open('csv/evolution_long.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        tmp_pokemon = {}
        for row in reader:
            tmp_evo = [[row['Evolving_to'], row['value']]]
            if len(tmp_pokemon) == 0:
                tmp_pokemon[row['Evolving_from']] = tmp_evo
                continue
            for key, value in tmp_pokemon.items():
                if key == row['Evolving_from']:
                    value.append([row['Evolving_to'], row['value']])
                else :
                    tmp_pokemon[row['Evolving_from']] = tmp_evo
        for key, value in tmp_pokemon.items():
            if len(value) == 1:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ? WHERE name = ?", (value[0][0], int(value[0][1]), key))
            if len(value) == 2:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ? WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), key))
            if len(value) == 3:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ?, Evolving_to3 = ?, Evolving_level3 = ? WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), value[2][0], int(value[2][1]), key))
            if len(value) == 4:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ?, Evolving_to3 = ?, Evolving_level3 = ?, Evolving_to4 = ?, Evolving_level4 = ?, WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), value[2][0], int(value[2][1]), value[3][0], int(value[3][1]), key))
            if len(value) == 5:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ?, Evolving_to3 = ?, Evolving_level3 = ?, Evolving_to4 = ?, Evolving_level4 = ?, Evolving_to5 = ?, Evolving_level5 = ? WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), value[2][0], int(value[2][1]), value[3][0], int(value[3][1]), value[4][0], int(value[4][1]), key))
            if len(value) == 6:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ?, Evolving_to3 = ?, Evolving_level3 = ?, Evolving_to4 = ?, Evolving_level4 = ?, Evolving_to5 = ?, Evolving_level5 = ?, Evolving_to6 = ?, Evolving_level6 = ? WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), value[2][0], int(value[2][1]), value[3][0], int(value[3][1]), value[4][0], int(value[4][1]), value[5][0], int(value[5][1]), key))
            if len(value) == 7:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ?, Evolving_to3 = ?, Evolving_level3 = ?, Evolving_to4 = ?, Evolving_level4 = ?, Evolving_to5 = ?, Evolving_level5 = ?, Evolving_to6 = ?, Evolving_level6 = ?, Evolving_to7 = ?, Evolving_level7 = ? WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), value[2][0], int(value[2][1]), value[3][0], int(value[3][1]), value[4][0], int(value[4][1]), value[5][0], int(value[5][1]), value[6][0], int(value[6][1]), key))
            if len(value) == 8:
                cursor.execute("UPDATE Pokedex SET Evolving_to = ?, Evolving_level = ?, Evolving_to2 = ?, Evolving_level2 = ?, Evolving_to3 = ?, Evolving_level3 = ?, Evolving_to4 = ?, Evolving_level4 = ?, Evolving_to5 = ?, Evolving_level5 = ?, Evolving_to6 = ?, Evolving_level6 = ?, Evolving_to7 = ?, Evolving_level7 = ?, Evolving_to8 = ?, Evolving_level8 = ? WHERE name = ?", (value[0][0], int(value[0][1]), value[1][0], int(value[1][1]), value[2][0], int(value[2][1]), value[3][0], int(value[3][1]), value[4][0], int(value[4][1]), value[5][0], int(value[5][1]), value[6][0], int(value[6][1]), value[7][0], int(value[7][1]), key))
    conn.commit()
    conn.close()
    print("Pokédex data inserted successfully.")

if __name__ == "__main__":
    add_pokedex()
