import csv
import sqlite3

def add_type():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    with open('csv/chart.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("INSERT INTO Type (Attacking, Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                row['Attacking'],
                row['Normal'],
                row['Fire'],
                row['Water'],
                row['Electric'],
                row['Grass'],
                row['Ice'],
                row['Fighting'],
                row['Poison'],
                row['Ground'],
                row['Flying'],
                row['Psychic'],
                row['Bug'],
                row['Rock'],
                row['Ghost'],
                row['Dragon'],
                row['Dark'],
                row['Steel'],
                row['Fairy']
                ))
    conn.commit()
    conn.close()
            
if __name__ == "__main__":
    add_type()