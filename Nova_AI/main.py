from ollama_client import chat_with_nova
from prompt import SYSTEM_PROMPT


from AI_memory_system.context.processor import process_context, processor_entities
from AI_memory_system import MemoryDB_link
import tools

# main loop for the ai chat 
while True:
    # messages 
    user_input = input("> ")

    if user_input.lower() in ["exit", "quit"]:
        break

    

    context = tools.find_relevant_context(user_input)


    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + "\n\nRecent previous chats:\n" + context 
        },
        {
            "role": "user",
            "content": user_input
        }
    ]


    response = chat_with_nova(messages)

    print(f"\n Nova: {response}\n")

    messages.append({
        "role": "assistant",
        "content": response
    })

    context = process_context(user_input, response)
    entities = processor_entities(user_input, response)

    # memory links to save and retreve data 

    # interactions 

    MemoryDB_link.add_interaction(
        entity_id = 2,
        type = "chat",
        user_input = user_input,
        response = response,
        summary = context["summary"],
        topic = context["topic"],
        mood = context["mood"]
   
    )


    # entities 

    
    MemoryDB_link.add_entity(
        name = entities["name"],
        surname = entities["surname"],
        age = entities["age"],
        entity_type = entities["type"],
        description = entities["description"],
        aliases = entities["aliases"]
    )


    entity_id = MemoryDB_link.get_entity_id(
        entities["match_name"],
        entities["surname"]
        )
    
    if entity_id is None:
        print("Not found Entity")
       # MemoryDB_link.add_entity()

    
    MemoryDB_link.update_entity(
        entity_id = entity_id,
        name = entities["name"],
        surname = entities["surname"],
        age = entities["age"],
        entity_type = entities["type"],
        description = entities["description"],
        aliases = entities["aliases"]
    )



    MemoryDB_link.delete_entity(entity_id)

    

    


# functions  

"""
add a dell to interactions and so on with interactions 
"""
   
""" 
# ENTITYS 

add_entity() done
get_entity_id()
get_entity()
update_entity() done 
update_entity_age()
delete_entity()
search_entity()
check_entities()
---------------------
use this for now 

add_entity() - done 
get_entity()
get_entity_id()
update_entity() - done 
delete_entity()

"""

"""
# Memory

add_memory()
get_memories_for_entity()
search_memories()
update_memory()
delete_memory()
compress_interactions_to_memory()

"""

"""
#relationship

add_relationship()
get_relationships()

"""

"""
# enviroment

add_enviroment_item()
get_enviroment_item()
"""