from datetime import datetime
import sqlite3
import json

# AI FROM JSON TO DB , ALSO HOLDS CACHE MEMORY IN JSON 

DB_PATH = "AI-memory-system/Memories.db"

def add_entity(name, entity_type, description=None, aliases=None, surname=None, age=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()
    aliases_json = json.dumps(aliases or [])

    cursor.execute("""
    INSERT INTO entities (name, surname, age, type, description, aliases, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, 
        surname, 
        age, 
        entity_type, 
        description, 
        aliases_json, 
        now, 
        now
    ))

    conn.commit()
    conn.close()



def get_entity_id(name, surname):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM entities WHERE name = ? AND surname = ?", (name, surname))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]

# TODO: 

# use "with sqlite3.connect(DB_PATH) as conn:"

# FUCTCTIONS FOR LATER TO MAKES LINKS FOR THE AI TO ACCESS THE DB 

#get_entity()
#update_entity()
#delete_entity()
#search_entities()