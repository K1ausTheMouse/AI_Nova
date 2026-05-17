from datetime import datetime
import sqlite3

DB_PATH = "AI-memory-system/Memories.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
#don't accidentally dell somthing lol
#cursor.execute("DELETE FROM memories WHERE id = ?", (,))
conn.commit()
