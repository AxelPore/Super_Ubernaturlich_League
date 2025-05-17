import csv
import os

# Define the CSV file name
CSV_FILE = 'csv/pokemon.csv'

# Define the columns
COLUMNS = [
    "name", "type_1", "type_2",
    "ability_1", "ability_1_is_hidden",
    "ability_2", "ability_2_is_hidden",
    "ability_3", "ability_3_is_hidden",
    "height", "weight",
    "stat_hp", "stat_attack", "stat_defense",
    "stat_spattack", "stat_spdef", "stat_speed",
    "sprite"
]

def get_input(column):
    """Prompt for each column, allow skipping."""
    raw = input(f"{column} (press Enter to skip): ").strip()
    if raw == "":
        return ""

    if column.endswith("_is_hidden"):
        return raw.lower() in ['true', '1', 'yes', 'y']
    elif column in ["height", "weight"]:
        try:
            return float(raw)
        except ValueError:
            print("⚠️ Invalid number. Skipping.")
            return ""
    elif column.startswith("stat_"):
        try:
            return int(raw)
        except ValueError:
            print("⚠️ Invalid integer. Skipping.")
            return ""
    else:
        return raw

def main():
    print("=== Add a new Pokémon entry ===")
    new_row = {col: get_input(col) for col in COLUMNS}

    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n✅ Pokémon added successfully!")

if __name__ == "__main__":
    main()
