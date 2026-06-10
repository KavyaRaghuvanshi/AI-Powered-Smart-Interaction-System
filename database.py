import sqlite3

# Connect database
conn = sqlite3.connect("ai_system.db",check_same_thread=False)

cursor = conn.cursor()

# Create table
cursor.execute("""CREATE TABLE IF NOT EXISTS interactions(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               gesture TEXT,
               emotion TEXT,
               action TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
conn.commit()

# Insert data
def save_interaction(gesture,emotion,action):
    cursor.execute("""INSERT INTO interactions(gesture,emotion,action) VALUES (?, ?, ?)""", (gesture,emotion,action))

def get_all_interactions():
        cursor.execute("""SELECT gesture, emotion, action, timestamp FROM interactions ORDER BY timestamp DESC""")
        return cursor.fetchall()

conn.commit()