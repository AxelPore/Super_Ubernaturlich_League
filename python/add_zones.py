import sqlite3

def add_zones():
    conn = sqlite3.connect('../database.db')
    cursor = conn.cursor()
    zonename = ["Stardust Valley", "Verdale Grove", "Crimson Spires", "Lumina Shores", "Aurora City", "Obsidian Hollow", "Glimmerfen Marsh", "Stormreach Cliffs", "Duskwind Plains", "Frostvale Ridge", "Thornveil Thicket", "Mystvale Ruins", "Ironroot Basin", "Solstice Crater"]
    zoneposition = [1,2,3,4,10,11,12,13,14,15,21,22,23,24]
    for i in range(len(zonename)):
        cursor.execute("""INSERT INTO Zone (ZoneName, ZonePosition) VALUES (?, ?)""", (zonename[i], zoneposition[i]))
    