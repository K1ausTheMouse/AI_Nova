# THIS IS ONLY TO DELETE ANYTHING IN THE MEMORY YOU DONT WANT NOVA TO STORE  

from datetime import datetime
import sqlite3

DB_PATH = "AI-memory-system/Memories.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# UNCOMMENT THIS LINE TO DELETE, FUTURE: MAYBE AN APP TO CONTROL NOVA'S MEMORY 

#cursor.execute("DELETE FROM memories WHERE id = ?", (,))
conn.commit()
