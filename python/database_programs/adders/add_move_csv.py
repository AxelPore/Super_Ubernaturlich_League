import csv
import os

CSV_FILE = 'csv/moves.csv'  # Change to your actual CSV file name

COLUMNS = [
    "name", "accuracy", "effect_chance", "pp", "priority", "power",
    "class", "type", "crit_rate", "drain", "flinch_chance", "healing",
    "max_hits", "min_hits", "max_turns", "min_turns", "stat_chance", "effect"
]

def get_input(column):
    """Prompt for input with type handling and skipping."""
    raw = input(f"{column} (press Enter to skip): ").strip()
    if raw == "":
        return ""

    try:
        # Try to parse numeric values where appropriate
        if column in ["accuracy", "effect_chance", "pp", "priority", "power",
                      "crit_rate", "drain", "flinch_chance", "healing",
                      "max_hits", "min_hits", "max_turns", "min_turns", "stat_chance"]:
            if '.' in raw:
                return float(raw)
            else:
                return int(raw)
    except ValueError:
        print(f"⚠️ Invalid number for {column}. Saving as blank.")
        return ""

    return raw  # for strings

def main():
    print("=== Add a new Move entry ===")
    new_row = {col: get_input(col) for col in COLUMNS}

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n✅ Move entry added successfully!")

if __name__ == "__main__":
    main()
