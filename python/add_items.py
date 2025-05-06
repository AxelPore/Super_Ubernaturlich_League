import csv
import sqlite3

def add_items():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    with open('csv/items.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Item (
                    ItemName
                ) VALUES (?)
            """, (
                row['identifier'],
            ))

    conn.commit()
    conn.close()
    print("Items data inserted successfully.")

if __name__ == "__main__":
    add_items()
