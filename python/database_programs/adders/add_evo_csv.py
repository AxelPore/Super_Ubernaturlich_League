import csv
import os

CSV_FILE = 'csv/evolution_long.csv'  # Adjust if needed

COLUMNS = ["Unnamed: 0", "Evolving_from", "Evolving_to", "trigger", "id", "Condition", "value"]

def get_input(column):
    """Prompt with option to skip."""
    raw = input(f"{column} (press Enter to skip): ").strip()
    if raw == "":
        return ""

    if column in ["Unnamed: 0", "id"]:
        try:
            return int(raw)
        except ValueError:
            return raw  # allow non-numeric ids too
    else:
        return raw

def main():
    print("=== Add a new Evolution entry ===")
    new_row = {col: get_input(col) for col in COLUMNS}

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n✅ Evolution entry added successfully!")

if __name__ == "__main__":
    main()
