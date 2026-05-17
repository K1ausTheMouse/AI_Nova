from datetime import datetime
import sqlite3

DB_PATH = "AI-memory-system/Memories.db"


def add_entity(name, surname, age, entity_type, description, aliases):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO entities (name, surname, age, type, description, aliases, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, surname, age, entity_type, description, aliases, now, now
    ))

    conn.commit()
    conn.close()


def get_entity_id(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM entities WHERE name = ?", (name,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]


def add_interaction(entity_id, user_input, response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO interactions (entity_id, type, input, response, summary, mood, topic, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entity_id,
        "chat",
        user_input,
        response,
        "Basic interaction",
        "neutral",
        "general",
        now
    ))

    cursor.execute("""
    INSERT INTO memories (entity_id, title, content, type, importance, datetime, created_at, last_accessed)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entity_id,
        "Conversation",
        f"{user_input} -> {response}",
        "interaction",
        3,
        now,
        now,
        now
    ))

    conn.commit()
    conn.close()


def get_memories(entity_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT content FROM memories
    WHERE entity_id = ?
    ORDER BY importance DESC, datetime DESC
    LIMIT 5
    """, (entity_id,))

    result = cursor.fetchall()
    conn.close()

    return result

def get_memories(entity_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, content FROM memories
    WHERE entity_id = ?
    ORDER BY importance DESC, datetime DESC
    LIMIT 5 
    """, (entity_id,))
                   
                   
    results = cursor.fetchall()

    now = datetime.now().isoformat()

    for memory in results:
        memory_id = memory[0]
    
    cursor.execute("""
    UPDATE memories
    SET last_accessed = ?
    WHERE id = ?
    """, (now, memory_id))

    conn.commit()
    conn.close()

    return results


def search_memories(entity_id, keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT content FROM memories
    WHERE entity_id = ?
    AND content LIKE ?
    ORDER BY importance DESC, datetime DESC
    LIMIT 5 
    """, (entity_id, f"%{keyword}%"))

    results = cursor.fetchall()
    conn.close() 

    return results

nova_id = get_entity_id("Nova")

if nova_id is not None:
    add_interaction(nova_id, "Hello Nova", "Hi Klaus")
    print(get_memories(nova_id))
else:
    print("Nova does not exist in entities yet.")