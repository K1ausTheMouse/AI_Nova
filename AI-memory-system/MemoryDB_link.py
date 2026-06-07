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


def get_entity(entity_id= None, name= None, surname= None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT* FROM entity WHERE id = ? OR (name = ? AND surname = ?)",(id, name, surname))
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
        WHERE id = ?
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


def add_memory(
    entity_id,
    title,
    content,
    source,
    confidence,
    memory_type,
    importance,
    created_at
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memories (
            entity_id,
            title,
            content,
            source,
            confidence,
            type,
            importance,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,(
        entity_id,
        title,
        content,
        source,
        confidence,
        memory_type,
        importance,
        created_at   
        ))
    
    
    conn.commit()
    conn.close()



#add_memory()


#get_memories_for_entity()




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


# TODO: 

# use "with sqlite3.connect(DB_PATH) as conn:"

# FUCTCTIONS FOR LATER TO MAKES LINKS FOR THE AI TO ACCESS THE DB 



#add_memory()
#get_memories_for_entity()


#add_relationship()
#get_relationships()

#add_interaction()
#get_recent_interactions()

#set_environment_value()
#get_environment_value()
