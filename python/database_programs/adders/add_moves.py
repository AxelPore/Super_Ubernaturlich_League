import csv
import sqlite3

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def add_moves():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    with open('csv/moves.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Move (
                    MoveName, type, power, effect_chance, accuracy,
                    priority, pp, class, crit_rate, drain,
                    flinch_chance, healing, max_hits, min_hits,
                    max_turns, min_turns, stat_chance, effect, buff_debuff
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['name'],
                row['type'],
                safe_int(row['power']),
                safe_int(row['effect_chance']),
                safe_int(row['accuracy']),
                safe_int(row['priority']),
                safe_int(row['pp']),
                row['class'],
                safe_int(row['crit_rate']),
                safe_int(row['drain']),
                safe_int(row['flinch_chance']),
                safe_int(row['healing']),
                safe_int(row['max_hits']),
                safe_int(row['min_hits']),
                safe_int(row['max_turns']),
                safe_int(row['min_turns']),
                safe_int(row['stat_chance']),
                row['effect'],
                row['']
            ))

    conn.commit()
    conn.close()
    print("Moves data inserted successfully.")

if __name__ == "__main__":
    add_moves()
