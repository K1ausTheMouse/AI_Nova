from datetime import datetime
import sqlite3
import json

# AI FROM JSON TO DB , ALSO HOLDS CACHE MEMORY IN JSON 

DB_PATH = "AI-memory-system/Memories.db"
CACHE_PATH = "AI-memory-system/interations_cache.json"


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


def get_entity(entity_id= None, name= None, surname= None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT* FROM entity WHERE id = ? OR (name = ? AND surname = ?)",(entity_id, name, surname))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None
    
    return row[0]


def update_entity(entity_id, new_description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        UPDATE entities
        SET description = ?,
        updated_at = ?,
        WHERE entity_id = ?
    """,(new_description, now, entity_id))

    conn.commit()
    conn.close()

    

def update_entity_age(entity_id, new_age):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        UPDATE entities
        SET age = ?, updated_at = ?
        WHERE id = ?
    """, (new_age, now, entity_id))

    conn.commit()
    conn.close()


def delete_entity(entity_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM entities
    WHERE entity_id = ?
                   
    """,(entity_id,))

    conn.commit()
    conn.close()



# SHOULD I UPGRADE IT SO NOVA CAN SEARCH FROM CHATS? IDK IF AI ALREADY DOES THAT BUT WE WILL SEE IN THE FUTURE IF I NEED TO ADD IT
def search_entity(name, surname):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT entity_id
        FROM entities
        WHERE name = ?
        AND (
            surname = ?
            OR (surname IS NULL AND ? IS NULL)
        )
    """, (name, surname, surname))

    result = cursor.fetchone()

    conn.close()

    return result




def add_memory(entity_id, title, content, source, confidence, type, importance , datetime):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO MEMORIES (
        entity_id,
        title,
        content, 
        source,
        confidence,
        type,
        importance,
        datetime, 
        created_at, 
        last_accessed)
    VALUES(?,?,?,?,?,?,?,?,?,?)
    """,(entity_id,
        title,
        content, 
        source,
        confidence,
        type,
        importance,
        datetime, 
        now, 
        now))

    conn.commit()
    conn.close()


def get_memories_for_entity(entity_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        entity_id,
        title,
        content,
        importance,
        confidence 
    content FROM memories
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




def search_memories(entity_id, keyword=None):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title,
       content,
       importance,
       confidence,
       datetime
    FROM memories
    WHERE entity_id = ?
    AND(
        title LIKE ?
        OR content LIKE ?
    )
    ORDER BY importance DESC, datetime DESC
    LIMIT 5 
    """, (entity_id, f"%{keyword}%",f"%{keyword}%"))

    results = cursor.fetchall()
    cursor.close()
    conn.close() 

    return results

def delete_memory(memory_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM entities
    WHERE id = ?
                   
    """,(memory_id,))

    conn.commit()
    conn.close()


def update_memory(memory_id, entity_id, content, importance, confidence):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

   

    cursor.execute("""
        UPDATE memories
        SET 
            content = ?,
            importance = ?,
            confidence = ?,
            last_accessed = ?
        WHERE entity_id = ? OR id = ?
    """,(
        content,
        importance,
        confidence,
        datetime.now().isoformat(),
        entity_id,
        memory_id
    ))

    conn.commit()
    conn.close()


def check_entities(entity_id, name, surname):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
    SELECT EXISTS(
        SELECT 1
        FROM entities
        WHERE entity_id = ?
        OR (name = ? AND surname = ?)
    )
    """, (entity_id, name, surname))

    exists = cursor.fetchone()[0]

    conn.close()

    return bool(exists)



def add_relationship(from_entity_id, to_entity_id, relation, strength=None):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(""" 
    INSERT INTO relationships (
        from_entity_id, 
        to_entity_id, 
        relation,
        strength, 
        created_at
    )

    VALUES (?, ?, ?, ?, ?)""",( 
        from_entity_id,
        to_entity_id,
        relation,
        strength,
        now))

    conn.commit()
    conn.close()


def get_relationships(entity_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM relationships
        WHERE from_entity_id = ?
        OR to_entity_id = ?
    """, (entity_id, entity_id))

    rows = cursor.fetchall()
    conn.close()

    return rows



def add_interaction(
    entity_id,
    type,
    user_input,
    response=None,
    summary=None,
    mood=None,
    topic=None
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO interactions(
        entity_id,
        type,
        input,
        response,
        summary,
        mood,
        topic,
        now               
    )

    VALUES(?,?,?,?,?,?,?,?)""",(
        entity_id,
        type,
        user_input,
        response,
        summary,
        mood,
        topic,
        now ))

    conn.commit()
    conn.close()


def get_recent_interactions(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    interactions = []

    cursor.execute(""" 
        SELECT id, entity_id, type, input, response, summary, mood, topic, created_at
        FROM interactions
        ORDER BY created_at DESC
        LIMIT ?
    """,(limit,))

    rows = cursor.fetchall()
    conn.close()


    for row in rows:
        interactions.append({
            "id": row[0],
            "entity_id": row[1],
            "type": row[2],
            "input": row[3],
            "response": row[4],
            "summary": row[5],
            "mood": row[6],
            "topic": row[7],
            "created_at": row[8]
        })
    
    return interactions 

def update_recent_interaction_cache(limit=50):
    recent = get_recent_interactions(limit)

    with open(CACHE_PATH, "w", encoding="utf-8") as file:
        json.dump(recent, file, indent=4)
    



def compress_interactions_to_memory(entity_id, limit):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT input,response, summary, mood, topic, created_at
        FROM interactions
        WHERE entity_id = ?
        ORDER BY created_at DESC
        LIMIT ?

    """, (entity_id, limit))

    rows = cursor.fetchall()
    
    if not rows:
        conn.close()
        return None
    
    summaries = []

    for row in rows:
        user_input = row[0]
        response = row[1]
        summary = row[2]
        mood = row[3]
        topic = row[4]

        if summary:
            summaries.append(summary)
        else:
            summaries.append(f"User said: {user_input} | Assistant replied: {response}")
    
    memory_content = "\n".join(summaries)

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO memories(
        entity_id,
        title,
        content,
        source,
        confidence,
        type,
        importance,
        created_at,
        last_accessed
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entity_id,
        "Compressed recent interaction",
        memory_content,
        "Interactions",
        70,
        "Compressed_summary",
        5,
        now,
        now
    ))

    conn.commit()
    conn.close()

    return memory_content

def add_enviroment_item(type, file_path=None, description=None, summary=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO enviroment(
                type,
                file_path,
                description,
                summary
            )
            VALUES (?,?,?,?)
        """,(
            type,
            file_path,
            description,
            summary
        ))

        conn.commit()


def get_enviroment_item(type=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        if type:
            cursor.execute("""
                SELECT id, type, file_path, description,summary
                FROM enviroment 
                WHERE type = ?
            """,(type,))
        else:
            cursor.execute("""
                SELECT id, type, file_path, description, summary
                FROM enviroment
            """)

        rows = cursor.fetchall()

    items = []

    for row in rows:
        items.append({
            "id": row[0],
            "type": row[1],
            "file_path": row[2],
            "description": row[3],
            "summary": row[4]
        })

    return items
        


# TODO: 
# MAYBE
# use "with sqlite3.connect(DB_PATH) as conn:"

