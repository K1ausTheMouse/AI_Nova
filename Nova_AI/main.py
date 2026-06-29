from ollama_client import chat_with_nova
from prompt import SYSTEM_PROMPT
#import sys
#from pathlib import Path

#sys.path.append(
 #   str(Path(__file__).resolve().parent.#parent / "AI_memory_system")
#)

from AI_memory_system.context.processor import generate_summary, generate_topic
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

    summary = generate_summary(user_input, response)
    print("Summary:", summary)
    topic = generate_topic(user_input, response)


    # memory links to save and retreve data 

    # interactions 

    MemoryDB_link.add_interaction(
        entity_id = None,
        type = "chat",
        user_input = user_input,
        response = response,
        summary = summary,
        topic = topic
    )

    


# functions  
   
""" 
# ENTITYS 

add_entity()
get_entity_id()
get_entity()
update_entity()
update_entity_age()
delete_entity()
search_entity()
check_entities()

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