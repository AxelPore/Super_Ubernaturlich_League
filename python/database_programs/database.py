import sqlite3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import adders.add_items as add_items
import adders.add_pokedex as add_pokedex
import adders.add_moves as add_moves
import adders.add_learning as add_learning
import adders.add_zones as add_zones
import adders.add_type as add_type

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
        Money INTEGER DEFAULT 1000,
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
        Pokedexid INTEGER NOT NULL,
        PokemonName TEXT NOT NULL,
        Surname TEXT,
        Level INTEGER NOT NULL,
        Exp INTEGER NOT NULL,
        Needed_exp INTEGER NOT NULL,
        Stat_hp INTEGER NOT NULL,
        Stat_attack INTEGER NOT NULL,
        Stat_defense INTEGER NOT NULL,
        Stat_spattack INTEGER NOT NULL,
        Stat_spdefense INTEGER NOT NULL,
        Stat_speed INTEGER NOT NULL,
        Stat_hp_ev INTEGER,
        Stat_attack_ev INTEGER,
        Stat_defense_ev INTEGER,
        Stat_spattack_ev INTEGER,
        Stat_spdefense_ev INTEGER,
        Stat_speed_ev INTEGER,
        Max_ev INTEGER,
        Stat_hp_iv INTEGER NOT NULL,
        Stat_attack_iv INTEGER NOT NULL,
        Stat_defense_iv INTEGER NOT NULL,
        Stat_spattack_iv INTEGER NOT NULL,
        Stat_spdefense_iv INTEGER NOT NULL,
        Stat_speed_iv INTEGER NOT NULL,
        Move1 TEXT,
        Move2 TEXT,
        Move3 TEXT,
        Move4 TEXT,
        Ability TEXT,
        Userid INTEGER,
        FOREIGN KEY (Pokedexid) REFERENCES Pokedex(Pokedexid),
        FOREIGN KEY (Move1) REFERENCES Move(MoveName),
        FOREIGN KEY (Move2) REFERENCES Move(MoveName),
        FOREIGN KEY (Move3) REFERENCES Move(MoveName),
        FOREIGN KEY (Move4) REFERENCES Move(MoveName),
        FOREIGN KEY (Userid) REFERENCES User(Userid)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Learning (
        Learningid INTEGER PRIMARY KEY AUTOINCREMENT,
        Pokedexid INTEGER NOT NULL,
        Moveid INTEGER NOT NULL,
        Foreign KEY (Pokedexid) REFERENCES Pokedex(Pokedexid),
        Foreign KEY (Moveid) REFERENCES Move(Moveid)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Move (
        Moveid INTEGER PRIMARY KEY AUTOINCREMENT,
        MoveName TEXT NOT NULL,
        type TEXT NOT NULL,
        power INTEGER NOT NULL,
        effect_chance INTEGER NOT NULL,
        accuracy INTEGER NOT NULL,
        priority INTEGER NOT NULL,
        pp INTEGER NOT NULL,
        class TEXT NOT NULL,
        crit_rate INTEGER NOT NULL,
        drain INTEGER NOT NULL,
        flinch_chance INTEGER NOT NULL,
        healing INTEGER NOT NULL,
        max_hits INTEGER NOT NULL,
        min_hits INTEGER NOT NULL,
        max_turns INTEGER NOT NULL,
        min_turns INTEGER NOT NULL,
        stat_chance INTEGER NOT NULL,
        effect Text,
        buff_debuff INTEGER
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Type (
        Typeid INTEGER PRIMARY KEY AUTOINCREMENT,
        Attacking TEXT NOT NULL,
        Normal INTEGER NOT NULL,
        Fire INTEGER NOT NULL,
        Water INTEGER NOT NULL,
        Electric INTEGER NOT NULL,
        Grass INTEGER NOT NULL,
        Ice INTEGER NOT NULL,
        Fighting INTEGER NOT NULL,
        Poison INTEGER NOT NULL,
        Ground INTEGER NOT NULL,
        Flying INTEGER NOT NULL,
        Psychic INTEGER NOT NULL,
        Bug INTEGER NOT NULL,
        Rock INTEGER NOT NULL,
        Ghost INTEGER NOT NULL,
        Dragon INTEGER NOT NULL,
        Dark INTEGER NOT NULL,
        Steel INTEGER NOT NULL,
        Fairy INTEGER NOT NULL
    );              
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Zone (
        Zoneid INTEGER PRIMARY KEY AUTOINCREMENT,
        ZoneName TEXT NOT NULL,
        ZonePosition INTEGER NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pokedex (
        Pokedexid INTEGER PRIMARY KEY AUTOINCREMENT,
        Zoneid INTEGER NOT NULL,
        name TEXT NOT NULL,
        type_1 TEXT NOT NULL,
        type_2 TEXT,
        base_experience INTEGER NOT NULL,
        min_spawn_level INTEGER NOT NULL,
        max_spawn_level INTEGER NOT NULL,
        exp_curve TEXT NOT NULL,
        Evolving_to TEXT,
        Evolving_level INTEGER,
        Evolving_to2 TEXT,
        Evolving_level2 INTEGER,
        Evolving_to3 TEXT,
        Evolving_level3 INTEGER,
        Evolving_to4 TEXT,
        Evolving_level4 INTEGER,
        Evolving_to5 TEXT,
        Evolving_level5 INTEGER,
        Evolving_to6 TEXT,
        Evolving_level6 INTEGER,
        Evolving_to7 TEXT,
        Evolving_level7 INTEGER,
        Evolving_to8 TEXT,
        Evolving_level8 INTEGER,
        Evolving_to9 TEXT,
        Evolving_level9 INTEGER,
        Evolving_to10 TEXT,
        Evolving_level10 INTEGER,
        ability_1 TEXT NOT NULL,
        ability_1_is_hidden BOOLEAN NOT NULL,
        ability_2 TEXT,
        ability_2_is_hidden BOOLEAN,
        ability_3 TEXT,
        ability_3_is_hidden BOOLEAN,
        height INTEGER NOT NULL,
        weight INTEGER NOT NULL,
        stat_hp INTEGER NOT NULL,
        stat_attack INTEGER NOT NULL,
        stat_defense INTEGER NOT NULL,
        stat_spattack INTEGER NOT NULL,
        stat_spdef INTEGER NOT NULL,
        stat_speed INTEGER NOT NULL,
        ev_hp INTEGER,
        ev_atk INTEGER,
        ev_def INTEGER,
        ev_spatk INTEGER,
        ev_spdef INTEGER,
        ev_speed INTEGER,
        FOREIGN KEY (Zoneid) REFERENCES Zone(Zoneid)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Item (
        Itemid INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemName TEXT NOT NULL,
        ItemPrice INTEGER NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Inventory (
        Iventoryid INTEGER PRIMARY KEY AUTOINCREMENT,
        Itemid INTEGER NOT NULL,
        Quantity INTEGER NOT NULL,
        Userid INTEGER NOT NULL,
        FOREIGN KEY (Itemid) REFERENCES Item(Itemid)
        FOREIGN KEY (Userid) REFERENCES User(Userid)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    add_pokedex.add_pokedex()
    add_moves.add_moves()
    add_learning.add_learning()
    add_items.add_items()
    add_zones.add_zones()
    add_type.add_type()
    print("Database and tables created successfully.")
