import sqlite3

# KEEP IF NEEDED PLEASE DONT DELL IT AGAIN 


DB_PATH = "AI_memory_system/Memories.db"

def delete_interaction(interaction_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM interactions
        WHERE id = ?
    """, (interaction_id,))

    conn.commit()
    conn.close()

#delete_interaction()
