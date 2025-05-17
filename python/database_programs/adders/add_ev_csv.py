import csv
import os

CSV_FILE = 'csv/base_xp_and_evs.csv'  # Adjust this to your file

COLUMNS = [
    "#", "Blank", "Pokemon", "Exp", "HP", "Attack", "Defense",
    "Sp.Attack", "Sp.Defense", "Speed", "Total EVs"
]

def get_input(column):
    """Prompt user input with optional skipping."""
    raw = input(f"{column} (press Enter to skip): ").strip()
    if raw == "":
        return ""

    if column in ["#", "Exp", "HP", "Attack", "Defense", "Sp.Attack", "Sp.Defense", "Speed", "Total EVs"]:
        try:
            return int(raw)
        except ValueError:
            print("⚠️ Invalid number. Saving as blank.")
            return ""
    else:
        return raw

def main():
    print("=== Add a new EV Table entry ===")
    new_row = {col: get_input(col) for col in COLUMNS}

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n✅ EV entry added successfully!")

if __name__ == "__main__":
    main()
