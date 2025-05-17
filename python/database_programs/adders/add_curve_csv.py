import csv
import os

# CSV file name
CSV_FILE = 'csv/exp_curve.csv'  # You can change this

# Define columns
COLUMNS = ["#", "MS", "Pokemon", "Experience type"]

def get_input(column):
    """Prompt user and allow skipping."""
    raw = input(f"{column} (press Enter to skip): ").strip()
    if raw == "":
        return ""

    if column == "#":
        try:
            return int(raw)
        except ValueError:
            print("⚠️ Invalid number. Skipping.")
            return ""
    else:
        return raw

def main():
    print("=== Add a new Experience Table entry ===")
    new_row = {col: get_input(col) for col in COLUMNS}

    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n✅ Entry added successfully!")

if __name__ == "__main__":
    main()
