import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        Userid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        Equipeid INTEGER,
        Zoneid INTEGER,
        FOREIGN KEY (Zoneid) REFERENCES Zone(Zoneid),
        FOREIGN KEY (Equipeid) REFERENCES Equipe(Equipeid)
    );
    """)

    # Create Equipe table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Equipe (
        Equipeid INTEGER PRIMARY KEY AUTOINCREMENT,
        Pokemon1 integer,
        Pokemon2 integer,
        Pokemon3 integer,
        Pokemon4 integer,
        FOREIGN KEY (Pokemon1) REFERENCES Pokemon(Pokemonid),
        FOREIGN KEY (Pokemon2) REFERENCES Pokemon(Pokemonid),
        FOREIGN KEY (Pokemon3) REFERENCES Pokemon(Pokemonid),
        FOREIGN KEY (Pokemon4) REFERENCES Pokemon(Pokemonid)
    );
    """)

    # Create Pokemon table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pokemon (
        Pokemonid INTEGER PRIMARY KEY AUTOINCREMENT,
        PokemonName TEXT NOT NULL,
        Surname TEXT,
        Move1 TEXT,
        Move2 TEXT,
        Move3 TEXT,
        Move4 TEXT,
        Ability TEXT,
        Userid INTEGER,
        FOREIGN KEY (Userid) REFERENCES User(Userid)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Zone (
        Zoneid INTEGER PRIMARY KEY AUTOINCREMENT,
        ZoneName TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WildPokemon (
        WildPokemonid INTEGER PRIMARY KEY AUTOINCREMENT,
        Zoneid INTEGER NOT NULL,
        FOREIGN KEY (Zoneid) REFERENCES Zone(Zoneid)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")
