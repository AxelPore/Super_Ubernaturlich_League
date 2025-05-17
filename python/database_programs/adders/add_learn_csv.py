import csv
import os

CSV_FILE = 'csv/learning.csv'  # Update this if needed

COLUMNS = ["pokemon", "move", "level_learned_at", "learn_method", "game"]

def get_input(column):
    """Prompt for input with optional skipping."""
    raw = input(f"{column} (press Enter to skip): ").strip()
    if raw == "":
        return ""

    if column == "level_learned_at":
        try:
            return int(raw)
        except ValueError:
            print("⚠️ Invalid level. Saving as blank.")
            return ""
    else:
        return raw

def main():
    print("=== Add a new Learnset entry ===")
    new_row = {col: get_input(col) for col in COLUMNS}

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n✅ Learnset entry added successfully!")

if __name__ == "__main__":
    main()
